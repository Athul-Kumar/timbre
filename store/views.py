from django.views.decorators.cache import never_cache
from unicodedata import category
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from category.models import Category
from carts .models import Cartitem, Cart
from carts.views import _cart_id
from  .models import Product




@never_cache
def store(request, category_slug=None):
    categories = None
    products = None
    if category_slug !=None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter( category_id=categories, is_available=True)

    else:
        products = Product.objects.all().filter(is_available=True)
    context={
        'products': products
    }

    return render(request, 'store/store.html', context)



@never_cache
def product_detail(request, category_slug, product_slug):

    try:
        single_product = Product.objects.get(category_id__slug = category_slug, slug=product_slug)
        in_cart = Cartitem.objects.filter(cart_id__cart_id = _cart_id(request), product_id = single_product).exists()
        

    except Exception as e:
        raise e

    context={
        'single_product': single_product,
        'in_cart': in_cart,

    }
    return render(request, 'store/product_detail.html', context)

