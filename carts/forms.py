from django import forms
from .models import Cart, Cartitem


class CartForm(forms.ModelForm):

    class Meta:
        model = Cart
        fields = '__all__'


class CartitemForm(forms.ModelForm):

    class Meta:
        model = Cartitem
        fields ='__all__'
