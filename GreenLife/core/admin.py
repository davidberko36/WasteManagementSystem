from django.contrib import admin
from .models import User, Customer, Driver, Schedule, Collection, Issues

# Register your models here.
admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Driver)
admin.site.register(Schedule)
admin.site.register(Collection)
admin.site.register(Issues)