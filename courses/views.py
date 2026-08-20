from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from quizzes.models import Quiz, QuizAttempt
from .models import Course
from .forms import CourseForm
from enrollments.models import Enrollment
from lessons.models import Lesson, LessonProgress
from quizzes.models import QuizAttempt
from enrollments.models import Enrollment
from lessons.models import Lesson, LessonProgress
from django.db.models import Count, Avg, Q

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


def course_list(request):
    courses = Course.objects.select_related(
        "category",
        "instructor"
    ).all()

    return render(
        request,
        "courses/course_list.html",
        {
            "courses": courses
        }
    )


def course_detail(request, course_id):
    course = get_object_or_404(
        Course.objects.select_related(
            "category",
            "instructor"
        ),
        id=course_id
    )

    return render(
        request,
        "courses/course_detail.html",
        {
            "course": course
        }
    )


@instructor_required
def instructor_dashboard(request):

    courses = Course.objects.filter(
        instructor=request.user
    ).select_related(
        "category"
    ).order_by(
        "-created_at"
    )

    total_courses = courses.count()

    total_students = Enrollment.objects.filter(
        course__instructor=request.user
    ).values(
        "student"
    ).distinct().count()

    total_lessons = Lesson.objects.filter(
        course__instructor=request.user
    ).count()

    for course in courses:

        student_count = Enrollment.objects.filter(
            course=course
        ).values(
            "student"
        ).distinct().count()

        lesson_count = Lesson.objects.filter(
            course=course
        ).count()

        completed_lessons = LessonProgress.objects.filter(
            lesson__course=course,
            completed=True
        ).count()

        total_possible_completions = (
            student_count * lesson_count
        )

        if total_possible_completions > 0:
            completion_percentage = int(
                (
                    completed_lessons
                    / total_possible_completions
                ) * 100
            )
        else:
            completion_percentage = 0

        course.student_count = student_count
        course.lesson_count = lesson_count
        course.completed_lessons = completed_lessons
        course.completion_percentage = completion_percentage

    return render(
        request,
        "courses/instructor_dashboard.html",
        {
            "courses": courses,
            "total_courses": total_courses,
            "total_students": total_students,
            "total_lessons": total_lessons,
        }
    )


@instructor_required
def add_course(request):

    if request.method == "POST":

        form = CourseForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            course = form.save(commit=False)
            course.instructor = request.user
            course.save()

            messages.success(
                request,
                "Course created successfully!"
            )

            return redirect(
                "instructor_dashboard"
            )

    else:
        form = CourseForm()

    return render(
        request,
        "courses/course_form.html",
        {
            "form": form,
            "page_title": "Create Course",
            "button_text": "Create Course"
        }
    )


@instructor_required
def edit_course(request, course_id):

    course = get_object_or_404(
        Course,
        id=course_id,
        instructor=request.user
    )

    if request.method == "POST":

        form = CourseForm(
            request.POST,
            request.FILES,
            instance=course
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Course updated successfully!"
            )

            return redirect(
                "instructor_dashboard"
            )

    else:

        form = CourseForm(
            instance=course
        )

    return render(
        request,
        "courses/course_form.html",
        {
            "form": form,
            "course": course,
            "page_title": "Edit Course",
            "button_text": "Save Changes"
        }
    )


@instructor_required
def instructor_dashboard(request):

    # =====================================================
    # INSTRUCTOR COURSES
    # =====================================================

    courses = Course.objects.filter(
        instructor=request.user
    ).select_related(
        "category"
    ).order_by(
        "-created_at"
    )

    # =====================================================
    # BASIC STATISTICS
    # =====================================================

    total_courses = courses.count()

    total_lessons = Lesson.objects.filter(
        course__instructor=request.user
    ).count()

    total_students = Enrollment.objects.filter(
        course__instructor=request.user
    ).values(
        "student"
    ).distinct().count()

    total_enrollments = Enrollment.objects.filter(
        course__instructor=request.user
    ).count()

    # =====================================================
    # COMPLETED ENROLLMENTS
    # =====================================================

    completed_enrollments = 0

    for enrollment in Enrollment.objects.filter(
        course__instructor=request.user
    ):

        total_lessons_for_course = Lesson.objects.filter(
            course=enrollment.course
        ).count()

        completed_lessons_for_student = LessonProgress.objects.filter(
            student=enrollment.student,
            lesson__course=enrollment.course,
            completed=True
        ).count()

        if (
            total_lessons_for_course > 0
            and
            completed_lessons_for_student
            == total_lessons_for_course
        ):
            completed_enrollments += 1

    # =====================================================
    # OVERALL COMPLETION PERCENTAGE
    # =====================================================

    if total_enrollments > 0:

        average_completion = int(
            (
                completed_enrollments
                / total_enrollments
            ) * 100
        )

    else:

        average_completion = 0

    # =====================================================
    # COURSE ANALYTICS
    # =====================================================

    course_analytics = []

    for course in courses:

        # -------------------------------------------------
        # Students
        # -------------------------------------------------

        student_count = Enrollment.objects.filter(
            course=course
        ).values(
            "student"
        ).distinct().count()

        # -------------------------------------------------
        # Lessons
        # -------------------------------------------------

        lesson_count = Lesson.objects.filter(
            course=course
        ).count()

        # -------------------------------------------------
        # Completed lessons
        # -------------------------------------------------

        completed_lessons = LessonProgress.objects.filter(
            lesson__course=course,
            completed=True
        ).count()

        # -------------------------------------------------
        # Possible lesson completions
        # -------------------------------------------------

        total_possible = (
            student_count
            * lesson_count
        )

        # -------------------------------------------------
        # Course completion
        # -------------------------------------------------

        if total_possible > 0:

            completion_percentage = int(
                (
                    completed_lessons
                    / total_possible
                ) * 100
            )

        else:

            completion_percentage = 0

        # -------------------------------------------------
        # Quiz attempts
        # -------------------------------------------------

        quiz_attempts = QuizAttempt.objects.filter(
            quiz__course=course
        ).count()

        # -------------------------------------------------
        # Average quiz score
        # -------------------------------------------------

        quiz_attempts_list = QuizAttempt.objects.filter(
            quiz__course=course
        )

        total_score = 0
        total_questions = 0

        for attempt in quiz_attempts_list:

            total_score += attempt.score
            total_questions += attempt.total_questions

        if total_questions > 0:

            average_quiz_score = int(
                (
                    total_score
                    / total_questions
                ) * 100
            )

        else:

            average_quiz_score = 0

        # -------------------------------------------------
        # Store analytics
        # -------------------------------------------------

        course_analytics.append(
            {
                "course": course,
                "student_count": student_count,
                "lesson_count": lesson_count,
                "completed_lessons": completed_lessons,
                "completion_percentage": completion_percentage,
                "quiz_attempts": quiz_attempts,
                "average_quiz_score": average_quiz_score,
            }
        )

    # =====================================================
    # CHART DATA
    # =====================================================

    chart_labels = []
    chart_students = []
    chart_completion = []
    chart_quiz_scores = []

    for item in course_analytics:

        chart_labels.append(
            item["course"].title
        )

        chart_students.append(
            item["student_count"]
        )

        chart_completion.append(
            item["completion_percentage"]
        )

        chart_quiz_scores.append(
            item["average_quiz_score"]
        )

    # =====================================================
    # DASHBOARD
    # =====================================================

    return render(
        request,
        "courses/instructor_dashboard.html",
        {
            "courses": courses,

            # Basic statistics
            "total_courses": total_courses,
            "total_students": total_students,
            "total_lessons": total_lessons,
            "total_enrollments": total_enrollments,
            "completed_enrollments": completed_enrollments,
            "average_completion": average_completion,

            # Course analytics
            "course_analytics": course_analytics,

            # Chart data
            "chart_labels": chart_labels,
            "chart_students": chart_students,
            "chart_completion": chart_completion,
            "chart_quiz_scores": chart_quiz_scores,
        }
    )

# =====================================================
# INSTRUCTOR ANALYTICS
# =====================================================

# =========================================================
# INSTRUCTOR ROLE CHECK
# =========================================================

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


# =========================================================
# INSTRUCTOR ANALYTICS
# =========================================================

@instructor_required
def instructor_analytics(request):

    # =====================================================
    # GET INSTRUCTOR COURSES
    # =====================================================

    courses = Course.objects.filter(
        instructor=request.user
    ).order_by(
        "title"
    )

    # =====================================================
    # COURSE FILTER
    # =====================================================

    selected_course_id = request.GET.get("course")

    selected_course = None

    if selected_course_id:

        selected_course = get_object_or_404(
            Course,
            id=selected_course_id,
            instructor=request.user
        )

        analytics_courses = courses.filter(
            id=selected_course.id
        )

    else:

        analytics_courses = courses

    # =====================================================
    # BASIC COURSE STATISTICS
    # =====================================================

    total_courses = analytics_courses.count()

    total_lessons = Lesson.objects.filter(
        course__in=analytics_courses
    ).count()

    # =====================================================
    # TOTAL STUDENTS
    # =====================================================

    total_students = Enrollment.objects.filter(
        course__in=analytics_courses
    ).values(
        "student"
    ).distinct().count()

    # =====================================================
    # COMPLETED LESSONS
    # =====================================================

    completed_lessons = LessonProgress.objects.filter(
        lesson__course__in=analytics_courses,
        completed=True
    ).count()

    # =====================================================
    # OVERALL POSSIBLE LESSON COMPLETIONS
    # =====================================================

    total_possible_completions = 0

    for course in analytics_courses:

        student_count = Enrollment.objects.filter(
            course=course
        ).values(
            "student"
        ).distinct().count()

        lesson_count = Lesson.objects.filter(
            course=course
        ).count()

        total_possible_completions += (
            student_count * lesson_count
        )

    # =====================================================
    # OVERALL COMPLETION
    # =====================================================

    if total_possible_completions > 0:

        overall_completion = int(
            (
                completed_lessons
                / total_possible_completions
            ) * 100
        )

    else:

        overall_completion = 0

    overall_completion = min(
        max(overall_completion, 0),
        100
    )

    # =====================================================
    # COURSE PERFORMANCE
    # =====================================================

    course_analytics = []

    for course in analytics_courses:

        # -------------------------------------------------
        # Students
        # -------------------------------------------------

        student_count = Enrollment.objects.filter(
            course=course
        ).values(
            "student"
        ).distinct().count()

        # -------------------------------------------------
        # Lessons
        # -------------------------------------------------

        lesson_count = Lesson.objects.filter(
            course=course
        ).count()

        # -------------------------------------------------
        # Completed lessons
        # -------------------------------------------------

        completed_count = LessonProgress.objects.filter(
            lesson__course=course,
            completed=True
        ).count()

        # -------------------------------------------------
        # Possible completions
        # -------------------------------------------------

        total_possible = (
            student_count * lesson_count
        )

        # -------------------------------------------------
        # Completion percentage
        # -------------------------------------------------

        if total_possible > 0:

            completion_percentage = int(
                (
                    completed_count
                    / total_possible
                ) * 100
            )

        else:

            completion_percentage = 0

        completion_percentage = min(
            max(completion_percentage, 0),
            100
        )

        # -------------------------------------------------
        # Quiz count
        # -------------------------------------------------

        quiz_count = Quiz.objects.filter(
            course=course
        ).count()

        # -------------------------------------------------
        # Quiz attempts
        # -------------------------------------------------

        quiz_attempt_count = QuizAttempt.objects.filter(
            quiz__course=course
        ).count()

        # -------------------------------------------------
        # Course analytics
        # -------------------------------------------------

        course_analytics.append(
            {
                "course": course,
                "student_count": student_count,
                "lesson_count": lesson_count,
                "completed_lessons": completed_count,
                "completion_percentage": completion_percentage,
                "quiz_count": quiz_count,
                "quiz_attempt_count": quiz_attempt_count,
            }
        )

    # =====================================================
    # QUIZ ANALYTICS
    # =====================================================

    quizzes = Quiz.objects.filter(
        course__in=analytics_courses
    ).select_related(
        "course"
    ).order_by(
        "course__title",
        "title"
    )

    total_quizzes = quizzes.count()

    # =====================================================
    # ALL QUIZ ATTEMPTS
    # =====================================================

    quiz_attempts = QuizAttempt.objects.filter(
        quiz__course__in=analytics_courses
    )

    total_quiz_attempts = quiz_attempts.count()

    # =====================================================
    # UNIQUE QUIZ STUDENTS
    # =====================================================

    quiz_students = quiz_attempts.values(
        "student"
    ).distinct().count()

    # =====================================================
    # OVERALL AVERAGE RAW SCORE
    # =====================================================

    average_score_data = quiz_attempts.aggregate(
        average_score=Avg("score")
    )

    overall_average_score = (
        average_score_data["average_score"]
        or 0
    )

    # =====================================================
    # OVERALL QUIZ PERCENTAGE
    # =====================================================

    overall_percentage_values = []

    for attempt in quiz_attempts:

        if attempt.total_questions > 0:

            percentage_value = (
                attempt.score
                / attempt.total_questions
            ) * 100

            overall_percentage_values.append(
                percentage_value
            )

    if overall_percentage_values:

        overall_quiz_percentage = int(
            sum(overall_percentage_values)
            / len(overall_percentage_values)
        )

    else:

        overall_quiz_percentage = 0

    overall_quiz_percentage = min(
        max(overall_quiz_percentage, 0),
        100
    )

    # =====================================================
    # OVERALL PASS RATE
    #
    # 50% OR HIGHER = PASSED
    # =====================================================

    overall_passed_attempts = 0

    for attempt in quiz_attempts:

        if attempt.total_questions > 0:

            attempt_percentage = (
                attempt.score
                / attempt.total_questions
            ) * 100

            if attempt_percentage >= 50:

                overall_passed_attempts += 1

    if total_quiz_attempts > 0:

        overall_pass_rate = int(
            (
                overall_passed_attempts
                / total_quiz_attempts
            ) * 100
        )

    else:

        overall_pass_rate = 0

    overall_pass_rate = min(
        max(overall_pass_rate, 0),
        100
    )

    # =====================================================
    # INDIVIDUAL QUIZ PERFORMANCE
    # =====================================================

    quiz_analytics = []

    for quiz in quizzes:

        attempts = QuizAttempt.objects.filter(
            quiz=quiz
        )

        attempt_count = attempts.count()

        # -------------------------------------------------
        # Unique students
        # -------------------------------------------------

        unique_students = attempts.values(
            "student"
        ).distinct().count()

        # -------------------------------------------------
        # Average raw score
        # -------------------------------------------------

        quiz_average_score_data = attempts.aggregate(
            average_score=Avg("score")
        )

        quiz_average_score = (
            quiz_average_score_data["average_score"]
            or 0
        )

        # -------------------------------------------------
        # Average percentage
        # -------------------------------------------------

        percentage_values = []

        for attempt in attempts:

            if attempt.total_questions > 0:

                attempt_percentage = (
                    attempt.score
                    / attempt.total_questions
                ) * 100

                percentage_values.append(
                    attempt_percentage
                )

        if percentage_values:

            percentage = int(
                sum(percentage_values)
                / len(percentage_values)
            )

        else:

            percentage = 0

        # -------------------------------------------------
        # Passed attempts
        # -------------------------------------------------

        passed_attempts = 0

        for attempt in attempts:

            if attempt.total_questions > 0:

                attempt_percentage = (
                    attempt.score
                    / attempt.total_questions
                ) * 100

                if attempt_percentage >= 50:

                    passed_attempts += 1

        # -------------------------------------------------
        # Pass rate
        # -------------------------------------------------

        if attempt_count > 0:

            pass_rate = int(
                (
                    passed_attempts
                    / attempt_count
                ) * 100
            )

        else:

            pass_rate = 0

        # -------------------------------------------------
        # Failed attempts
        # -------------------------------------------------

        failed_attempts = (
            attempt_count
            - passed_attempts
        )

        # -------------------------------------------------
        # Add quiz analytics
        # -------------------------------------------------

        quiz_analytics.append(
            {
                "quiz": quiz,
                "attempt_count": attempt_count,
                "unique_students": unique_students,
                "average_score": round(
                    quiz_average_score,
                    1
                ),
                "percentage": percentage,
                "passed_attempts": passed_attempts,
                "failed_attempts": failed_attempts,
                "pass_rate": pass_rate,
            }
        )

    # =====================================================
    # STUDENT PERFORMANCE ANALYTICS
    # =====================================================

    student_enrollments = Enrollment.objects.filter(
        course__in=analytics_courses
    ).select_related(
        "student",
        "course"
    )

    student_ids = student_enrollments.values_list(
        "student_id",
        flat=True
    ).distinct()

    student_performance = []

    for student_id in student_ids:

        # -------------------------------------------------
        # Get student
        # -------------------------------------------------

        student = student_enrollments.filter(
            student_id=student_id
        ).first().student

        # -------------------------------------------------
        # Student's enrolled courses
        # -------------------------------------------------

        enrolled_course_ids = list(
            Enrollment.objects.filter(
                student=student,
                course__in=analytics_courses
            ).values_list(
                "course_id",
                flat=True
            )
        )

        enrolled_course_count = len(
            enrolled_course_ids
        )

        # -------------------------------------------------
        # Total lessons available to student
        # -------------------------------------------------

        total_student_lessons = Lesson.objects.filter(
            course_id__in=enrolled_course_ids
        ).count()

        # -------------------------------------------------
        # Completed lessons
        # -------------------------------------------------

        completed_student_lessons = LessonProgress.objects.filter(
            student=student,
            lesson__course_id__in=enrolled_course_ids,
            completed=True
        ).count()

        # -------------------------------------------------
        # Lesson completion percentage
        # -------------------------------------------------

        if total_student_lessons > 0:

            lesson_completion = int(
                (
                    completed_student_lessons
                    / total_student_lessons
                ) * 100
            )

        else:

            lesson_completion = 0

        lesson_completion = min(
            max(lesson_completion, 0),
            100
        )

        # -------------------------------------------------
        # Quiz attempts
        # -------------------------------------------------

        student_attempts = QuizAttempt.objects.filter(
            student=student,
            quiz__course__in=analytics_courses
        )

        attempt_count = student_attempts.count()

        # -------------------------------------------------
        # Quiz score
        # -------------------------------------------------

        student_score = 0
        student_total_questions = 0

        for attempt in student_attempts:

            student_score += attempt.score

            student_total_questions += (
                attempt.total_questions
            )

        if student_total_questions > 0:

            quiz_percentage = round(
                (
                    student_score
                    / student_total_questions
                ) * 100,
                1
            )

        else:

            quiz_percentage = 0

        quiz_percentage = min(
            max(quiz_percentage, 0),
            100
        )

        # -------------------------------------------------
        # Completed courses
        # -------------------------------------------------

        completed_courses = 0

        for course_id in enrolled_course_ids:

            course_lessons = Lesson.objects.filter(
                course_id=course_id
            ).count()

            completed_course_lessons = LessonProgress.objects.filter(
                student=student,
                lesson__course_id=course_id,
                completed=True
            ).count()

            if (
                course_lessons > 0
                and completed_course_lessons == course_lessons
            ):

                completed_courses += 1

        # -------------------------------------------------
        # Course completion percentage
        # -------------------------------------------------

        if enrolled_course_count > 0:

            course_completion = int(
                (
                    completed_courses
                    / enrolled_course_count
                ) * 100
            )

        else:

            course_completion = 0

        course_completion = min(
            max(course_completion, 0),
            100
        )

        # -------------------------------------------------
        # Add student analytics
        # -------------------------------------------------

        student_performance.append(
            {
                "student": student,
                "course_count": enrolled_course_count,
                "completed_courses": completed_courses,
                "lesson_completion": lesson_completion,
                "quiz_attempts": attempt_count,
                "quiz_percentage": quiz_percentage,
                "course_completion": course_completion,
            }
        )

    # =====================================================
    # CONTEXT
    # =====================================================

    context = {

        # -------------------------------------------------
        # Course analytics
        # -------------------------------------------------

        "courses": courses,

        "course_analytics": course_analytics,

        "selected_course": selected_course,

        "total_courses": total_courses,

        "total_students": total_students,

        "total_lessons": total_lessons,

        "completed_lessons": completed_lessons,

        "overall_completion": overall_completion,

        # -------------------------------------------------
        # Quiz analytics
        # -------------------------------------------------

        "quizzes": quizzes,

        "quiz_analytics": quiz_analytics,

        "total_quizzes": total_quizzes,

        "total_quiz_attempts": total_quiz_attempts,

        "quiz_students": quiz_students,

        "average_score": round(
            overall_average_score,
            1
        ),

        "overall_quiz_percentage": (
            overall_quiz_percentage
        ),

        "overall_passed_attempts": (
            overall_passed_attempts
        ),

        "overall_pass_rate": (
            overall_pass_rate
        ),

        # -------------------------------------------------
        # Student analytics
        # -------------------------------------------------

        "student_performance": (
            student_performance
        ),
    }

    # =====================================================
    # RENDER
    # =====================================================

    return render(
        request,
        "courses/instructor_analytics.html",
        context
    )

# =====================================================
# DELETE COURSE
# =====================================================

@instructor_required
def delete_course(request, course_id):

    course = get_object_or_404(
        Course,
        id=course_id,
        instructor=request.user
    )

    if request.method == "POST":

        course.delete()

        messages.success(
            request,
            "Course deleted successfully!"
        )

        return redirect(
            "instructor_dashboard"
        )

    return render(
        request,
        "courses/course_confirm_delete.html",
        {
            "course": course
        }
    )