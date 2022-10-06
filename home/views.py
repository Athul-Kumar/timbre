from django.shortcuts import render, redirect
from store .models import Product
# from django.http import HttpResponse
# Create your views here.



def homepage(request):

    product = Product.objects.all().filter(is_available=True)
    context = {
        'product': product
    }
    return render(request, 'index.html', context)
    
   