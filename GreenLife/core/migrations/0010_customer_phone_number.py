# Generated by Django 5.0.2 on 2024-07-20 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_driver_phone_number_vehicle_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='phone_number',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
