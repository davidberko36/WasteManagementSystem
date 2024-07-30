from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from django.core.management import call_command
from django.conf import settings
import sys

# def start():
#     scheduler = BackgroundScheduler()
#     scheduler.add_jobstore(DjangoJobStore(), "default")
#
#     @scheduler.scheduled_job('cron', hour=0, minute=0)
#     def run_create_collections():
#         call_command('create_collections')
#
#     scheduler.start()
#     print("Scheduler started...", file=sys.stdout)