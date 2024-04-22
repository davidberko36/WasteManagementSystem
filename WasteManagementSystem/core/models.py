from typing import Any
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from enum import Enum

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, username, other_names, last_name, date_of_birth, mobile_phone, password=None, is_driver=False, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            other_names=other_names,
            last_name=last_name,
            date_of_birth=date_of_birth,
            mobile_phone=mobile_phone,
            is_driver=is_driver,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, other_names, last_name, date_of_birth, mobile_phone, password, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_admin=True.')
        return self.create_user(email, username, other_names, last_name, date_of_birth, mobile_phone, password, **extra_fields)

class Customer(AbstractBaseUser):
    CUSTOMER_TYPES = [
        ('domestic', 'Domestic'),
        ('business', 'Business'),
    ]

    customer_id = models.AutoField(primary_key=True)
    other_names = models.CharField(max_length=60, blank=False, null=False)
    last_name = models.CharField(max_length=30, blank=False, null=False)
    address = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    mobile_phone = models.CharField(max_length=15, blank=False, null=False)
    password = models.CharField(max_length=255, blank=False, null=False)
    username = models.CharField(max_length=30, blank=False, null=False, unique=True)
    date_of_birth = models.DateField(blank=False, null=False)
    user_type = models.CharField(max_length=20, choices=CUSTOMER_TYPES, default=CUSTOMER_TYPES[0][0]) 
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_driver = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'other_names', 'last_name', 'date_of_birth', 'mobile_phone']








    def __str__(self):
        return f"{self.other_names} {self.last_name}"

    



class Driver(AbstractBaseUser):
    other_names= models.CharField(max_length=60, blank=False, null=False)
    last_name = models.CharField(max_length=30, blank=False, null=True)
    email = models.EmailField(verbose_name = 'email address', unique=True)
    driver_license_number = models.CharField(max_length=20, blank=False, null=False)
    password = models.CharField(max_length=255, blank=False, null=False)
    date_of_birth = models.DateField(blank=False, null=False)
    is_active= models.BooleanField(default=True)
    is_admin= models.BooleanField(default=False)
    is_driver = models.BooleanField(default=True)


    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return f"{self.other_names} {self.last_name}"
    




class Vehicle(models.Model):
    License_plate_number= models.CharField(max_length=11, null=False)
    Driver = models.ForeignKey(Driver)

    



PICKUP_DAYS = (
        ('sunday', 'Sunday'),
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday')
)



class PickUpDaysField(models.CharField):
    description = _('A list of the days of the week')


    def __init__(self, *args, **kwargs):
        kwargs.setdefault('choices', PICKUP_DAYS)
        super(PickUpDaysField, self).__init__(*args, **kwargs)


    def to_python(self, value):
        if isinstance(value, list):
            return value
        
        return value.split(',')
    


    def get_prep_value(self, value):
        return ','.join(value)



    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_prep_value(value)






class Schedule(models.Model):
    FREQUENCY_CHOICES = [
        ('weekly', 'Weekly'),
        ('bi-weekly', 'Bi-weekly'),
        ('daily', 'Daily')
    ]

    
    start_date = models.DateField(blank=False, null=False)
    end_date = models.DateField(blank=False, null=False)
    Customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    location = models.CharField(max_length = 30, blank=False, null=False)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default=FREQUENCY_CHOICES[0][0])
    days = PickUpDaysField(max_length=50, blank=True)

    def __str__(self):
        return f'Schedule for {Customer.other_names}'
    
class IssueStatus(Enum):
    PENDING = 'Pending'
    RESOLVED = 'Resolved'



class Issue(models.Model):
    ISSUE_TYPE = [
        ('missed pickups', 'Missed pickups'),
        ('poor service', 'Poor service')
    ]



    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    issue_type = models.CharField(max_length=30, choices=ISSUE_TYPE, default=ISSUE_TYPE[0][0])
    description = models.TextField()
    status = models.CharField(max_length=13, choices=[(tag, tag.value) for tag in IssueStatus])
    


class PickUpStatus(Enum):
    PENDING = 'Pending'
    COMPLETED = 'Completed'








class Collection(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    date = models.DateTimeField()
    status = models.CharField(max_length=13, choices=[(tag, tag.value) for tag in PickUpStatus])