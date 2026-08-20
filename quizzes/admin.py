from django.contrib import admin

from .models import Quiz, Question, QuizAttempt


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "course",
        "created_at",
    )

    list_filter = (
        "course",
    )

    search_fields = (
        "title",
        "course__title",
    )


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):

    list_display = (
        "question_text",
        "quiz",
        "correct_answer",
    )

    list_filter = (
        "quiz",
        "correct_answer",
    )

    search_fields = (
        "question_text",
        "quiz__title",
    )


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):

    list_display = (
        "student",
        "quiz",
        "score",
        "total_questions",
        "attempted_at",
    )

    list_filter = (
        "quiz",
        "attempted_at",
    )

    search_fields = (
        "student__username",
        "quiz__title",
    )