from django.urls import path
from home.views import *

urlpatterns = [
    path('', home , name='home'),
    path('ref-code/<referral_code>', home , name='home'),
    path('error404', error404 , name='error404'),
    path('error500', error500 , name='error500'),
    path('error403', error403 , name='error403'),
    path('register', register , name='register'),
    path('login', login , name='login'),
    path('logout', logout , name='logout'),
    path('password_reset', password_reset , name='password_reset'),
    path('password_reset/<password_reset_token>', reset_your_password , name='reset_your_password'),
    path('activate_email/<email_token>', activate_email , name='activate_email'),
]
