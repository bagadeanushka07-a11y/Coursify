from django.contrib import admin
from .models import Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "instructor",
        "price",
        "level",
        "duration",
        "created_at",
    )

    list_filter = (
        "category",
        "level",
    )

    search_fields = (
        "title",
        "description",
    )