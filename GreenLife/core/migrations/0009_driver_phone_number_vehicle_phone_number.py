# Generated by Django 5.0.2 on 2024-07-20 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_rename_drivers_license_driver_driver_license_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='phone_number',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='phone_number',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
