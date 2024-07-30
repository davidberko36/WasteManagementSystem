# from django.core.management.base import BaseCommand
# from django.utils import timezone
# from datetime import timedelta
# import json
# from core.models import Schedule, Collection, Driver, Vehicle, Customer
#
# class Command(BaseCommand):
#     help = 'Create collection instances for due pickups automatically.'
#
#     def handle(self, *args, **options):
#         today = timezone.now().date()
#         self.stdout.write(f"Checking schedules for {today}")
#         active_schedules = Schedule.objects.filter(is_active=True)
#         for schedule in active_schedules:
#             if self.is_pickup_day(schedule, today):
#                 self.create_collection(schedule)
#
#     def is_pickup_day(self, schedule, today):
#         pickup_days = schedule.pickup_days
#         self.stdout.write(f"Pickup days for schedule {schedule.id}: {pickup_days}")
#
#         if not isinstance(pickup_days, list):
#             self.stdout.write(f"Warning: pickup_days is not a list for schedule {schedule.id}")
#             return False
#
#         day_of_week = today.strftime("%A")
#         self.stdout.write(f"Day of week: {day_of_week}")
#
#         day_of_week = today.strftime("%A").lower()
#
#         if schedule.frequency == 'daily':
#             return True
#         elif schedule.frequency == 'weekly' and day_of_week in pickup_days:
#             return True
#         elif schedule.frequency in ['biweekly', 'fortnightly']:
#             weeks_since_start = (today - schedule.start_date).days // 7
#             return weeks_since_start % 2 == 0 and day_of_week in pickup_days
#
#         return False
#
#     def create_collection(self, schedule):
#         vehicle = Vehicle.objects.first()
#         driver = vehicle.driver
#
#         collection = Collection.objects.create(
#             customer=schedule.customer,
#             driver=driver,
#             vehicle=vehicle,
#             location=schedule.customer.address,
#             status='pending'
#         )
#
#         self.stdout.write(self.style.SUCCESS(f'Created collection for {schedule.customer}'))


from django.core.management.base import BaseCommand
from django.utils import timezone
import json
from core.models import Schedule, Collection, Driver, Vehicle, Customer

class Command(BaseCommand):
    help = 'Create collection instances for due pickups automatically.'

    def handle(self, *args, **options):
        today = timezone.now().date()
        self.stdout.write(f"Checking schedules for {today}")
        active_schedules = Schedule.objects.filter(is_active=True)
        self.stdout.write(f"Found {active_schedules.count()} active schedules.")
        for schedule in active_schedules:
            self.stdout.write(f"Checking schedule {schedule.id} for customer {schedule.customer}.")
            if self.is_pickup_day(schedule, today):
                self.create_collection(schedule)
            else:
                self.stdout.write(f"Today is not a pickup day for schedule {schedule.id}.")

    def is_pickup_day(self, schedule, today):
        pickup_days = schedule.pickup_days
        self.stdout.write(f"Pickup days for schedule {schedule.id}: {pickup_days}")

        if isinstance(pickup_days, str):
            try:
                pickup_days = json.loads(pickup_days)
                self.stdout.write(f"Parsed pickup days for schedule {schedule.id}: {pickup_days}")
            except json.JSONDecodeError:
                self.stdout.write(f"Warning: Invalid JSON in pickup_days for schedule {schedule.id}")
                return False

        if not isinstance(pickup_days, list):
            self.stdout.write(f"Warning: pickup_days is not a list for schedule {schedule.id}")
            return False

        day_of_week = today.strftime("%A")
        self.stdout.write(f"Day of week: {day_of_week}")

        if schedule.frequency == 'daily':
            return True
        elif schedule.frequency == 'weekly' and day_of_week in pickup_days:
            return True
        elif schedule.frequency in ['biweekly', 'fortnightly']:
            weeks_since_start = (today - schedule.start_date).days // 7
            return weeks_since_start % 2 == 0 and day_of_week in pickup_days

        return False

    def create_collection(self, schedule):
        vehicle = Vehicle.objects.first()
        if not vehicle:
            self.stdout.write(f"No vehicles available for schedule {schedule.id}.")
            return

        driver = vehicle.Driver
        if not driver:
            self.stdout.write(f"No drivers available for vehicle {vehicle.id}.")
            return

        collection = Collection.objects.create(
            customer=schedule.customer,
            driver=driver,
            vehicle=vehicle,
            location=schedule.customer.address,
            status='pending'
        )

        self.stdout.write(self.style.SUCCESS(f'Created collection for {schedule.customer} with collection ID {collection.id}'))

