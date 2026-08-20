from django.urls import path

from . import views


urlpatterns = [
    path(
        "",
        views.certificate_list,
        name="certificate_list"
    ),

    path(
        "<int:certificate_id>/",
        views.certificate_detail,
        name="certificate_detail"
    ),

    path(
        "<int:certificate_id>/download/",
        views.download_certificate,
        name="download_certificate"
    ),
]