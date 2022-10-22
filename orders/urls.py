from django.urls import path, include
from . import views

urlpatterns = [
   
    path('place_order', views.place_order, name="place_order"),
    path('payments/', views.payments, name="payments"),
    path('cash_on_delivery/<int:id>', views.cash_on_delivery, name="cash_on_delivery"),
    path('order_complete/', views.order_complete, name="order_complete"),
    path('razor_pay', views.razor_pay,name="razor_pay"),
   
]