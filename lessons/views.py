from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import (
    render,
    get_object_or_404,
    redirect
)
from django.utils import timezone

from certificates.models import Certificate
from quizzes.models import Quiz, QuizAttempt
from courses.models import Course
from enrollments.models import Enrollment

from .models import Lesson, LessonProgress
from .forms import LessonForm


# =====================================================
# INSTRUCTOR ROLE CHECK
# =====================================================

def instructor_required(view_func):

    @login_required
    def wrapper(request, *args, **kwargs):

        if request.user.role not in ["instructor", "admin"]:

            messages.error(
                request,
                "You do not have permission to access the instructor area."
            )

            return redirect("dashboard")

        return view_func(request, *args, **kwargs)

    return wrapper


# =====================================================
# INSTRUCTOR LESSON MANAGEMENT
# =====================================================

@instructor_required
def manage_lessons(request, course_id):

    course = get_object_or_404(
        Course,
        id=course_id,
        instructor=request.user
    )

    lessons = Lesson.objects.filter(
        course=course
    ).order_by("order")

    return render(
        request,
        "lessons/manage_lessons.html",
        {
            "course": course,
            "lessons": lessons,
        }
    )


# =====================================================
# ADD LESSON
# =====================================================

@instructor_required
def add_lesson(request, course_id):

    course = get_object_or_404(
        Course,
        id=course_id,
        instructor=request.user
    )

    if request.method == "POST":

        form = LessonForm(request.POST)

        if form.is_valid():

            lesson = form.save(
                commit=False
            )

            lesson.course = course
            lesson.save()

            messages.success(
                request,
                "Lesson added successfully!"
            )

            return redirect(
                "manage_lessons",
                course_id=course.id
            )

    else:

        last_lesson = Lesson.objects.filter(
            course=course
        ).order_by(
            "-order"
        ).first()

        next_order = (
            last_lesson.order + 1
            if last_lesson
            else 1
        )

        form = LessonForm(
            initial={
                "order": next_order
            }
        )

    return render(
        request,
        "lessons/lesson_form.html",
        {
            "form": form,
            "course": course,
            "page_title": "Add Lesson",
            "button_text": "Add Lesson",
        }
    )


# =====================================================
# EDIT LESSON
# =====================================================

@instructor_required
def edit_lesson(request, lesson_id):

    lesson = get_object_or_404(
        Lesson,
        id=lesson_id,
        course__instructor=request.user
    )

    if request.method == "POST":

        form = LessonForm(
            request.POST,
            instance=lesson
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Lesson updated successfully!"
            )

            return redirect(
                "manage_lessons",
                course_id=lesson.course.id
            )

    else:

        form = LessonForm(
            instance=lesson
        )

    return render(
        request,
        "lessons/lesson_form.html",
        {
            "form": form,
            "course": lesson.course,
            "lesson": lesson,
            "page_title": "Edit Lesson",
            "button_text": "Save Changes",
        }
    )


# =====================================================
# DELETE LESSON
# =====================================================

@instructor_required
def delete_lesson(request, lesson_id):

    lesson = get_object_or_404(
        Lesson,
        id=lesson_id,
        course__instructor=request.user
    )

    if request.method == "POST":

        course_id = lesson.course.id

        lesson.delete()

        messages.success(
            request,
            "Lesson deleted successfully!"
        )

        return redirect(
            "manage_lessons",
            course_id=course_id
        )

    return render(
        request,
        "lessons/lesson_confirm_delete.html",
        {
            "lesson": lesson
        }
    )


# =====================================================
# STUDENT LESSONS HOME
# =====================================================

@login_required
def lessons_home(request):

    lessons = Lesson.objects.all().order_by(
        "course",
        "order"
    )

    return render(
        request,
        "lessons/lessons_home.html",
        {
            "lessons": lessons
        }
    )


# =====================================================
# STUDENT LESSON LIST
# =====================================================

@login_required
def lesson_list(request, course_id):

    course = get_object_or_404(
        Course,
        id=course_id
    )

    is_enrolled = Enrollment.objects.filter(
        student=request.user,
        course=course
    ).exists()

    if not is_enrolled:

        return redirect(
            "course_detail",
            course_id=course.id
        )

    lessons = Lesson.objects.filter(
        course=course
    ).order_by(
        "order"
    )

    completed_lessons = LessonProgress.objects.filter(
        student=request.user,
        lesson__course=course,
        completed=True
    ).values_list(
        "lesson_id",
        flat=True
    )

    completed_lessons = set(
        completed_lessons
    )

    total_lessons = lessons.count()

    completed_count = len(
        completed_lessons
    )

    if total_lessons > 0:

        course_progress = int(
            (completed_count / total_lessons) * 100
        )

    else:

        course_progress = 0

    # =================================================
    # QUIZ INFORMATION
    # =================================================

    quizzes = Quiz.objects.filter(
        course=course
    )

    quiz_attempts = QuizAttempt.objects.filter(
        quiz__course=course,
        student=request.user
    )

    quiz_passed = False

    for attempt in quiz_attempts:

        if attempt.total_questions > 0:

            percentage = int(
                (attempt.score / attempt.total_questions) * 100
            )

            if percentage >= 50:

                quiz_passed = True
                break

    return render(
        request,
        "lessons/lesson_list.html",
        {
            "course": course,
            "lessons": lessons,
            "completed_lessons": completed_lessons,
            "total_lessons": total_lessons,
            "completed_count": completed_count,
            "course_progress": course_progress,
            "quizzes": quizzes,
            "quiz_passed": quiz_passed,
        }
    )


# =====================================================
# STUDENT LESSON DETAIL
# =====================================================

@login_required
def lesson_detail(request, lesson_id):

    lesson = get_object_or_404(
        Lesson,
        id=lesson_id
    )

    # =================================================
    # CHECK ENROLLMENT
    # =================================================

    is_enrolled = Enrollment.objects.filter(
        student=request.user,
        course=lesson.course
    ).exists()

    if not is_enrolled:

        return redirect(
            "course_detail",
            course_id=lesson.course.id
        )

    # =================================================
    # GET OR CREATE PROGRESS
    # =================================================

    progress, created = LessonProgress.objects.get_or_create(
        student=request.user,
        lesson=lesson
    )

    # =================================================
    # PREVIOUS LESSON
    # =================================================

    previous_lesson = Lesson.objects.filter(
        course=lesson.course,
        order__lt=lesson.order
    ).order_by(
        "-order"
    ).first()

    # =================================================
    # NEXT LESSON
    # =================================================

    next_lesson = Lesson.objects.filter(
        course=lesson.course,
        order__gt=lesson.order
    ).order_by(
        "order"
    ).first()

    # =================================================
    # TOTAL LESSONS
    # =================================================

    total_lessons = Lesson.objects.filter(
        course=lesson.course
    ).count()

    # =================================================
    # COMPLETED LESSONS
    # =================================================

    completed_lessons = LessonProgress.objects.filter(
        student=request.user,
        lesson__course=lesson.course,
        completed=True
    ).count()

    # =================================================
    # COURSE PROGRESS
    # =================================================

    if total_lessons > 0:

        course_progress = int(
            (
                completed_lessons
                / total_lessons
            ) * 100
        )

    else:

        course_progress = 0

    # =================================================
    # QUIZ STATUS
    # =================================================

    quizzes = Quiz.objects.filter(
        course=lesson.course
    )

    quiz_passed = False

    for quiz in quizzes:

        attempts = QuizAttempt.objects.filter(
            quiz=quiz,
            student=request.user
        )

        for attempt in attempts:

            if attempt.total_questions > 0:

                percentage = int(
                    (attempt.score / attempt.total_questions) * 100
                )

                if percentage >= 50:

                    quiz_passed = True
                    break

        if quiz_passed:

            break

    # =================================================
    # COURSE COMPLETED
    # =================================================

    course_completed = (
        total_lessons > 0
        and completed_lessons == total_lessons
        and quiz_passed
    )

    return render(
        request,
        "lessons/lesson_detail.html",
        {
            "lesson": lesson,
            "progress": progress,
            "previous_lesson": previous_lesson,
            "next_lesson": next_lesson,
            "total_lessons": total_lessons,
            "completed_lessons": completed_lessons,
            "course_progress": course_progress,
            "course_completed": course_completed,
            "quiz_passed": quiz_passed,
        }
    )


# =====================================================
# MARK LESSON COMPLETE
# =====================================================

@login_required
def mark_complete(request, lesson_id):

    # =================================================
    # ONLY POST REQUESTS
    # =================================================

    if request.method != "POST":

        return redirect(
            "lesson_detail",
            lesson_id=lesson_id
        )

    # =================================================
    # GET LESSON
    # =================================================

    lesson = get_object_or_404(
        Lesson,
        id=lesson_id
    )

    # =================================================
    # CHECK ENROLLMENT
    # =================================================

    is_enrolled = Enrollment.objects.filter(
        student=request.user,
        course=lesson.course
    ).exists()

    if not is_enrolled:

        return redirect(
            "course_detail",
            course_id=lesson.course.id
        )

    # =================================================
    # CREATE OR GET LESSON PROGRESS
    # =================================================

    progress, created = LessonProgress.objects.get_or_create(
        student=request.user,
        lesson=lesson
    )

    # =================================================
    # MARK LESSON COMPLETED
    # =================================================

    progress.completed = True
    progress.completed_at = timezone.now()

    progress.save()

    # =================================================
    # CHECK COURSE LESSON COMPLETION
    # =================================================

    total_lessons = Lesson.objects.filter(
        course=lesson.course
    ).count()

    completed_lessons = LessonProgress.objects.filter(
        student=request.user,
        lesson__course=lesson.course,
        completed=True
    ).count()

    lessons_completed = (
        total_lessons > 0
        and completed_lessons == total_lessons
    )

    # =================================================
    # CHECK QUIZ
    # =================================================

    quizzes = Quiz.objects.filter(
        course=lesson.course
    )

    quiz_exists = quizzes.exists()

    quiz_passed = False

    for quiz in quizzes:

        attempts = QuizAttempt.objects.filter(
            quiz=quiz,
            student=request.user
        )

        for attempt in attempts:

            if attempt.total_questions > 0:

                percentage = int(
                    (attempt.score / attempt.total_questions) * 100
                )

                # Passing percentage = 50%

                if percentage >= 50:

                    quiz_passed = True
                    break

        if quiz_passed:

            break

    # =================================================
    # FINAL COURSE COMPLETION CHECK
    # =================================================

    if quiz_exists:

        course_completed = (
            lessons_completed
            and quiz_passed
        )

    else:

        course_completed = lessons_completed

    # =================================================
    # GENERATE CERTIFICATE
    # =================================================

    if course_completed:

        certificate, created = Certificate.objects.get_or_create(
            student=request.user,
            course=lesson.course
        )

        if created:

            messages.success(
                request,
                "🎉 Congratulations! You completed the course and earned a certificate!"
            )

        else:

            messages.success(
                request,
                "🎉 Course completed! Your certificate is already available."
            )

    else:

        if lessons_completed and quiz_exists and not quiz_passed:

            messages.success(
                request,
                "All lessons completed! Please pass the quiz to complete the course."
            )

        else:

            messages.success(
                request,
                "Lesson completed successfully!"
            )

    # =================================================
    # RETURN TO LESSON
    # =================================================

    return redirect(
        "lesson_detail",
        lesson_id=lesson.id
    )