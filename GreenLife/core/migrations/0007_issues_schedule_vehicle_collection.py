# Generated by Django 5.0.2 on 2024-06-15 01:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_customer_driver'),
    ]

    operations = [
        migrations.CreateModel(
            name='Issues',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue', models.CharField(choices=[('missed pickup', 'Missed pickup'), ('poor service', 'Poor service')], max_length=40)),
                ('details', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('resolved', 'Resolved'), ('withdrawn', 'Withdrawn')], default='Pending', max_length=15)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frequency', models.CharField(choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('biweekly', 'Biweekly'), ('fortnightly,', 'Fortnightly')], max_length=20)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('license_plate', models.CharField(max_length=30)),
                ('capacity', models.PositiveIntegerField()),
                ('Driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.driver')),
            ],
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=30)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='Pending', max_length=20)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.customer')),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.driver')),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.vehicle')),
            ],
        ),
    ]
