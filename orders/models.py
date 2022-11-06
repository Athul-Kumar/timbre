from email.policy import default
from hashlib import blake2b
from django.db import models
from accounts .models import Account
from store .models import Product, Brandinfo
from django.core.validators import MinValueValidator,MaxValueValidator
# Create your models here.
# from django.utils.translation import gettext_lazy as _

# Create your models here.

class Payment(models.Model):
    
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    # amount_id = models.CharField(max_length = 100)
    status = models.BooleanField()
    created_at= models.DateTimeField(auto_now_add=True)
    order_number  =models.IntegerField(null=True)
    amount_paid   = models.CharField(max_length=100, default=0)

    def __str__(self):
        return self.payment_id


class   Order(models.Model):
    STATUS = (
        ('Order confirmed', 'Order confirmed'),
        ('Shipped', 'Shipped'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Completed', 'Completed'),
        #  user side
        ('Order cancelled', 'Order cancelled'),
        ('Returned', 'Returned')

    
    )
    # id =  models.AutoField(primary_key=True, unique=True)
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    product= models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.CharField(max_length=20)
    first_name= models.CharField(max_length=50)
    last_name= models.CharField(max_length=50)
    phone =  models.CharField(max_length=15)
    email = models.EmailField(max_length=50)    
    address_line_1 = models.CharField(max_length=50)
    address_line_2= models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length= 50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    order_total = models.FloatField()
    order_note = models.CharField(max_length=100, blank=True)
    delivery_charge = models.FloatField()
    status = models.CharField(max_length=50,choices=STATUS, default= 'Order confirmed')
    ip=  models.CharField(blank=True, max_length=20)
    is_ordered= models.BooleanField(default= False)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)


    def __str__(self):
        return str(self.first_name)

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'


class OrderProduct(models.Model):
    # id = models.AutoField(primary_key=True, unique=True)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='user_order_page')
    payment_id = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    def __str__(self):
        return self.product_id.product_name



class Address(models.Model):
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    address_line_1 = models.CharField(max_length=50)
    address_line_2 = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)


    
    def __str__(self):
        return str(self.first_name)

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    
    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'



class Coupon(models.Model):
    code = models.CharField(max_length=50,unique=True)
    discount = models.IntegerField(validators = [MinValueValidator(0),MaxValueValidator(20)])
    min_value = models.IntegerField(validators = [MinValueValidator(0)])
    valid_from = models.DateTimeField(auto_now_add=True)
    valid_at = models.DateField()
    active = models.BooleanField(default=False)
    def __str__(self):
        return self.code

class UserCoupon(models.Model):
    user =  models.ForeignKey(Account,on_delete=models.CASCADE, null= True)
    coupone = models.ForeignKey(Coupon,on_delete = models.CASCADE, null = True)
    order  = models.ForeignKey(Order,on_delete=models.SET_NULL,null = True,related_name='order_coupon')
    used = models.BooleanField(default = False)
    def __str__(self):  
        return str(self.id)