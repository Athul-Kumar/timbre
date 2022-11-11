from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from carts.models import Cartitem
from store.models import Product
from .models import Order, Payment, OrderProduct, Address, Coupon, UserCoupon
from .forms import OrderForm
from django.contrib.auth.decorators import login_required
import razorpay
import datetime
import json


from django.core.paginator import Paginator

# ------------------------------------
# Create your views here.
client = razorpay.Client(auth=('rzp_test_BsgpW3PBm8OnAn', '6ggyjHFCI1nq9BBgJWqOVpxG'))

def payments(request):
  
   body = json.loads(request.body)
   # print(body['orderID'])
   order = Order.objects.get(user= request.user, is_ordered = False, order_number= body['orderID'])
   
   payment = Payment(
      user =  request.user,
      payment_id =body['transID'],
      payment_method = body['payment_method'],
      amount_paid = order.order_total,
      status = True,
      order_number = body['orderID']
   )
   payment.save()
  
   order.payment = payment
   order.is_ordered =True
   order.save()

      # move the cart item to the Orderproduct table
   cart_items = Cartitem.objects.filter(user = request.user) 
   for item in cart_items:

      orderproduct =OrderProduct()
      orderproduct.order_id = order
      orderproduct.payment_id = payment
      orderproduct.user_id = request.user
      orderproduct.product_id = item.product_id
      orderproduct.quantity = item.quantitiy
      orderproduct.product_price = item.product_id.product_max_price
      orderproduct.ordered = True
      orderproduct.save()


      # reduce the quantity of sold products
      # print(item.product_id)
      product = Product.objects.get(id = item.product_id.id)
     
      product.stock -= item.quantitiy
      product.save()

   # clear the cart
   Cartitem.objects.filter(user=request.user).delete()

   # send order number and translation back to console.(senddata)

   data = {
      'order_number': order.order_number,
      'transID': payment.payment_id

   }
   
   return JsonResponse(data)


@login_required(login_url='login')
def order_complete(request):
   order_number = request.GET.get('order_number')
   transID  = request.GET.get('transID')

   try:

      order = Order.objects.get(order_number=order_number, is_ordered= True)
      ordered_products = OrderProduct.objects.filter(order_id = order)

      subtotal = 0
      for i in ordered_products:
         subtotal += i.product_price * i.quantity
      context = {
         'order' :   order,
         'ordered_products' : ordered_products,
         'subtotal' : subtotal,
      }

      return render(request, 'orders/order_complete.html', context)
   except (Payment.DoesNotExist, Order.DoesNotExist):
      return redirect('home')


@login_required(login_url='login')
def place_order(request, total =0, quantitiy =0):
   print(request.method)
   
   current_user = request.user
   # if the cart count <0 then redirect to store
   cart_items = Cartitem.objects.filter(user= current_user)
   cart_count = cart_items.count()

   if cart_count <=0:
    return redirect('store')
   grand_total = 0
   delivery_charge = 0

   for cart_item in cart_items:
      
      total  += int(cart_item.product_id.offer_price())*int(cart_item.quantitiy)
      quantitiy+= cart_item.quantitiy
    
   delivery_charge = 250 if total <= 5000 else 0
   grand_total = total + delivery_charge

   if request.method == 'POST':
      # form =  OrderForm(request.POST)
      # if form.is_valid():
         id = request.POST['flexRadioDefault']
         address  = Address.objects.get(user = request.user,id = id)
         
        #  store all the billing information inside order table

         data = Order()
         data.user = current_user
         data.first_name = address.first_name
         data.last_name = address.last_name
         data.email = address.email
         data.phone = address.phone
         data.address_line_1 = address.address_line_1
         data.address_line_2 = address.address_line_2
         data.country = address.country
         data.state = address.state
         data.city = address.city
         # data.order_note = address.order_note
         data.order_total = grand_total
         data.delivery_charge = delivery_charge
         data.ip = request.META.get('REMOTE_ADDR')
         data.save()
         #  generate order Number
        
         yr = int(datetime.date.today().strftime('%Y'))
         dt = int(datetime.date.today().strftime('%d'))
         mt = int(datetime.date.today().strftime('%m'))
         d = datetime.date(yr, mt, dt)
         current_date =  d.strftime("%Y%m%d")
         order_number = current_date + str(data.id)
         data.order_number = order_number
         data.save()


         coupons = Coupon.objects.filter(active = True)

         for item in coupons:
            try:
               coupon = UserCoupon.objects.get(user = request.user, coupone = item)
            except:
               coupon = UserCoupon()
               coupon.user = request.user
               coupon.coupone = item
               coupon.order = data
               coupon.save() 

         coupons = UserCoupon.objects.filter(used = False, user = request.user )
         order = Order.objects.get(user = current_user, is_ordered = False, order_number=order_number)
         context = {
            'order': order,
            'cart_items': cart_items,
            'total': total,
            'delivery_charge':delivery_charge,
            'grand_total': grand_total,
            'product_order_number':order_number,
            'coupons':coupons

         }
         return render(request,'orders/payment.html', context)
      
      # else:
      #    # print(form.errors.as_data())
      #    return redirect('checkout')

   else:
        return redirect('checkout')
 
 

@login_required(login_url='login')

def cash_on_delivery(request, id):
    # Move cart item to orderd product table
  
    try:
   
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
      
        payment.save()
        order.payment = payment
        order.is_ordered = True
        order.save()
        for cart_item in cart_items:
            order_product =  OrderProduct()
            order_product.order_id = order
            order_product.user_id =  request.user
            order_product.payment_id = payment
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
            
            return render(request,'orders/cash-delivery-success.html',context)
    except Exception as e:
        print(e)
    
        return redirect('home')




#  RazorPay
@login_required(login_url='login')
def razor_pay(request):
        DATA = {
            "amount": 100,
            "currency": "INR",
            "receipt": "receipt#1",
            "notes": {
                "key1": "value3",
                "key2": "value2"
            }
        }
        payment = client.order.create(data=DATA)
        return JsonResponse({
            'payment':payment,
             'payment_method' : "RazorPay"
        })


#  User Profile Orders


#order management
@login_required(login_url='login')
def user_orders(request):
    orders = Order.objects.filter(user = request.user.id, is_ordered = True).order_by('-created_at') 
    paginator = Paginator(orders, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'orders' : orders,
        'page_obj': page_obj
    }
    return render(request,'accounts/dashboard/user_orders.html',context)



@login_required(login_url='login')
def cancel_order(request,id):
    order = Order.objects.get(order_number = id,user = request.user)
    order.status = "Order cancelled"
    order.save()
    payment = Payment.objects.get(order_number = order.order_number)
    payment.delete()
    return redirect('user_orders')

@login_required(login_url='login')
def return_order(request,id):
    order = Order.objects.get(order_number = id,user = request.user)
    order.status = "Returned"
    order.save()
   #  print("return adikkeda niiii")
    print(f'The value = {order.order_number}')
    payment = Payment.objects.get(order_number = order.order_number)

   #  print("return Kittiii kettooo")
    payment.delete()
    return redirect('user_orders')

@login_required(login_url='login')
def invoice_download(request,id):
   print("invoice ippo kittumm")
   try:
        if request.method == 'POST':
            order = Order.objects.get(user = request.user,id = id)
            ordered_products = OrderProduct.objects.filter(order_id=order.id)

            subtotal = 0
            for i in ordered_products:
                subtotal += i.product_id.sub(request) * i.quantity

            payment = Payment.objects.get(order_number=order.order_number)

            context = {
                'order': order,
                'ordered_products': ordered_products,
                'order_number': order.order_number,
                'transID': payment.payment_id,
                'payment': payment,
                'subtotal': subtotal,
            }
            return render(request, 'accounts/dashboard/invoice_download.html',context )
        else:
            print("invoice kittiyillaaa")
            return redirect('home')
   except:
        print("ippo kittilla")
        return redirect('home')


@login_required(login_url='login')
def coupon(request):
   #  print("coupon kittiyillo")
    if request.method == 'POST':
        grand_total = request.POST.get('grand_total')
        coupon = request.POST.get('coupon')
        coupon_perc = 0
        try:
            instance = UserCoupon.objects.get(user = request.user ,coupone__code = coupon)
            order = Order.objects.get(user = request.user,order_coupon__coupone = instance.coupone)
            if int(grand_total) >= int(instance.coupone.min_value):
                grand_total = int(grand_total) - ((int(grand_total) * int(instance.coupone.discount))/100)
                coupon_perc = instance.coupone.discount
                msg = 'Applied coupon successfully'
                instance.used = True
                order.order_total = grand_total
                order.save()
                instance.save()
            else:
                msg='This coupon only applicable for more than '+ str(instance.coupone.min_value)+ 'rupee only!'
        except:
            msg = 'Coupon is not valid'
        response = {
                         'grand_total': grand_total,
                         'msg':msg,
                         'coupon_perc':coupon_perc
            }
      #   print("hhhh")
        print(grand_total)
        print(coupon_perc)
        return JsonResponse(response)