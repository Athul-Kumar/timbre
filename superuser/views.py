from itertools import product
from multiprocessing import context
from django.shortcuts import render,redirect
from accounts.models import Account
from accounts.forms import RegistrationForm, UserForm
from orders.forms import OrderForm
from store.models import Product
from store.forms import ProductForm
from store.models import Brandinfo
from store.forms import BrandForm
from category.models import Category
from category.forms import CategoryForm
from orders.models import Order, OrderProduct, Payment
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
# from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404

from category.views import category


# Create your views here.

# Admin login & logout



def admin_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method =='POST':
        email = request.POST.get('email')
        password= request.POST.get('password')
        user = auth.authenticate(email=email, password=password)

        if user is not None:
            user = Account.objects.get(email=email)
            if user.is_admin == True:
                auth.login(request, user)
                return redirect('dashboard')
            
            else:
                messages.error(request, "Invalid login credentials")
                return redirect('admin_login')

    return render(request, 'superuser/login.html')



def admin_home(request):
# product status

    order_confirmed = Order.objects.filter(status='Order confirmed').count()
    shipped = Order.objects.filter(status = 'Shipped').count()
    out_of_delivery = Order.objects.filter(status = 'Out of Delivery').count()
    completed = Order.objects.filter(status = 'Completed').count()
    Cod = Payment.objects.filter(payment_method = 'Cash On Delivery', status = False).count()
    payPal = Payment.objects.filter(payment_method = 'PayPal', status = False).count()
    Razorpay = Payment.objects.filter(payment_method = 'RazorPay', status = False).count()
    print(Cod, payPal, Razorpay)
    context ={
        'order_confirmed': order_confirmed,
        'shipped': shipped,
        'out_of_delivery': out_of_delivery,
        'completed': completed,
        'Cod': Cod,
        'payPal': payPal,
        'RazorPay': Razorpay,

    }

    return render(request, 'superuser/dashboard.html',context)



@login_required(login_url= 'admin_login')
def admin_logout(request):
    auth.logout(request)
    return redirect('admin_login')



# admin user side

def userlist(request):
    users = Account.objects.filter(is_admin=False, is_verified=True)
    form= UserForm()
    # pagination

    p= Paginator(Account.objects.filter(is_admin=False, is_verified=True), 5)
    page= request.GET.get('page')
    userlist= p.get_page(page)  
    context={
        'users': users,   
        'form': form,
        'userlist': userlist
    }
    # print(users)

    return render(request, 'superuser/userlist.html', context)



def userblock(request,id,flag):
    if request.method == 'POST':
        customer= Account.objects.get(id = id)
        if flag ==1:
            customer.is_active = False
            customer.save()
        else: 
            customer.is_active = True
            customer.save()
        return redirect('userlist')


# def userblock(request, id):
#     if request.method == 'POST':
#         customer = Account.objects.get(id= id)
#         if customer.is_active== True:
#             customer.is_active= False
#             customer.save()
            
#     return redirect('userlist')


# def userunblock(request, id):
#     if request.method == 'POST':
#         customer = Account.objects.get(id=id)
#         if customer.is_active == False:
#             customer.is_active = True
#             customer.save()
#     return redirect('userlist')


#  Admin category

def admin_category(request):
    categories = Category.objects.all()
    form = CategoryForm()

    # pagination
    p= Paginator(Category.objects.all(), 5)
    page= request.GET.get('page')
    categorylist= p.get_page(page)  


    context ={
        'categories': categories,
        'form': form,
        'categorylist': categorylist,   
    }

    return render(request, 'superuser/categorylist.html', context)


def admin_category_add(request):
    if request.method == 'POST':
        form=CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully.')
            return redirect('categorylist')
        else:
            messages.error(request, 'Category added failed.')
            return redirect('categorylist')
        
    form = CategoryForm()
    context ={
        
        'form': form
    }

    return render(request, 'superuser/category-add.html', context)



def admin_category_delete(request, id):
    if request.method =='POST':
        category_id = Category.objects.get(pk=id)
        category_id.delete()
    return redirect('categorylist')

# Admin Products

def admin_productlist(request):

    productlist = Product.objects.all()
    form = ProductForm()
    # pagination 

    p = Paginator(Product.objects.all(), 5)
    page= request.GET.get('page')
    productedlist= p.get_page(page)  

    context = {
        'productlist': productlist,
        'form': form,
        'productedlist': productedlist
    }
    return render(request, 'superuser/productlist.html', context)


def admin_product_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully.')
            return redirect('productlist')

        else:
            print(form.errors.as_data())
            messages.error(request, 'product adding is failed')
            return redirect('productlist')
        
    form = ProductForm()
    context = {

      'form': form
    }
    
    return render(request, 'superuser/product-add.html', context)

def admin_product_delete(request, id):
    if request.method == 'POST':
        product_id = Product.objects.get(pk=id)
        product_id.delete()

    return redirect('productlist')

# def admin_product_specifications(request):
#     if request.method == 'POST':
#         form = SpecificationForm()
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Specification added successfully.')
#             return redirect('productlist')
#         else:
#             messages.error(request, 'Specification adding is failed')
#             return redirect('productlist')

#     form = SpecificationForm()
#     context ={
#         'form': form
#     }

#     return render(request, 'superuser/product-specifications.html',context)


# Admin Brans

def admin_brandlist(request):

    brandlist = Brandinfo.objects.all()
    form = BrandForm()
    # pagination
    p= Paginator(Brandinfo.objects.all(), 5)
    page= request.GET.get('page')
    brandedlist= p.get_page(page)  

    context = {
        'brandlist': brandlist,
        'form': form,
        'brandedlist': brandedlist
    }

    return render(request, 'superuser/brandlist.html', context)


def admin_brand_delete(request, id):
    if request.method =='POST':
        brand_id = Brandinfo.objects.get(pk=id)
        brand_id.delete()
    return redirect('brandlist')


def admin_brand_add(request):
    if request.method == 'POST':
        form = BrandForm(request.POST, request.FILES)
        # print(form)
        if form.is_valid():
            form.save()
            messages.success(request, 'Brand added successfully.')
            return redirect('brandlist')
        else:
            print(form.errors.as_data())
            messages.error(request, 'Brand adding is failed')
            return redirect('brandlist')

    form = BrandForm()
    context ={
        'form': form
    }

    return render(request, 'superuser/brand-add.html', context)



def admin_orderlist(request):
    # print("enthada")
    if 'key' in request.GET:
        # print("inguvaaa ni")
        key = request.GET.get('key')
        if key:
            order = Order.objects.all().filter(tracking_no__icontains = key).order_by('-created_at')
        else:
            return redirect('orderlist')
    else:
        order = Order.objects.all().filter().order_by('-created_at')

    p = Paginator(order, 10)
    page = request.GET.get('page')
    orders = p.get_page(page)
    # print("vallom nadakkuvo")
    form = OrderForm()
    
    
    context = {
        'form' : form,
        'orders' : orders
    }
    return render(request, 'superuser/order-detail.html',context)

def admin_order_update(request, id):
    if request.method == 'POST':
        instance = get_object_or_404(Order, id=id)
        status = request.POST.get('status')
        instance.status = status
        instance.save()
    return redirect('order-detail')