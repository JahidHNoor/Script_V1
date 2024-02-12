from django.urls import path
from user_app.views import *


urlpatterns = [
    path('dashboard', dashboard , name='dashboard'),
    path('rps', rps , name='rps'),
    path('profile', profile , name='profile'),
    path('settings', settings , name='settings'),
    path('history', history , name='history'),
]
