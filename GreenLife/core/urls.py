from django.urls import path
from .views import home, register_customer, register_driver, about, SignInView, logout_view, mission, services, pricing


urlpatterns = [
    path('', home, name='home'),
    path('register/customer/', register_customer, name='register_customer'),
    path('register/driver/', register_driver, name='register_driver'),
    path('about/', about, name='about'),
    path('mission/', mission, name='mission'),
    path('services/', services, name='services'),
    path('pricing/', pricing, name='pricing'),
    path('sign_in/customer/', SignInView.as_view(), name='sign_in_customer'),
    path('logout/', logout_view, name='logout'),
]