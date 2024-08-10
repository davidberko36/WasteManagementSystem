from django.contrib import admin
from .models import User, Customer, Driver, Schedule, Collection, Issues, Vehicle

# Register your models here.
admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Driver)
admin.site.register(Vehicle)
admin.site.register(Schedule)
# admin.site.register(Collection)
admin.site.register(Issues)


class CollectionAdmin(admin.ModelAdmin):
    list_display = ['customer', 'driver', 'status', 'location']
    list_filter = ['status', 'driver']
    search_fields = ['customer__username', 'driver__username', 'location']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(driver=request.user.driver)

    def has_change_permission(self, request, obj=None):
        if not obj:
            return True
        return obj.driver == request.user.driver

    def has_delete_permission(self, request, obj=None):
        if not obj:
            return False
        return obj.driver == request.user.driver


admin.site.register(Collection, CollectionAdmin)
