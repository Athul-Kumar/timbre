from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from carts.models import Cartitem
from store.models import Product
from .models import Order, Payment, OrderProduct
from .forms import OrderForm
import datetime




# ------------------------------------
# Create your views here.

def payments(request):
   return render(request, 'orders/payment.html')

def place_order(request, total =0, quantitiy =0):
   current_user = request.user
#    if the cart count <0 then redirect to store
   cart_items = Cartitem.objects.filter(user= current_user)
   cart_count = cart_items.count()

   if cart_count <=0:
    return redirect('store')
   grand_total = 0
   delivery_charge = 0

   for cart_item in cart_items:
      total  += (cart_item.product_id.product_max_price * cart_item.quantitiy)
      quantitiy+= cart_item.quantitiy
    
   delivery_charge = 250 if total <= 5000 else 0
   grand_total = total + delivery_charge

   if request.method == 'POST':
      form =  OrderForm(request.POST)
      if form.is_valid():
        #  store all the billing information inside order table

         data = Order()
         data.user = current_user
         data.first_name = form.cleaned_data['first_name']
         data.last_name = form.cleaned_data['last_name']
         data.email = form.cleaned_data['email']
         data.phone = form.cleaned_data['phone']
         data.address_line_1 = form.cleaned_data['address_line_1']
         data.address_line_2 = form.cleaned_data['address_line_2']
         data.country = form.cleaned_data['country']
         data.state = form.cleaned_data['state']
         data.city = form.cleaned_data['city']
         data.order_note = form.cleaned_data['order_note']
         data.order_total = grand_total
         data.delivery_charge = delivery_charge
         data.ip = request.META.get('REMOTE_ADDR')
         data.save()
         #  generate order Number
         # print("pwoli sathanam")
         yr = int(datetime.date.today().strftime('%Y'))
         dt = int(datetime.date.today().strftime('%d'))
         mt = int(datetime.date.today().strftime('%m'))
         d = datetime.date(yr, mt, dt)
         current_date =  d.strftime("%Y%m%d")
         order_number = current_date + str(data.id)
         data.order_number = order_number
         data.save()

         
         order = Order.objects.get(user = current_user, is_ordered = False, order_number=order_number)
         context = {
            'order': order,
            'cart_items': cart_items,
            'total': total,
            'delivery_charge':delivery_charge,
            'grand_total': grand_total,
            'product_order_number':order_number,

         }
         return render(request,'orders/payment.html', context)
      
      else:
         # print(form.errors.as_data())
         return redirect('checkout')

   else:
        return redirect('checkout')
 
 

def cash_on_delivery(request, id):
    # Move cart item to orderd product table
   
   #  print("ippo kittum")
    try:
      #   print("Niokki irunno")
        order = Order.objects.get(user = request.user, is_ordered = False, order_number = id)
        print(order)
        cart_items = Cartitem.objects.filter(user = request.user)
        order.is_ordered = True
        payment = Payment(
            user = request.user,
            payment_id = order.order_number,
            order_number = order.order_number,
            payment_method = 'Cash On Delivery', 
            amount_paid = order.order_total,
            status = False
        )
      #   print("ayyedaaa mone")
        payment.save()
        order.payment = payment
        order.is_ordered = True
        order.save()
        for cart_item in cart_items:
            order_product =  OrderProduct()
            order_product.order_id = order
            order_product.user_id =  request.user
            order_product.product_id = cart_item.product_id
            order_product.quantity =  cart_item.quantitiy
            order_product.product_price = cart_item.product_id.product_max_price
            order_product.ordered = True
            order_product.save()
        #Reduce Quantity of procut
            product = Product.objects.get( id = cart_item.product_id.id)
            product.stock -= cart_item.quantitiy
            product.save()

            #clear cart
            Cartitem.objects.filter(user = request.user).delete()
            #send order number and Transaction id to Web page using 
            context ={
            'orders':order,
            'payment':payment
             }
            # print("ittech podaaaa")
            return render(request,'orders/cash-delivery-success.html',context)
    except Exception as e:
        print(e)
      #   print("ayye patticheeeee")
        return redirect('home')


