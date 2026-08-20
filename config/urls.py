from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect


urlpatterns = [
    path(
        "",
        lambda request: redirect("login")
    ),

    path(
        "admin/",
        admin.site.urls
    ),

    path(
        "",
        include("accounts.urls")
    ),

    path(
        "dashboard/",
        include("dashboard.urls")
    ),

    path(
        "courses/",
        include("courses.urls")
    ),

    path(
        "enrollments/",
        include("enrollments.urls")
    ),

    path(
        "lessons/",
        include("lessons.urls")
    ),

    path(
        "settings/",
        include("user_settings.urls")
    ),

    path(
        "quizzes/",
        include("quizzes.urls")
    ),

    path(
    "certificates/",
    include("certificates.urls")
),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )