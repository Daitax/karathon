from django.urls import path

from . import views

app_name = 'steps'

urlpatterns = [
    path('addreport/', views.add_report, name='add-report'),
]
