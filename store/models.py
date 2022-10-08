from email.policy import default
from django.db import models
from category .models import Category
from django.urls import reverse


# Create your models here.
class Product(models.Model):
    id =  models.AutoField(primary_key=True, unique=True)
    product_name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    description= models.TextField(max_length= 250, blank= True)
    rating= models.FloatField() 
    product_max_price= models.IntegerField()
    product_long_description=models.TextField(max_length=500, blank=True)
    pro_images=models.ImageField(upload_to='photos/products')
    pro_image_1= models.ImageField(upload_to='photos/products')
    pro_image_2= models.ImageField(upload_to='photos/products')
    pro_image_3= models.ImageField(upload_to='photos/products')
    pro_image_4= models.ImageField(upload_to='photos/products')
    stock= models.IntegerField()
    is_available= models.BooleanField(default=True)
    created_date=models.DateTimeField(auto_now_add=True)
    modified_date= models.DateTimeField(auto_now=True)
    spec_title = models.TextField(blank=True, null=True)
    spec_description = models.TextField(null=True,blank=True,)

    
    def __str__(self):
        return self.product_name    

    
    def get_absolute_url(self):
        return reverse('product_detail', args=[self.category_id.slug, self.slug])


    
class Brandinfo(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    brand_name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name = 'productbrand')
    brand_images=models.ImageField(upload_to='photos/brands')
    description= models.TextField(max_length= 250, blank= True)
    total_products= models.IntegerField()
    is_available= models.BooleanField(default=True)
    created_date=models.DateTimeField(auto_now_add=True)
    modified_date= models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name='Brandinfo'
        verbose_name_plural = 'Brandinforms'


    def __str__(self):
        return self.brand_name
    
    def get_absolute_url(self):
        return reverse('brandlist', args=[self.slug])