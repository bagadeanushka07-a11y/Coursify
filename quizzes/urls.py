from django.urls import path

from . import views


urlpatterns = [

    # =====================================================
    # QUIZ LIST
    # =====================================================

    path(
        "",
        views.quiz_list,
        name="quiz_list"
    ),

    # =====================================================
    # CREATE QUIZ
    # =====================================================

    path(
        "create/",
        views.create_quiz,
        name="create_quiz"
    ),

    # =====================================================
    # QUIZ ATTEMPTS
    # =====================================================

    path(
        "<int:quiz_id>/attempts/",
        views.quiz_attempts,
        name="quiz_attempts"
    ),

    # =====================================================
    # EDIT QUIZ
    # =====================================================

    path(
        "<int:quiz_id>/edit/",
        views.edit_quiz,
        name="edit_quiz"
    ),

    # =====================================================
    # DELETE QUIZ
    # =====================================================

    path(
        "<int:quiz_id>/delete/",
        views.delete_quiz,
        name="delete_quiz"
    ),

    # =====================================================
    # SUBMIT QUIZ
    # =====================================================

    path(
        "<int:quiz_id>/submit/",
        views.submit_quiz,
        name="submit_quiz"
    ),

    # =====================================================
    # MANAGE QUIZ
    # =====================================================

    path(
        "<int:quiz_id>/manage/",
        views.manage_quiz,
        name="manage_quiz"
    ),

    # =====================================================
    # ADD QUESTION
    # =====================================================

    path(
        "<int:quiz_id>/add-question/",
        views.add_question,
        name="add_question"
    ),

    # =====================================================
    # EDIT QUESTION
    # =====================================================

    path(
        "question/<int:question_id>/edit/",
        views.edit_question,
        name="edit_question"
    ),

    # =====================================================
    # DELETE QUESTION
    # =====================================================

    path(
        "question/<int:question_id>/delete/",
        views.delete_question,
        name="delete_question"
    ),

    # =====================================================
    # QUIZ DETAIL
    #
    # Keep this LAST because <int:quiz_id>/ is general.
    # =====================================================

    path(
        "<int:quiz_id>/",
        views.quiz_detail,
        name="quiz_detail"
    ),
]