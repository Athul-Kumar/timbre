from xml.parsers.expat import model
from django import forms
from .models import Order, Coupon




        
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields= ['first_name', 'last_name', 'phone', 'email', 'address_line_1', 'address_line_2', 'country','state', 'city', 'order_note']



class DateInput(forms.DateInput):
    input_type = 'date'

class CouponForm(forms.ModelForm):
    class Meta: 
        model = Coupon      
        fields = ['code', 'discount','min_value','valid_at','active']
        widgets = {
            'valid_at': DateInput(),
        }