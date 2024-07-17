from django.shortcuts import render, redirect
from pyexpat.errors import messages
from .forms import CustomerForm, DriverCreationForm, SignInForm
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse


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


# class SignInView(View):
#     template_name = 'sign in.html'
#
#     def get(self, request):
#         form = SignInForm()
#         return render(request, self.template_name, {'form': form})
#
#     def post(self, request):
#         form = SignInForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 messages.success(request, f"Welcome back, {username}!")
#                 return redirect('')
#             else:
#                 messages.error(request, "Invalid username or password.")
#         return render(request, self.template_name, {'form': form})

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
