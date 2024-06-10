from django.contrib import admin
from .models import Customer, Driver, Vehicle, Schedule, Issue, Collection

# Register your models here.
admin.site.register(Customer)
admin.site.register(Driver)
admin.site.register(Vehicle)
admin.site.register(Schedule)
admin.site.register(Issue)
admin.site.register(Collection)
