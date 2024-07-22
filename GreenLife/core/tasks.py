# from celery import shared_task
# from .models import Schedule
# from datetime import date
#
#
# @shared_task
# def check_schedule():
#     today = date.today()
#     schedules = Schedule.objects.all()
#     for schedule in schedules:
#         if today.strftime('%A') in schedule.pickup_days:
#             logger.info(f"Scheduled pickup for {schedule.customer} on {today}")
#             pass


from celery import shared_task
from .models import Schedule
from datetime import date
import json
import logging

logger = logging.getLogger(__name__)

@shared_task
def check_schedule(schedule_id):
    try:
        schedule = Schedule.objects.get(id=schedule_id)
        today = date.today()
        pickup_days = json.loads(schedule.pickup_days)
        if today.strftime('%A') in pickup_days:
            logger.info(f"Scheduled pickup for {schedule.customer} on {today}")
            # Add your pickup logic here
    except Schedule.DoesNotExist:
        logger.error(f"Schedule with id {schedule_id} not found")
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON in pickup_days for schedule {schedule_id}")