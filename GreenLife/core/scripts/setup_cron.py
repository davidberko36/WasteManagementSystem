from crontab import CronTab

cron = CronTab(user=True)
job = cron.new(command='cd /mnt/c/Users/David\\ Berko/Desktop/WasteManagementSystem/GreenLife && .venv/Scripts/activate && python manage.py create_collections', comment='Django management command')
job.setall('0 0 * * *')  # Runs daily at midnight
cron.write()
