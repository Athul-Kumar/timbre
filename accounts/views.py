
from itertools import product
from django.shortcuts import render,redirect
from .models import Account
from .forms import RegistrationForm, UserUpdationForm
from django.contrib import messages,auth
from .verify import send_otp, verify_otp
from  .forms import *
from .models import *
from django.contrib.auth import authenticate, logout,login
from django.contrib.auth.decorators import login_required
from carts.views import _cart_id
from carts .models import Cart, Cartitem
from orders.models import Address





from django.core.paginator import Paginator
import requests


def user_register(request):
   
    if request.method=='POST':
        
        form=RegistrationForm(request.POST)
        if form.is_valid():
            first_name = request.POST['first_name']
            last_name  = request.POST['last_name']
            email      = request.POST['email']
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
            print(form.errors.as_data())
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
            messages.error(request,"User does not exist..")
        user = auth.authenticate(request,email=email,password=password)
        if user is not None:
            try:
                print("User Exist")
               
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
            # print('podapatti')
        #     user = authenticate(request,mobile = mobile)
        #   if user is not None:
            login(request,user)
            return redirect('home') 
        else:
            messages.error(request,'Wrong OTP..')
            # return redirect('otplogin')
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
            mobile     = request.session['mobile']
            password   = request.session['password']

            user = Account.objects.create_user(
                first_name =  first_name,
                last_name  =  last_name,
                email      =  email,
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





# User Dashboard

def user_dashboard(request):

    return render(request, 'accounts/dashboard/user_dashboard.html')

def user_details(request):
    user_details = Account.objects.filter(id = request.user.id)

    context = {
        'user_detail': user_details
    }

    return render(request, 'accounts/dashboard/user_details.html', context)



def user_detail_update(request):
    id=Account.objects.get(id = request.user.id)
    if request.method == 'POST':
        form = UserUpdationForm(request.POST , request.FILES, instance=id)
        if form.is_valid():
            form.save()
            messages.success(request , 'Updated Successfully')
            return redirect(user_details)
        else:
            messages.error(request , 'Details is not valid please check it!!')
            return redirect(user_details)
    else:
        form = UserUpdationForm(instance=id)
        context = {
            'form' : form,
        }
    return render(request , 'accounts/dashboard/user_detail_update.html' , context)
    # return render(request , 'accounts/dashboard/user_detail_update.html')



def address_list(request):
    addresses=Address.objects.filter(user = request.user.id)
    paginator = Paginator(addresses, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context={
        'addresses':addresses,
        'page_obj':page_obj
    }
    return render(request,'accounts/dashboard/address_list.html',context)

def add_address(request):
    if request.method == 'POST':
        form = AddAddress(request.POST,request.FILES,)
        if form.is_valid():
            print('form is valid')
            detail = Address()
            detail.user = request.user
            detail.first_name =form.cleaned_data['first_name']
            detail.last_name = form.cleaned_data['last_name']
            detail.phone =  form.cleaned_data['phone']
            detail.email =  form.cleaned_data['email']
            detail.address_line_1 =  form.cleaned_data['address_line_1']
            detail.address_line_2  = form.cleaned_data['address_line_2']
            detail.country =  form.cleaned_data['country']
            detail.state =  form.cleaned_data['state']
            detail.city =  form.cleaned_data['city']
            detail.save()
            messages.success(request,'Address is Added Successfully')
            return redirect(address_list)
        else:
            messages.success(request,'Form is Not valid')
            return redirect(address_list)
    else:
        form = AddAddress()
        context={
            'form':form
        }    
    return render(request,'accounts/dashboard/add_address.html',context)


def delete_address(request,id):
    address=Address.objects.get(id = id)
    messages.success(request,"Address Deleted")
    address.delete()
    return redirect(address_list)


def update_address(request,id):
    id=Address.objects.get(id = id)
    if request.method == 'POST':
        form = AddAddress(request.POST, instance=id)
        if form.is_valid():
            form.save()
            messages.error(request , 'Updated Successfully')
            return redirect(address_list)
        else:
            messages.error(request , 'Details is not valid please check it!!')
            return redirect(address_list)
    else:
        form = AddAddress(instance=id)
        context = {
            'form' : form,
        }
    return render(request , 'accounts/dashboard/update_address.html' , context)
