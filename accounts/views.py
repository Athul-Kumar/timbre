# from multiprocessing import context
# from django.shortcuts import render, redirect
# from django.shortcuts import  HttpResponse
# from .forms import RegistrationForm
# from .models import Account
# from django.contrib import messages, auth
# from django.contrib.auth.decorators import login_required

# # 
# # from django.utils.decorators import method_decorator
# # import json
# # # 
# # # from  .forms import PhoneVerificationForm
# # # 
# # # from authy_api import send_verfication_code, verify_sent_code
# # # # 

# # # Create your views here.



# def user_register(request):
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             first_name = form.cleaned_data['first_name']
#             last_name = form.cleaned_data['last_name']
#             email = form.cleaned_data['email']
#             mobile = form.cleaned_data['mobile']
#             password = form.cleaned_data['password']
#             user = Account.objects.create_user(first_name= first_name, last_name= last_name, email = email, mobile = mobile, password = password)
#             user.save()
#             messages.success(request, 'Registration Successful')
#             return redirect('register')
#     else: 
#         form = RegistrationForm()     
    
#     context = {
#         'form': form,
#     }
#     return render(request, 'accounts/register.html', context)



# def user_login(request):
    # if request.method == 'POST':
    #     email =  request.POST['email']
    #     password = request.POST['password']
    #     user = auth.authenticate(email=email, password=password)
        
    #     if user is not None:
    #         auth.login(request, user)
    #         return redirect('home')
    #     else:
    #         messages.error(request, 'lnvalid login credentials')
    #         return redirect('login')    
#     return render (request, 'accounts/login.html')



# @login_required(login_url= 'login')
# def user_logout(request):
#     auth.logout(request)
#     messages.success(request, 'you are logged out')
#     return redirect('login')




    # ---------------jithin-------------------#

from itertools import product
from django.shortcuts import render,redirect
from .models import Account
from .forms import RegistrationForm
from django.contrib import messages,auth
from .verify import send_otp, verify_otp
from  .forms import *
from .models import *
from django.contrib.auth import authenticate, logout,login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from carts.views import _cart_id
from carts .models import Cart, Cartitem
from orders .models import Order, OrderProduct

import requests
from django.shortcuts import get_object_or_404

# Create your views here.
def user_register(request):
    if request.method=='POST':
        
        form=RegistrationForm(request.POST)
        if form.is_valid():
            first_name = request.POST['first_name']
            last_name  = request.POST['last_name']
            email      = request.POST['email']
            # gender     = request.POST['gender']
            mobile     = request.POST['mobile']
            password   = request.POST['password']

            request.session['first_name'] = first_name
            request.session['last_name']  = last_name
            request.session['email']      = email
            # request.session['gender']     = gender
            request.session['mobile']     = mobile
            request.session['password']   = password
            
            # print("mobile: ",mobile)
            send_otp(mobile)
            return redirect(verify_code)
        else:
            messages.error(request,"Enter correct data")
            return render(request,'accounts/register.html')

    form=RegistrationForm()
    context = {
         'form': form,
    }
    return render(request,'accounts/register.html', context )

def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
      
        try:
            user = Account.objects.get(email=email)
            
        except :
            messages.error(request,"user Does not exist..")
        user = auth.authenticate(request,email=email,password=password)
        if user is not None:
            try:
               
                cart = Cart.objects.get(cart_id = _cart_id(request))
                is_cart_item_exists = Cartitem.objects.filter( cart_id=cart).exists()
                if is_cart_item_exists:
                    cart_item =  Cartitem.objects.filter(cart_id = cart)
                    print(cart_item)
                    for item in cart_item:
                        item.user = user 
                        item.save()
            except:
                pass
            auth.login(request,user)
            url = request.META.get('HTTP_REFERER') 

            try: 
                query =requests.utils.urlparse(url).query
                # print('query ->', query)
                params = dict(x.split('=') for x in query.split('&'))
                # print('params ->', params)
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)

               
            except:
                return redirect('home') 
        else:
            messages.error(request, 'lnvalid login credentials')
            return redirect('login')
    return render(request,'accounts/login.html')





def loginotp(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        mobile = request.POST.get('mobile')
        request.session['mobile'] = mobile
        try :
            user = Account.objects.get(mobile = mobile)
        except:
            messages.error(request, 'mobile is not registered')
            return redirect('otplogin')
    
        send_otp(mobile)
        return redirect(verify_loginotp)
    return render(request, 'accounts/otplogin.html')

def verify_loginotp(request):
    if request.method =='POST':
        otp_check = request.POST.get('otp')
        mobile=request.session['mobile']

        verify=verify_otp(mobile,otp_check)
        user = Account.objects.get(mobile = mobile)
        if verify:
            mobile  = request.session['mobile']
            print('podapatti')
        #     user = authenticate(request,mobile = mobile)
        #   if user is not None:
            login(request,user)
            return redirect('home') 
        else:
            # messages.error(request,'user does not exist..')
            return redirect('otplogin')
    return render(request,'accounts/verify.html')


@login_required
def user_logout(request):
    # if request.method == 'POST':
    auth.logout(request)
        # print(auth.logout(request))
    messages.success(request, 'you are logged out')
    return redirect('login')

    
   
    # return HttpResponse('<h1>404</h1>')

def verify_code(request):
    if  request.method == 'POST':
        otp_check = request.POST.get('otp')
        mobile=request.session['mobile']

        verify=verify_otp(mobile,otp_check)

        if  verify:
            messages.success(request,'account has created successfuly please login now') 

            first_name = request.session['first_name']
            last_name  = request.session['last_name']
            email      = request.session['email']
            # gender     = request.session['gender']
            mobile     = request.session['mobile']
            password   = request.session['password']

            user = Account.objects.create_user(
                first_name =  first_name,
                last_name  =  last_name,
                email      =  email,
                # gender     =  gender,
                mobile     =  mobile,
                password   =  password
            )
            user.is_verified = True
            user.save()
            messages.success(request,'Registration Successful')
            return redirect('login')
        
        else:
            messages.error(request,'Incorrect OTP')
            return redirect ('verify')
        
    return render(request,'accounts/verify.html')


def home(request):
    return render(request, 'index.html')


def user_dashboard(request):
    orders = Order.objects.order_by('-created_at').filter(user = request.user.id, is_ordered = True)
    orders_count =  orders.count()
    context = {
        'orders_count': orders_count,

    }
    return render(request, 'accounts/dashboard.html', context)

def my_orders(request):
    orders = OrderProduct.objects.filter(user_id = request.user.id  )
    
    context = {
        'orders': orders,
    }
    return render(request, 'accounts/my_orders.html', context)


def edit_profile(request):
    
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FIELS, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
           
            
            messages.success(request, 'Your profile has been Updated.')
            return redirect('edit_profile')
    else:
        
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance = userprofile)
     
    
    context={
        'user_form': user_form,
        'profile_form': profile_form,
    }

    return render(request, 'accounts/edit_profile.html', context)