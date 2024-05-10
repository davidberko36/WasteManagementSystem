from django.urls import path
from .views import home, signup


# urlpatterns=[
#     path('signup/', driver_signup.as_view(), name='signup'),
#     path('createdriver/', driver_signup.as_view(), name='driversignup')
# ]




urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, name='signup' )
]