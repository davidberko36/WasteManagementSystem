# Generated by Django 5.0.2 on 2024-07-29 15:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_payment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vehicle',
            name='phone_number',
        ),
    ]
