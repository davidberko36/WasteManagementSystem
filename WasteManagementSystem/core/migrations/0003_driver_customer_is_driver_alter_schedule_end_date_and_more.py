# Generated by Django 5.0.2 on 2024-04-22 04:25

import core.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_schedule'),
    ]

    operations = [
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('other_names', models.CharField(max_length=60)),
                ('last_name', models.CharField(max_length=30, null=True)),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('driver_license_number', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=255)),
                ('date_of_birth', models.DateField()),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_driver', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='customer',
            name='is_driver',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='end_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='start_date',
            field=models.DateField(),
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('status', models.CharField(choices=[(core.models.PickUpStatus['PENDING'], 'Pending'), (core.models.PickUpStatus['COMPLETED'], 'Completed')], max_length=13)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.customer')),
                ('schedule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.schedule')),
            ],
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue_type', models.CharField(choices=[('missed pickups', 'Missed pickups'), ('poor service', 'Poor service')], default='missed pickups', max_length=30)),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[(core.models.IssueStatus['PENDING'], 'Pending'), (core.models.IssueStatus['RESOLVED'], 'Resolved')], max_length=13)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.customer')),
            ],
        ),
    ]