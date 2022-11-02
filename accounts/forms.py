from django import forms
from .models import Account
from orders.models import Address



class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Confirm password'}))
    class Meta:
        model = Account
        fields =  ['first_name', 'last_name', 'email', 'mobile', 'password']


    

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder']='Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder']='Enter Last Name'
        self.fields['email'].widget.attrs['placeholder']='Enter Email Id'
        self.fields['mobile'].widget.attrs['placeholder']='Enter Mobile Number'
        # self.fields['password'].widget.attrs['placeholder']='Enter Password'
        # self.fields['confirm_password'].widget.attrs['placeholder']='Confirm Password'

        for fields in self.fields:
            self.fields[fields].widget.attrs['class']='form-control'


    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password  = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "password does not match!"
            )


class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['is_active'] 

    def __str__(self):
        return self.first_name




class UserUpdationForm(forms.ModelForm):
    class Meta:
        model=Account
        fields=['first_name','last_name' ,'email','mobile','profile_image']

class AddAddress(forms.ModelForm):
    class Meta:
        model = Address
        fields=['first_name','last_name','phone','email','address_line_1','address_line_2','country','state','city']





# # --------------------jithin-------------------

# from django import forms
# from .models import Account

# # Create your forms here.

# # class RegistrtationForm(forms.ModelForm):

# #     password=forms.CharField(widget=forms.PasswordInput(attrs={
# # 		'placeholder':'Enter Password'
# # 	}))
# #     confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={
# # 		'placeholder':'Enter Password'
# # 	})) 
# #     class Meta:
# #         model=Account
# #         fields=['first_name','last_name' ,'email','mobile' ,'password','confirm_password']
# #     def clean(self):
# #         cleaned_data    =super(RegistrtationForm,self).clean()
# #         password        =cleaned_data.get('password')
# #         confirm_password=cleaned_data.get('confirm_password')
# #         if password != confirm_password:
# #             raise forms.ValidationError("Password does not match")    
