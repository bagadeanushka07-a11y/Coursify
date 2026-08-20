from django.urls import path
from . import views


urlpatterns = [

    # =====================================================
    # STUDENT LESSONS
    # =====================================================

    path(
        "",
        views.lessons_home,
        name="lessons_home"
    ),

    path(
        "course/<int:course_id>/",
        views.lesson_list,
        name="lesson_list"
    ),

    path(
        "<int:lesson_id>/",
        views.lesson_detail,
        name="lesson_detail"
    ),

    path(
        "<int:lesson_id>/complete/",
        views.mark_complete,
        name="mark_complete"
    ),


    # =====================================================
    # INSTRUCTOR LESSON MANAGEMENT
    # =====================================================

    path(
        "manage/<int:course_id>/",
        views.manage_lessons,
        name="manage_lessons"
    ),

    path(
        "manage/<int:course_id>/add/",
        views.add_lesson,
        name="add_lesson"
    ),

    path(
        "manage/edit/<int:lesson_id>/",
        views.edit_lesson,
        name="edit_lesson"
    ),

    path(
        "manage/delete/<int:lesson_id>/",
        views.delete_lesson,
        name="delete_lesson"
    ),

]