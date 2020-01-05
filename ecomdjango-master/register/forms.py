from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,PasswordChangeForm,AuthenticationForm
from .models import Profile
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'PayPal')
)



class ProfileForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ['image']

class PaymentForm(forms.Form):
    stripeToken = forms.CharField(required=False)
    save = forms.BooleanField(required=False)
    use_default = forms.BooleanField(required=False)


class UserPwChange(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'type':'password',
            }))
    new_password1= forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'type':'password',
            }))
    new_password2= forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'type':'password',
            }))
    def clean_old_password(self):
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password
    class Meta:
        model = User 
        fields = ['old_password','new_password1','new_password2']
class UserEditForm(UserChangeForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'value': 'Stage lkher',
            }))
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Email goes here',
            }))
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'FirstName goes here',
                
            }))
    class Meta:
        model = User
        fields = ['username','first_name','email','password']

class UserLog(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id':"username"  ,
                'class':"form-control",
                 'name':"username" ,
                 'required' : 'autofocus',
            }))
    password = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'type':'password',
                'id':'password',
                
            }))
    class Meta:
        model = User
        fields = ['username','password']

class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id':'first_name',
                'name':'first_name'
            }))
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'name': 'name',
                'id':'name',
            }))
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id':'email',
                'type':'email',
                'name':'email'
            }))
    
    
    password1 = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id':'password',
                'name':'password',
                'type':'password',
            }))
    
    password2 = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id':'password',
                'name':'password',
                'type':'password',
            }))
    
    class Meta:
        model = User
        fields = ['first_name','username','email','password1','password2']

class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(required=False)
    shipping_address2 = forms.CharField(required=False)
    shipping_country = CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',
        }))
    shipping_zip = forms.CharField(required=False)
  
    set_default_shipping = forms.BooleanField(required=False)
    use_default_shipping = forms.BooleanField(required=False)


    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promo code',
        'aria-label': 'Recipient\'s username',
        'aria-describedby': 'basic-addon2'
    }))


class RefundForm(forms.Form):
    ref_code = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4
    }))
    email = forms.EmailField()