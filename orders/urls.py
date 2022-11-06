from django.urls import path, include
from . import views

urlpatterns = [
   
    path('place_order', views.place_order, name="place_order"),
    path('payments/', views.payments, name="payments"),
    path('cash_on_delivery/<int:id>', views.cash_on_delivery, name="cash_on_delivery"),
    path('order_complete/', views.order_complete, name="order_complete"),
    path('razor_pay', views.razor_pay,name="razor_pay"),
    path('user_orders/',views.user_orders,name="user_orders"),
    path("cancel_order/<int:id>",views.cancel_order,name='cancel_order'),
    path("return_order/<int:id>",views.return_order,name='return_order'),
    path("invoice_download/<int:id>",views.invoice_download, name='invoice_download'),
    path('coupon',views.coupon,name="coupon"),
   
]