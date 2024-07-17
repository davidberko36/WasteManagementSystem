from django import forms
from .models import User, Customer, Driver, Schedule, Issues
from django.contrib.auth.forms import AuthenticationForm


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


class ScheduleCreationForm(forms.ModelForm):
    PICKUP_FREQUENCY = (
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('biweekly', 'Biweekly'),
        ('fortnightly,', 'Fortnightly'),
    )

    frequency = forms.ChoiceField(choices=PICKUP_FREQUENCY)
    start_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'))
    end_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'))

    class Meta:
        model = Schedule
        fields = ['frequency', 'start_date', 'end_date']


class UserIssuesForm(forms.ModelForm):
    ISSUE_TYPE = (
        ('missed pickup', 'Missed pickup'),
        ('poor service', 'Poor service'),
    )

    issue_type = forms.ChoiceField(choices=ISSUE_TYPE)
    details = forms.CharField(widget=forms.Textarea)


