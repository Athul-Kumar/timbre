from django.contrib import admin

from .models import Payment,Order,OrderProduct,Address
# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display= ['order_number', 'full_name', 'email', 'city', 'order_total', 'status', 'is_ordered']
    list_filter = ['status', 'is_ordered']
    search_fields= ['order_number', 'first_name', 'last_name', 'phone', 'email']
    list_per_page = 20

admin.site.register(Payment)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)
admin.site.register(Address)