
from django.db import models
from django.urls import reverse
# from django.utils.text import slugify
# Create your models here.

class Category(models.Model):
    id =  models.AutoField(primary_key=True, unique=True)
    category_name= models.CharField(max_length=100, unique=True)
    slug= models.SlugField(max_length = 300, unique=True )
    description = models.TextField(max_length=255, blank=True)
    cat_image= models.ImageField(upload_to='photos/categories', null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    is_available = models.BooleanField(default=True)

    class Meta:
        verbose_name='Category'
        verbose_name_plural = 'Categories'


# slugify

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         slug=self.category_name,self.pk
    #         self.slug = slugify(slug)
    #     return super().save(*args, **kwargs)
 


    # def get_absolute_url(self): 
    #     return reverse('category:single_categorydeatail', args=[self.Category.slug,self.pk])

    
    def get_absolute_url(self):
        return reverse('products_by_category', args=[self.slug])
                      


    def __str__(self):
        return self.category_name 

    
    

