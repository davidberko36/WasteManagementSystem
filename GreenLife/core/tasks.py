from celery import shared_task
from .models import Schedule
from datetime import date


@shared_task
def check_schedule():
    today = date.today()
    schedules = Schedule.objects.all()
    for schedule in schedules:
        if today.strftime('%A') in schedule.pickup_days:
            logger.info(f"Scheduled pickup for {schedule.customer} on {today}")
            pass
