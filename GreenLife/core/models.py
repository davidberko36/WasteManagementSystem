from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ROLES = (
        ('admin', 'Admin'),
        ('customer', 'Customer'),
        ('driver', 'Driver'),
    )

    email = models.EmailField(unique=True)
    last_name = models.CharField(max_length=255, blank=False, null=False)
    other_names = models.CharField(max_length=255, blank=False, null=False)
    phone_number = models.CharField(max_length=20, blank=False, null=False)
    role = models.CharField(max_length=20, choices=ROLES, blank=False, null=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    address = models.CharField(max_length=100, blank=True, null=True)    # For Customers only.
    driver_license = models.CharField(max_length=100, blank=True, null=True)    # For Drivers only

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['last_name', 'other_names', 'role']

    objects = UserManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if self.role == 'customer' and not self.address:
            raise ValueError('Address cannot be empty.')
        if self.role == 'driver' and not self.driver_license:
            raise ValueError('License number must be provided.')


class Car(models.Model):
    License_Plate = models.CharField(max_length=10, blank=False, null=False)
    Driver = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, null=True)
    Capacity = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)

    def __str__(self):
        return self.License_Plate


class Schedule(models.Model):
    PICKUP_FREQUENCIES = (
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('biweekly', 'Biweekly'),
        ('fortnightly', 'Fortnightly'),
    )

    User = models.ForeignKey('User', on_delete=models.CASCADE, blank=False, null=False)
    Frequency = models.CharField(max_length=20, choices=PICKUP_FREQUENCIES, blank=False, null=False)
    start_date = models.DateField(blank=False, null=False)
    end_date = models.DateField(blank=False, null=False)
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)

    def __str__(self):
        return f"{self.User.last_name}'s schedule"



