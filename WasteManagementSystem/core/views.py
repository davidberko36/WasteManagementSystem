from django.http import JsonResponse
from django.contrib.auth import login
from .forms import SignupForm, DriverCreationForm

def customer_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return JsonResponse({'success': True, 'message': 'Customer registration successful'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = SignupForm()
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

def driver_signup(request):
    if request.method == 'POST':
        form = DriverCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return JsonResponse({'success': True, 'message': 'Driver registration successful'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = DriverCreationForm()
    return JsonResponse({'success': False, 'message': 'Invalid request method'})