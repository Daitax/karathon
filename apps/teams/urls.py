from django.urls import path

from . import views

app_name = 'teams'


urlpatterns = [
    path('', views.index, name='team-index'),
    path('add-desire/', views.add_desire, name='add-desire'),
]
