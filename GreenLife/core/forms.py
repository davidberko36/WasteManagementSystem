from django import forms
from django.core.exceptions import ValidationError
from .models import User, Customer, Driver, Schedule, Issues
from django.contrib.auth.forms import AuthenticationForm
import json
from .email import send_welcome_email
from django.contrib.auth import authenticate


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

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already in use.")
        return email

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


class SignInForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


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


# class DriverCreationForm(forms.Form):
#     email = forms.EmailField(widget=forms.EmailInput(attrs={
#         'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm'
#     }))
#     password = forms.CharField(widget=forms.PasswordInput(attrs={
#         'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm'
#     }))
#     last_name = forms.CharField(widget=forms.TextInput(attrs={
#         'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm'
#     }))
#     other_names = forms.CharField(widget=forms.TextInput(attrs={
#         'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm'
#     }))
#     username = forms.CharField(widget=forms.TextInput(attrs={
#         'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm'
#     }))
#     drivers_license = forms.CharField(widget=forms.TextInput(attrs={
#         'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm'
#     }))


class ScheduleCreationForm(forms.ModelForm):
    PICKUP_FREQUENCY = (
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('biweekly', 'Biweekly'),
        ('fortnightly,', 'Fortnightly'),
    )

    pickup_days = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    )

    frequency = forms.ChoiceField(choices=PICKUP_FREQUENCY)
    start_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'))
    pickup_days = forms.MultipleChoiceField(choices=pickup_days, widget=forms.CheckboxSelectMultiple, required=True)

    class Meta:
        model = Schedule
        fields = ['frequency', 'start_date', 'pickup_days']

    def clean_pickup_days(self):
        return json.dumps(self.cleaned_data['pickup_days'])


class UserIssuesForm(forms.ModelForm):
    ISSUE_TYPE = (
        ('missed pickup', 'Missed pickup'),
        ('poor service', 'Poor service'),
    )

    issue_type = forms.ChoiceField(choices=ISSUE_TYPE)
    details = forms.CharField(widget=forms.Textarea)


class CustomerSettingsForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'w-full px-3 py-2 border rounded-md'}))

    class Meta:
        model = Customer
        fields = ['username', 'email', 'phone_number', 'address']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-md'}),
            'phone_number': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-md'}),
            'address': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-md'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        customer = super().save(commit=False)
        customer.user.email = self.cleaned_data['email']
        if commit:
            customer.user.save()
            customer.save()
        return customer


# class CustomerSettingsForm(forms.ModelForm):
#     password = forms.CharField(
#         widget=forms.PasswordInput,
#         required=False,
#         help_text="Leave blank if you don't want to change your password."
#     )
#     confirm_password = forms.CharField(
#         widget=forms.PasswordInput,
#         required=False,
#         help_text="Enter the same password again for confirmation."
#     )
#
#     class Meta:
#         model = Customer
#         fields = ['username', 'email', 'phone_number', 'address']
#
#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get('password')
#         confirm_password = cleaned_data.get('confirm_password')
#
#         if password and password != confirm_password:
#             raise forms.ValidationError("Passwords do not match.")
#         return cleaned_data
#
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         password = self.cleaned_data.get('password')
#         if password:
#             user.set_password(password)
#         if commit:
#             user.save()
#         return user


class QuoteRequestForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}))
    business_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your business name'}))
    business_address = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your business address'}))


class DriverSignInForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if user is None or not hasattr(user, 'driver'):
                raise forms.ValidationError("Invalid email or password.")
        return cleaned_data