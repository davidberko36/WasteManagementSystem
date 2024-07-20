from django.shortcuts import render, redirect
from pyexpat.errors import messages
from .forms import CustomerForm, DriverCreationForm, SignInForm, ScheduleCreationForm, CustomerSettingsForm
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Schedule, Customer


# Create your views here.


def home(request):
    return render(request, 'index.html')


def register_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CustomerForm()
    return render(request, 'customersignup.html', {'form': form})


class SignInView(View):
    template_name = 'sign in.html'

    def get(self, request):
        if request.user.is_authenticated:
            print("User is already authenticated, redirecting to home")
            return HttpResponseRedirect(reverse('home'))
        form = SignInForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                print(f"User {username} successfully logged in, redirecting to home")
                return HttpResponseRedirect(reverse('home'))
            else:
                print(f"Authentication failed for user {username}")
                form.add_error(None, "Invalid username or password.")
        else:
            print("Form is invalid:", form.errors)
        return render(request, self.template_name, {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')

def create_schedule(request):
    if request.method == 'POST':
        form = ScheduleCreationForm(request.POST)
        if form.is_valid:
            schedule = form.save(commit=False)
            schedule.user = request.user.customer
            schedule.save()
            return redirect('schedule_success')
        else:
            form = ScheduleCreationForm()
        return render(request, 'plan.html', {'form': form})


@login_required
def cancel_schedule(request):
    schedule = Schedule.objects.filter(user=request.user.customer)
    schedule.is_active=False
    schedule.save()
    return redirect('schedule_cancelled')


@login_required
def settings(request):
    customer = Customer.objects.get(user=request.user)
    if request.method == 'POST':
        form = CustomerSettingsForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your settings have been updated successfully.')
            return redirect('settings')
    else:
        form = CustomerSettingsForm(instance=customer)

    return render(request, 'settings.html', {'form': form})


def register_driver(request):
    if request.method == 'POST':
        form = DriverCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = DriverCreationForm()
    return render(request, 'drivercreation.html', {'form': form})

def about(request):
    return render(request, 'About.html')


def mission(request):
    return render(request, 'mission.html')


def services(request):
    return render(request, 'services.html')


def pricing(request):
    return render(request, 'pricing.html')
