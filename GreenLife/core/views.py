from django.shortcuts import render, redirect
from pyexpat.errors import messages
from .forms import CustomerForm, DriverCreationForm, SignInForm
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib import messages


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
                messages.success(request, f"Welcome back, {username}!")
                return redirect('home')  # Replace 'home' with your home page URL name
            else:
                messages.error(request, "Invalid username or password.")
        return render(request, self.template_name, {'form': form})

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


