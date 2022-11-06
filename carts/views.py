from logging import exception
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,get_object_or_404
from  store.models import Product
from .models import Cart, Cartitem
from orders.models import Address
 
# Create your views here.


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        request.session.create()
    return cart

 
def add_cart(request, product_id):


    user = request.user
    product = Product.objects.get(id =product_id)    
    
    if user.is_authenticated:
        is_cart_item_exists = Cartitem.objects.filter(product_id = product, user=user).exists()
        if is_cart_item_exists:
            cart_item = Cartitem.objects.get(product_id= product, user=user)
            cart_item.quantitiy +=1
            cart_item.save()
        else:
            cart_item = Cartitem.objects.create(
                product_id=product, 
                quantitiy=1,
                user = user
            )
            cart_item.save()
    else:
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
    delivery_charge = 0
    grand_total  =0
    try:
        if request.user.is_authenticated:
            cart_items= Cartitem.objects.filter(user = request.user, is_active = True)
        else:
            cart= Cart.objects.get(cart_id = _cart_id(request))
            cart_items= Cartitem.objects.filter(cart_id = cart, is_active = True)

        for cart_item in cart_items:
            # total  += (cart_item.product_id.product_max_price * cart_item.quantitiy)
            total += int(cart_item.product_id.offer_price())*int(cart_item.quantitiy)
            quantitiy+= cart_item.quantitiy
        
        delivery_charge = 250 if total <= 5000 else 0
        grand_total = total + delivery_charge

    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantitiy': quantitiy,
        'cart_items': cart_items,
        'grand_total': grand_total,
        'delivery_charge': delivery_charge
    }
    
    return render(request, 'store/cart.html', context)


def remove_cart(request, product_id):

    product = get_object_or_404(Product, id= product_id)

    try:
        if request.user.is_authenticated:
            cart_item = Cartitem.objects.get(product_id =product, user= request.user)
        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_item = Cartitem.objects.get(product_id =product, cart_id= cart)

        if cart_item.quantitiy > 1:
            cart_item.quantitiy -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')

def  delete_cart(request, product_id):
    print(product_id)
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = Cartitem.objects.filter(product_id=product, user = request.user)
    else:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_item = Cartitem.objects.get(product_id=product, cart_id = cart)
    cart_item.delete()
    
    return redirect('cart')



#  check Out
@login_required(login_url='login')

def checkout(request, total =0, quantitiy=0, cart_items=None):
    addresses = Address.objects.filter(user  = request.user)
    try:
        if request.user.is_authenticated:
            cart_items= Cartitem.objects.filter(user = request.user, is_active = True)
        else:
            cart= Cart.objects.get(cart_id = _cart_id(request))
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
        'cart_items': cart_items,
        'addresses':addresses,

    }
    
    
    return render (request,'store/checkout.html', context)