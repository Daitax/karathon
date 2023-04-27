from django.urls import path
from django.views.generic.base import TemplateView

from . import views

app_name = "core"

urlpatterns = [
    path(
        "",
        TemplateView.as_view(template_name="core/index.html"),
        name="site-index",
    ),
    path(
        "about_karachunia",
        TemplateView.as_view(template_name="core/about_karachunia.html"),
        name="about_karachunia",
    ),
    path("participate/", views.participate, name="participate"),
    path("karathons/", views.about_karathons, name="about_karathons"),
    path(
        "karathons/<int:karathon_number>-karathon/",
        views.karathon,
        name="karathon",
    ),
    path(
        "privacy_policy",
        TemplateView.as_view(template_name="core/privacy_policy.html"),
        name="privacy_policy",
    ),
]
