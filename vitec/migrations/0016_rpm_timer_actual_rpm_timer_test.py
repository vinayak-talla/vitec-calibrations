# Generated by Django 5.1.4 on 2025-01-24 23:57

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vitec', '0015_service_order_additional_contact_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='rpm',
            name='timer_actual',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.DurationField(), blank=True, default=list, size=None),
        ),
        migrations.AddField(
            model_name='rpm',
            name='timer_test',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.DurationField(), blank=True, default=list, size=None),
        ),
    ]