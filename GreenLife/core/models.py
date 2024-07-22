from django.db import models
from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone


# Create your models here.
class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("You have not provided a valid email address")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)

    def create_driver(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, blank=True, default='')
    last_name = models.CharField(max_length=255, blank=False, null=False)
    other_names = models.CharField(max_length=255, blank=False, null=False)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Customer(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=30, blank=True, null=True)
    username = models.CharField(max_length=30, null=False, blank=False)
    address = models.CharField(max_length=30, null=False, blank=False)

    def __str__(self):
        return self.user.email


class Driver(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=30, null=True, blank=True)
    username = models.CharField(max_length=30, null=False, blank=False)
    driver_license = models.CharField(max_length=30, null=False, blank=False)


class Vehicle(models.Model):
    license_plate = models.CharField(max_length=30, null=False, blank=False)
    phone_number = models.CharField(max_length=30, null=True, blank=True)
    capacity = models.PositiveIntegerField()
    Driver = models.ForeignKey('Driver', on_delete=models.CASCADE)


class Schedule(models.Model):
    PICKUP_FREQUENCY = (
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('biweekly', 'Biweekly'),
        ('fortnightly,', 'Fortnightly')
    )

    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, null=False, blank=False)
    frequency = models.CharField(max_length=20, choices=PICKUP_FREQUENCY, null=False, blank=False)
    start_date = models.DateField(blank=False, null=False)
    pickup_days = models.JSONField(null=False, blank=False, default=dict)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.customer} - {self.frequency} starting {self.start_date}"


class Collection(models.Model):
    STATUS = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, blank=False, null=False)
    driver = models.ForeignKey('Driver', on_delete=models.CASCADE, blank=False, null=False)
    vehicle = models.ForeignKey('Vehicle', on_delete=models.CASCADE, blank=False, null=False)
    location = models.CharField(max_length=30, blank=False, null=False)
    status = models.CharField(max_length=20, choices=STATUS, null=False, blank=False, default='Pending')


class Issues(models.Model):
    ISSUES = (
        ('missed pickup', 'Missed pickup'),
        ('poor service', 'Poor service'),
    )

    ISSUE_STATUS = (
        ('pending', 'Pending'),
        ('resolved', 'Resolved'),
        ('withdrawn', 'Withdrawn'),
    )

    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, null=False, blank=False)
    issue = models.CharField(max_length=40, choices=ISSUES, null=False, blank=False)
    details = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=15, choices=ISSUE_STATUS, null=False, blank=False, default='Pending')
