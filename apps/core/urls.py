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
    path("champions", views.ChampionsView.as_view(), name="champions"),
    # path("champions", views.champions, name="champions"),
    path(
        "karathons/",
        TemplateView.as_view(template_name="core/about_karathons.html"),
        name="about_karathons",
    ),
    path(
        "karathons/<int:karathon_number>-karathon/",
        views.KarathonView.as_view(),
        name="karathon",
    ),
    path("participate/", views.participate, name="participate"),
    path("participate/webhooks/yookassa/", views.webhooks_yookassa, name="webhooks_yookassa"),
    path("participate/webhooks/paypal/", views.webhooks_paypal, name="webhooks_paypal"),
    # path("participate/", views.ParticipateView.as_view(), name="participate"),
    path(
        "privacy_policy",
        TemplateView.as_view(template_name="core/privacy_policy.html"),
        name="privacy_policy",
    ),
]
