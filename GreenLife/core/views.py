from django.shortcuts import render, redirect, get_object_or_404
from pyexpat.errors import messages
from .forms import CustomerForm, DriverCreationForm, SignInForm, ScheduleCreationForm, CustomerSettingsForm
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Schedule, Customer, User, Payment
from .tasks import check_schedule
from decimal import Decimal
from django.conf import settings
from .email import send_welcome_email, send_subscription_email, send_cancellation_email
# from django_paystack.models import Transaction
# from django_paystack.utils import generate_reference


# Create your views here.


def home(request):
    return render(request, 'index.html')


def register_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer=form.save()
            send_welcome_email(customer.user.email)
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
    pricing = {
        'daily': Decimal('50.00'),
        'weekly': Decimal('200.00'),
        'biweekly': Decimal('350.00'),
        'fortnightly': Decimal('300.00'),
    }

    try:
        customer = request.user.customer
    except User.customer.RelatedObjectDoesNotExist:
        messages.error(request, "You need to complete your profile to create a schedule.")
        return redirect('profile')

    active_schedules = Schedule.objects.filter(customer=customer, is_active=True)

    if request.method == 'POST':
        form = ScheduleCreationForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.customer = customer
            schedule.price = pricing[schedule.frequency]
            schedule.save()
            send_subscription_email(schedule.customer.user.email)

            # Schedule the task to run daily
            # check_schedule.apply_async(args=[schedule.id], eta=schedule.start_date)

            messages.success(request, "Schedule created successfully!")
            return redirect('create_schedule')  # Redirect to the plans page or wherever you want
        else:
            messages.error(request, "There was an error in your form. Please check and try again.")
    else:
        form = ScheduleCreationForm()

    return render(request, 'plans.html', {
        'form': form,
        'active_schedules': active_schedules,
        'pricing': pricing
    })


@login_required
def cancel_schedule(request, schedule_id):
    schedule = get_object_or_404(Schedule, id=schedule_id, customer=request.user.customer)
    customer = request.user.customer
    send_cancellation_email(customer.user.email)
    schedule.is_active = False
    schedule.save()
    messages.success(request, 'Your schedule has been cancelled successfully.')
    return redirect('create_schedule')



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
