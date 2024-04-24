from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Customer, Driver


class SignupForm(UserCreationForm):
    CUSTOMER_TYPES = [
        ('domestic', 'Domestic'),
        ('business', 'Business'),
    ]

    other_names = forms.CharField(max_length=60, required=True)
    last_name = forms.CharField(max_length=60, required=True)
    address = forms.CharField(max_length=50, required=False)
    username = forms.CharField(max_length = 30, required=True)
    email = forms.EmailField(max_length=255, required=True)
    mobile_phone = forms.CharField(max_length=14, required=True)
    date_of_birth = forms.DateField(required=True)
    customer_type = forms.ChoiceField(max_length = 20, choices=CUSTOMER_TYPES, default=CUSTOMER_TYPES [0][0])


    class Meta:
        model = Customer
        fields = ['other_names', 'last_name', 'address', 'email', 'mobile_phone', 'username', 'date_of_birth', 'customer_type']





class DriverCreationForm(UserCreationForm):
    other_names=forms.CharField(max_length=60, required=True)
    last_name=forms.CharField(max_length=60, required=True)
    email=forms.EmailField(max_length=255, required=True)
    mobile_phone=forms.CharField(max_length=14, required=True)
    date_of_birth=forms.DateField(required=True)
    driver_license_number=forms.CharField(max_length=30, required=True)



    class Meta:
        model = Driver
        fields = ['other_names', 'last_name', 'email', 'mobile_phone', 'date_of_birth', 'driver_license_number']