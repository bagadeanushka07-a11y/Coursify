from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from courses.models import Course
from .models import Enrollment
from lessons.models import Lesson, LessonProgress


# =====================================================
# ENROLL IN COURSE
# =====================================================

@login_required
def enroll_course(request, course_id):

    # Only students can enroll
    if request.user.role != "student":

        messages.error(
            request,
            "Only students can enroll in courses."
        )

        return redirect(
            "course_detail",
            course_id=course_id
        )

    course = get_object_or_404(
        Course,
        id=course_id
    )

    Enrollment.objects.get_or_create(
        student=request.user,
        course=course
    )

    messages.success(
        request,
        "You have successfully enrolled in the course!"
    )

    return redirect("my_courses")


# =====================================================
# MY COURSES
# =====================================================

@login_required
def my_courses(request):

    enrollments = Enrollment.objects.select_related(
        "course",
        "course__category",
        "course__instructor"
    ).filter(
        student=request.user
    ).order_by(
        "-enrolled_at"
    )

    for enrollment in enrollments:

        # ---------------------------------------------
        # Total lessons
        # ---------------------------------------------

        total_lessons = Lesson.objects.filter(
            course=enrollment.course
        ).count()

        # ---------------------------------------------
        # Completed lessons
        # ---------------------------------------------

        completed_lessons = LessonProgress.objects.filter(
            student=request.user,
            lesson__course=enrollment.course,
            completed=True
        ).count()

        # ---------------------------------------------
        # Progress percentage
        # ---------------------------------------------

        if total_lessons > 0:

            enrollment.progress = int(
                (completed_lessons / total_lessons) * 100
            )

        else:

            enrollment.progress = 0

        # ---------------------------------------------
        # Lesson count
        # ---------------------------------------------

        enrollment.total_lessons = total_lessons
        enrollment.completed_lessons = completed_lessons

        # ---------------------------------------------
        # Course completed?
        # ---------------------------------------------

        enrollment.is_completed = (
            total_lessons > 0
            and completed_lessons == total_lessons
        )

        # ---------------------------------------------
        # Find first incomplete lesson
        # ---------------------------------------------

        completed_lesson_ids = LessonProgress.objects.filter(
            student=request.user,
            lesson__course=enrollment.course,
            completed=True
        ).values_list(
            "lesson_id",
            flat=True
        )

        enrollment.next_lesson = Lesson.objects.filter(
            course=enrollment.course
        ).exclude(
            id__in=completed_lesson_ids
        ).order_by(
            "order"
        ).first()

        # ---------------------------------------------
        # If course completed, use first lesson
        # for review
        # ---------------------------------------------

        if enrollment.next_lesson is None:

            enrollment.review_lesson = Lesson.objects.filter(
                course=enrollment.course
            ).order_by(
                "order"
            ).first()

    return render(
        request,
        "enrollments/my_courses.html",
        {
            "enrollments": enrollments
        }
    )