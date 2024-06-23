from django.shortcuts import render, redirect
from pyexpat.errors import messages
from .forms import CustomerForm, DriverCreationForm


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


def register_driver(request):
    if request.method == 'POST':
        form = DriverCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = DriverCreationForm()
    return render(request, 'drivercreation.html', {'form': form})
