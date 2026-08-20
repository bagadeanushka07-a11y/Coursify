from django.urls import path
from . import views


urlpatterns = [

    # Student
    path(
        "",
        views.course_list,
        name="course_list"
    ),

    path(
        "<int:course_id>/",
        views.course_detail,
        name="course_detail"
    ),


    # Instructor
    path(
        "instructor/",
        views.instructor_dashboard,
        name="instructor_dashboard"
    ),

    path(
        "instructor/add/",
        views.add_course,
        name="add_course"
    ),

    path(
        "instructor/edit/<int:course_id>/",
        views.edit_course,
        name="edit_course"
    ),

    path(
        "instructor/delete/<int:course_id>/",
        views.delete_course,
        name="delete_course"
    ),

    path(
    "instructor/analytics/",
    views.instructor_analytics,
    name="instructor_analytics"
    ),

]