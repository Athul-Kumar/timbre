from django.urls import path
from . import views



urlpatterns = [
    path('register/', views.user_register, name = 'register'),
    path('', views.user_login, name = 'login'),
    path('logout/', views.user_logout, name = 'logout'),
    path('verify_loginotp/',views.verify_loginotp,name='verify_loginotp'),
    path('otplogin', views.loginotp, name='otplogin'),
    path('verify/', views.verify_code ,name='verify'),
    
]