from django.urls import path, include

import apps.teams.views
from . import views

app_name = 'account'

urlpatterns = [
    path('', views.index, name='account-index'),
    path('messages/', views.messages, name='account-messages'),
    path('results/', views.results, name='account-results'),
    path('team/', include('apps.teams.urls')),

    path('authentication/', views.authentication, name='account-authentication'),
    path('logout/', views.user_logout, name='account-logout'),
]
