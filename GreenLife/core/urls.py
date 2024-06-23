from django.urls import path
from .views import home, register_customer, register_driver


urlpatterns = [
    path('', home, name='home'),
    path('register/customer/', register_customer, name='register_customer'),
    path('register/driver/', register_driver, name='register_driver'),
]
