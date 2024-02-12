from django.urls import path
from tic_tac_toe.views import *


urlpatterns = [
    path('tic_tac_toe', tic_tac_toe , name='tic_tac_toe'),
    path('tic_tac_toe/game/<str:username>/<int:id>/', tic_tac_toe2 , name='tic_tac_toe2'),
]
