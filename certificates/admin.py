from django.contrib import admin

from .models import Certificate


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "student",
        "course",
        "issued_at",
    )

    list_filter = (
        "issued_at",
        "course",
    )

    search_fields = (
        "student__username",
        "student__email",
        "course__title",
    )

    ordering = (
        "-issued_at",
    )