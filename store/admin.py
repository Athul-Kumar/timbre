from django.contrib import admin

from store.forms import BrandForm
from .models import Product, Brandinfo

# Register your models here.

class ProductAdmin(admin.ModelAdmin):

    prepopulated_fields = {'slug': ('product_name',)}
    list_display=['product_name', 'description', 'pro_images', 'stock', 'is_available']



class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('brand_name',)}
    list_display= ['brand_name', 'brand_images', 'description', 'total_products', 'is_available']



admin.site.register(Product, ProductAdmin)
admin.site.register(Brandinfo, BrandAdmin)
