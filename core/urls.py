from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('', include('home.urls')),
    path('user/', include('user_app.urls')),
    path('user/', include('tic_tac_toe.urls')),
    path('admin/', admin.site.urls),
]


handler404 = 'home.views.error404'
handler500 = 'home.views.error500'
handler403 = 'home.views.error403'