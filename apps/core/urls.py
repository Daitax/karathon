from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.index, name="site-index"),
    path(
        "about_karachunia",
        views.AboutKarachuniaView.as_view(),
        name="about_karachunia",
    ),
    path("participate/", views.participate, name="participate"),
    path("karathons/", views.about_karathons, name="about_karathons"),
    path(
        "karathons/<int:karathon_number>-karathon/",
        views.karathon,
        name="karathon",
    ),
]
