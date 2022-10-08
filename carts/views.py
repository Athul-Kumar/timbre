from logging import exception
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect,get_object_or_404
from  store.models import Product
from .models import Cart, Cartitem
 
# Create your views here.


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        request.session.create()
    return cart

 
def add_cart(request, product_id):

    product = Product.objects.get(id =product_id)    
    #  to get product
    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))
    except  Cart.DoesNotExist:
        cart= Cart.objects.create(
            cart_id = _cart_id(request)
        )
        cart.save()

    try:
        cart_item =Cartitem.objects.get(product_id =product, cart_id = cart)
        cart_item.quantitiy +=1
        cart_item.save()
    except Cartitem.DoesNotExist:
        cart_item = Cartitem.objects.create(
            product_id = product,
            quantitiy = 1,
            cart_id = cart  
            
        )
        cart_item.save()
        
    return redirect('cart')


def cart(request, total =0, quantitiy=0, cart_items=None):
    try:
        cart= Cart.objects.get(cart_id = _cart_id(request))
        # print(cart)
        cart_items= Cartitem.objects.filter(cart_id = cart, is_active = True)
        # print(cart_items)
        for cart_item in cart_items:
            total  += (cart_item.product_id.product_max_price * cart_item.quantitiy)
            # print(total)
            quantitiy+= cart_item.quantitiy
            # print(quantitiy)

    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantitiy': quantitiy,
        'cart_items': cart_items
    }
    
    return render(request, 'store/cart.html', context)

def remove_cart(request, product_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product, id= product_id)
    cart_item = Cartitem.objects.get(product_id =product, cart_id= cart)

    if cart_item.quantitiy > 1:
        cart_item.quantitiy -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

def  delete_cart(request, product_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = Cartitem.objects.get(product_id=product, cart_id = cart)
    cart_item.delete()
    return redirect('cart')