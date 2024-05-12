from django.urls import path
from .views import home, signup,signin, Plans, AboutUs
from django.contrib.auth.views import LoginView


# urlpatterns=[
#     path('signup/', driver_signup.as_view(), name='signup'),
#     path('createdriver/', driver_signup.as_view(), name='driversignup')
# ]




urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, name='signup' ),
    path('signin/', signin, name='signin'),
    path('plans/', Plans, name='Plans'),
    path('About Us/', AboutUs, name='About')
]