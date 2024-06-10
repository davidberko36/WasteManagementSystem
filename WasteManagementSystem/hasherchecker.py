import os
import django
from core.models import Customer
from django.contrib.auth.hashers import get_hasher

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WasteManagementSystem.settings')
django.setup()

from core.models import Customer
from django.contrib.auth.hashers import get_hasher

# Retrieve an existing user instance
user = Customer.objects.first()  # Replace with your user retrieval logic

# Get the hasher used for the password
hasher = get_hasher(user.password)

# Print the hasher algorithm
print(hasher.algorithm)