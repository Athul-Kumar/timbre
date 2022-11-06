from django.urls import path
from . import views

urlpatterns = [
   path('', views.admin_login, name="admin_login"),
   path('dashboard/', views.admin_home, name="dashboard"),
   path('logout/', views.admin_logout, name="admin_logout"),
   path('userlist/', views.userlist, name="userlist"),
   path('userblock/<int:id>/<int:flag>',views.userblock, name="userblock"),
   path('categorylist/',views.admin_category, name="categorylist"),
   path('category_delete/<int:id>',views.admin_category_delete, name="category_delete"),
   path('category-add/', views.admin_category_add, name="category-add"),
   path('productlist/', views.admin_productlist, name="productlist"),
   path('product-add/', views.admin_product_add, name="product-add"),
   path('product_delete/<int:id>',views.admin_product_delete, name="product_delete"),
   path('brandlist/', views.admin_brandlist, name="brandlist"),
   path('brand-delete/<int:id>', views.admin_brand_delete, name="brand-delete"), 
   path('brand-add/', views.admin_brand_add, name="brand-add"),
   path('order-detail/', views.admin_orderlist, name="order-detail"),
   path('order-update/<str:id>', views.admin_order_update, name="order-update"),
   
   path('coupon_list/', views.admin_display_coupon, name="coupon_list"),
   path('coupon_add',views.admin_add_coupon,name='admin_add_coupon'),
   path('admin_display_coupon',views.admin_display_coupon,name='admin_display_coupon'),
   path("coupon_delete/<int:id>",views.coupon_delete,name='coupon_delete'),
   path("coupon_update/<int:id>",views.coupon_update,name='coupon_update'),
   path("product_offer",views.product_offer,name='product_offer'),
   path("add-product-offer",views.add_product_offer,name='add-product-offer'),
   path("product_offer_delete/<int:id>",views.product_offer_delete,name='product_offer_delete'),
   path("category_offer",views.category_offer,name='category_offer'),
   path("add-category-offer",views.add_category_offer,name='add-category-offer'),
   path("category_offer_delete/<int:id>",views.category_offer_delete,name='category_offer_delete'),

   path("sales_report",views.sales_report,name='sales_report'),
   path("sales_report_month/<int:id>",views.sales_report_month,name='sales_report_month'),
   path("sales_report_year/<int:id>",views.sales_report_year,name='sales_report_year')
 
   
   
  
]