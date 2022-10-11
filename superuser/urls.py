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
   # path('specifications/', views.admin_product_specifications, name="specifications"),
   path('brandlist/', views.admin_brandlist, name="brandlist"),
   path('brand-delete/<int:id>', views.admin_brand_delete, name="brand-delete"), 
   path('brand-add/', views.admin_brand_add, name="brand-add"),
   path('order-detail/', views.admin_orders_list, name="order-detail"),
   path('update_admin_order/<str:id>', views.update_admin_order, name="update_admin_order") ,
   
  
]