from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login_page, name='home'),
    path('registration/', views.registration_page, name='registration'),
    path('logout/', views.user_logout, name='user-logout')
]

