from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import SignupForm, DriverCreationForm, SignInForm





def home(request):
    return render(request, 'index.html')



def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})



# def signin(request):
#     return render(request, 'signin.html', {})




def signin(request):
    if request.method == 'POST':
        #form = SignInForm(request, request.POST)
        form = SignInForm(None, data=request.POST)
        if form.is_valid():
            # username = form.cleaned_data['username']
            # password = form.cleaned_data['password']
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, "Invalid username or password.")
    else:
        form = SignInForm()
    return render(request, 'signin.html', {'form': form})





def Plans(request):
    return render(request, 'plans.html')




def AboutUs(request):
    return render(request, 'about.html')







# def customer_signup(request):
#     if request.method == 'POST':
#         form = SignupForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return JsonResponse({'success': True, 'message': 'Customer registration successful'})
#         else:
#             return JsonResponse({'success': False, 'errors': form.errors})
#     else:
#         form = SignupForm()
#     return JsonResponse({'success': False, 'message': 'Invalid request method'})

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