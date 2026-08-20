from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from enrollments.models import Enrollment
from lessons.models import Lesson, LessonProgress
from courses.models import Course
from categories.models import Category


@login_required
def dashboard(request):

    # =====================================================
    # INSTRUCTOR / ADMIN DASHBOARD
    # =====================================================

    if request.user.role in ["instructor", "admin"]:

        courses = Course.objects.filter(
            instructor=request.user
        ).select_related(
            "category"
        ).order_by(
            "-created_at"
        )

        # -------------------------------------------------
        # Instructor Statistics
        # -------------------------------------------------

        total_courses = courses.count()

        total_students = Enrollment.objects.filter(
            course__instructor=request.user
        ).values(
            "student"
        ).distinct().count()

        total_lessons = Lesson.objects.filter(
            course__instructor=request.user
        ).count()

        # -------------------------------------------------
        # Course Analytics
        # -------------------------------------------------

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

        # -------------------------------------------------
        # Instructor Dashboard
        # -------------------------------------------------

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

    # =====================================================
    # STUDENT DASHBOARD
    # =====================================================

    enrollments = Enrollment.objects.select_related(
        "course",
        "course__category",
        "course__instructor"
    ).filter(
        student=request.user
    ).order_by(
        "-enrolled_at"
    )

    # =====================================================
    # BASIC STATISTICS
    # =====================================================

    enrolled_count = enrollments.count()

    completed_lessons_count = LessonProgress.objects.filter(
        student=request.user,
        completed=True
    ).count()

    completed_courses_count = 0

    # =====================================================
    # DASHBOARD COURSES
    # =====================================================

    dashboard_courses = []

    for enrollment in enrollments:

        total_course_lessons = Lesson.objects.filter(
            course=enrollment.course
        ).count()

        completed_course_lessons = LessonProgress.objects.filter(
            student=request.user,
            lesson__course=enrollment.course,
            completed=True
        ).count()

        # =================================================
        # COURSE PROGRESS
        # =================================================

        if total_course_lessons > 0:

            progress = int(
                (
                    completed_course_lessons
                    / total_course_lessons
                ) * 100
            )

        else:

            progress = 0

        enrollment.progress = progress

        enrollment.total_lessons = total_course_lessons

        enrollment.completed_lessons = completed_course_lessons

        # =================================================
        # COURSE COMPLETION
        # =================================================

        enrollment.is_completed = (
            total_course_lessons > 0
            and completed_course_lessons == total_course_lessons
        )

        if enrollment.is_completed:

            completed_courses_count += 1

        # =================================================
        # FIND NEXT LESSON
        # =================================================

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

        # =================================================
        # IF ALL LESSONS COMPLETED
        # SHOW FIRST LESSON FOR REVIEW
        # =================================================

        if enrollment.next_lesson is None:

            enrollment.next_lesson = Lesson.objects.filter(
                course=enrollment.course
            ).order_by(
                "order"
            ).first()

        dashboard_courses.append(enrollment)

    # =====================================================
    # OVERALL LEARNING PROGRESS
    # =====================================================

    total_lessons = Lesson.objects.filter(
        course__enrollments__student=request.user
    ).distinct().count()

    total_completed_lessons = LessonProgress.objects.filter(
        student=request.user,
        completed=True
    ).count()

    if total_lessons > 0:

        overall_progress = int(
            (
                total_completed_lessons
                / total_lessons
            ) * 100
        )

    else:

        overall_progress = 0

    # =====================================================
    # POPULAR COURSES
    # =====================================================

    popular_courses = Course.objects.select_related(
        "category",
        "instructor"
    ).order_by(
        "-created_at"
    )[:3]

    # =====================================================
    # CATEGORIES
    # =====================================================

    categories = Category.objects.all()[:6]

    # =====================================================
    # STUDENT DASHBOARD
    # =====================================================

    return render(
        request,
        "dashboard/dashboard.html",
        {
            "enrollments": dashboard_courses,
            "enrolled_count": enrolled_count,
            "completed_lessons_count": completed_lessons_count,
            "completed_courses_count": completed_courses_count,
            "overall_progress": overall_progress,
            "popular_courses": popular_courses,
            "categories": categories,
        }
    )