from django.urls import path
from . import views



urlpatterns = [
    path('register/', views.user_register, name = 'register'),
    path('', views.user_login, name = 'login'),
    path('logout/', views.user_logout, name = 'logout'),
    path('verify_loginotp/',views.verify_loginotp,name='verify_loginotp'),
    path('otplogin', views.loginotp, name='otplogin'),
    path('verify/', views.verify_code ,name='verify'),



    path('user_dashboard/', views.user_dashboard, name = 'user_dashboard'),
    path('user_details/', views.user_details, name = 'user_details'),
    path('user_detail_update/', views.user_detail_update, name = 'user_detail_update'),
    path('address_list/',views.address_list, name='address_list'),
    path('add_address/',views.add_address,name='add_address'),
    path('delete_address/<int:id>',views.delete_address,name='delete_address'),
    path('update_address/<int:id>',views.update_address,name='update_address'),


    


    
]