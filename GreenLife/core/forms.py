from django import forms
from .models import User, Customer, Driver, Schedule, Issues


class CustomerForm(forms.ModelForm):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    last_name = forms.CharField(max_length=255)
    other_names = forms.CharField(max_length=255)
    username = forms.CharField(max_length=255)

    class Meta:
        model = Customer
        fields = ['username', 'address']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['password'].required = True
        self.fields['last_name'].required = True
        self.fields['other_names'].required = True
        self.fields['username'].required = True

    def save(self, commit=True):
        user = User.objects.create_user(
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            last_name=self.cleaned_data['last_name'],
            other_names=self.cleaned_data['other_names'],
        )
        customer = Customer.objects.create(
            user=user,
            username=self.cleaned_data['username'],
            address=self.cleaned_data['address'],
        )
        return customer


class DriverCreationForm(forms.ModelForm):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    last_name = forms.CharField(max_length=255)
    other_names = forms.CharField(max_length=255)
    username = forms.CharField(max_length=255)
    driver_license = forms.CharField(max_length=30)

    class Meta:
        model = Driver
        fields = ['driver_license']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['password'].required = True
        self.fields['last_name'].required = True
        self.fields['other_names'].required = True
        self.fields['username'].required = True
        self.fields['driver_license'].required = True

    def save(self, commit=True):
        user = User.objects.create_user(
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            last_name=self.cleaned_data['last_name'],
            other_names=self.cleaned_data['other_names'],
        )
        driver = Driver.objects.create(
            user=user,
            username=self.cleaned_data['username'],
            driver_license=self.cleaned_data['driver_license'],
        )
        return driver
