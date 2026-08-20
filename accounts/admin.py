from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    fieldsets = UserAdmin.fieldsets + (
        (
            "Coursify Information",
            {
                "fields": (
                    "role",
                    "profile_picture",
                    "phone_number",
                )
            }
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Coursify Information",
            {
                "fields": (
                    "role",
                    "profile_picture",
                    "phone_number",
                )
            }
        ),
    )