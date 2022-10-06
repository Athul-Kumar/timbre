from itertools import product
from  . models import Product, Brandinfo
from django import forms


# ----------------------------------------------

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields =  '__all__'
        

class BrandForm(forms.ModelForm):

    class Meta:
        model = Brandinfo
        fields= '__all__'