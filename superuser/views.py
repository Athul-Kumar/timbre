from itertools import product
from multiprocessing import context
from django.shortcuts import render,redirect
from accounts.models import Account
from accounts.forms import RegistrationForm,UserForm
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
from django.shortcuts import get_object_or_404

from category.views import category
from orders.models import Coupon
from orders.forms import CouponForm
import datetime
from datetime import datetime,timedelta,date
from django.db.models import Sum,Q

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
    out_of_delivery = Order.objects.filter(status = 'Out for Delivery').count()
    completed = Order.objects.filter(status = 'Completed').count()
    Cod = Payment.objects.filter(payment_method = 'Cash On Delivery', status = False).count()
    payPal = Payment.objects.filter(payment_method = 'PayPal').count()
    Razorpay = Payment.objects.filter(payment_method = 'RazerPay').count()
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
    # print("Category Enter")
    if request.method == 'POST':
        form=CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully.')
            return redirect('categorylist')
        else:
            print(form.errors.as_data())
            messages.error(request, 'Category added failed.')
            return redirect('categorylist')
        
    form = CategoryForm()
    context ={
        
        'form': form
    }
    print(form)

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



#  AdminCoupon Section

def admin_display_coupon(request):
    if 'query' in request.GET:
        query = request.GET.get('query')
        print(query)
        if query:
            coupons = Coupon.objects.filter(code__icontains = query)            
        else:
            return redirect(admin_display_coupon)
    else:
        coupons = Coupon.objects.all()
    paginator = Paginator(coupons, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    print(coupons)
    context = {
        'coupons': coupons,
        'page_obj' : page_obj,
        'serch_item':8
    }
    return render(request, 'superuser/coupon-list.html', context)



def admin_add_coupon(request):
    if request.method == 'POST':
        form = CouponForm(request.POST , request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Coupon Added successfully')
            return redirect(admin_display_coupon)
        else:
            messages.error(request, 'Coupon with this code already exists !')
            return redirect(admin_display_coupon)
    form = CouponForm()
    today_date=str(datetime.date.today())
    context = { 
        'form':form,
        'today_date': today_date
    }
    return render(request,'superuser/add-coupon.html',context)

def coupon_delete(request,id):
    print("delte")
    if request.method == 'POST' :
        coupon = Coupon.objects.get(id=id)
        coupon.delete()
        messages.error(request, 'Coupon deleted successfully')
    return redirect(admin_display_coupon)


def coupon_update(request, id) :
    category = Coupon.objects.get(id=id)
    if request.method == 'POST' :
        form = CouponForm(request.POST, request.FILES, instance=category)   
        if form.is_valid() :
            form.save()
            messages.success(request,'Coupon Updated success fully ')
            return redirect(admin_display_coupon)    
    form = CouponForm(instance=category)
    today_date=str(datetime.date.today())
    context = {'form' : form,'today_date': today_date}
    return render(request, 'superuser/add-coupon.html', context)  





# @staff_member_required(login_url='admin_login')
def category_offer(request):
    if 'query' in request.GET:
        query = request.GET.get('query')
        print(query)
        if query:
            category=Category.objects.filter(category_name__icontains = query)
        else:
            return redirect(admin_category)
    else:
        category=Category.objects.all()
    paginator = Paginator(category, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context={
        'category':category,
        'page_obj': page_obj,
        'serch_item':7
    }

    return render(request,'superuser/category-offer.html',context)

# @staff_member_required(login_url='admin_login')
def add_category_offer(request):
    if request.method == 'POST' :
        category_name = request.POST.get('category_name')
        category_offer = request.POST.get('category_offer')
        category = Category.objects.get(category_name = category_name)
        category.category_offer =  category_offer
        category.save()
        messages.success(request,'Added Category offer success fully')
        return redirect('category_offer')
        
# @staff_member_required(login_url='admin_login')
def category_offer_delete(request,id):
    if request.method == 'POST' :
        category = Category.objects.get(id = id)
        category.category_offer =  0
        category.save()
        messages.error(request,'Deleted Category offer successfully')
        return redirect('category_offer')
        



def product_offer(request):
    if 'query' in request.GET:
        query = request.GET.get('query')
        print(query)
        if query:
            product=Product.objects.filter(product_name__icontains = query).order_by('-created_at')
        else:
            return redirect(admin_productlist)
    else:
        product=Product.objects.all()
    paginator = Paginator(product, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context={
        'product':product,
        'page_obj':page_obj,
         'serch_item':6
    }
    return render(request,'superuser/product-offer.html',context)

# @staff_member_required(login_url='admin_login')
def add_product_offer(request):
    if request.method == 'POST' :
        product_name = request.POST.get('product_name')
        product_offer = request.POST.get('product_offer')
        product = Product.objects.get(product_name = product_name)
        product.product_offer = product_offer 
        product.save()
        messages.success(request,'Added product offer success fully')
        return redirect('product_offer')

# @staff_member_required(login_url='admin_login')
def product_offer_delete(request,id):
    if request.method == 'POST' :
        product = Product.objects.get(id = id)
        product.product_offer =  0
        product.save()
        messages.success(request,'Deleted product offer successfully')
        return redirect('product_offer')


#  sales report


# @staff_member_required(login_url='admin_login')
def sales_report(request):
    year = datetime.now().year
    today = datetime.today()
    month = today.month
    years = []
    today_date=str(date.today())

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        val = datetime.strptime(end_date, '%Y-%m-%d')
        end_date = val+timedelta(days=1)
        orders = Order.objects.filter(Q(created_at__lt=end_date),Q(created_at__gte=start_date),payment__status = True).values('user_order_page__product_id__product_name','user_order_page__product_id__stock',total = Sum('order_total'),).annotate(dcount=Sum('user_order_page__quantity')).order_by()
        # print(orders)
    else:
        # print(orders)
        orders = Order.objects.filter(created_at__year = year,created_at__month=month,payment__status = True).values('user_order_page__product_id__product_name','user_order_page__product_id__stock',total = Sum('order_total'),).annotate(dcount=Sum('user_order_page__quantity')).order_by()
        # print(orders)
    year = today.year
    for i in range (10):
        val = year-i
        years.append(val)
    context = {
        'orders':orders,
        'today_date':today_date,
        'years':years
    }
    
    return render(request,'superuser/salesreport.html',context)
      

# @staff_member_required(login_url='admin_login')
def sales_report_month(request,id):
    print("reached")
    orders = Order.objects.filter(created_at__month = id,payment__status = True).values('user_order_page__product_id__product_name','user_order_page__product_id__stock',total = Sum('order_total'),).annotate(dcount=Sum('user_order_page__quantity')).order_by()    
   
    today_date=str(date.today())
    context = {
        'orders':orders,
        'today_date':today_date
    }
    print(orders)
    return render(request,'superuser/sales-report-table.html',context) 
  



# @staff_member_required(login_url='admin_login')
def sales_report_year(request,id):
    orders = Order.objects.filter(created_at__year = id,payment__status = True).values('user_order_page__product_id__product_name','user_order_page__product_id__stock',total = Sum('order_total'),).annotate(dcount=Sum('user_order_page__quantity')).order_by()    
    today_date=str(date.today())
    context = {
        'orders':orders,
        'today_date':today_date
    }
    return render(request,'superuser/sales-report-table.html',context)
    
