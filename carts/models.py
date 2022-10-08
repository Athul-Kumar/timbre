from django.db import models
from store .models import Product

# Create your models here.

class Cart(models.Model):

    cart_id = models.CharField(max_length= 250, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.cart_id



class Cartitem(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name= 'testcase')
    quantitiy = models.IntegerField()
    is_active= models.BooleanField(default= True)


    def sub_total(self):
        return self.product_id. product_max_price * self.quantitiy

    def __str__(self):
        return self.product_id.product_name
    
    