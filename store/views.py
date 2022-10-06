from unicodedata import category
from django.shortcuts import get_object_or_404, render, redirect
from category.models import Category
from  .models import Product


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


def product_detail(request, category_slug, product_slug):

    try:
        single_product = Product.objects.get(category_id__slug = category_slug, slug=product_slug)

    except Exception as e:
        raise e

    context={
        'single_product': single_product

    }
    return render(request, 'store/product_detail.html', context)