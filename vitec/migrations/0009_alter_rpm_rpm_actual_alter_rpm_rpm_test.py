# Generated by Django 5.1.2 on 2024-12-19 02:09

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vitec', '0008_rename_type_instrument_instrument_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rpm',
            name='rpm_actual',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, default=list, size=None),
        ),
        migrations.AlterField(
            model_name='rpm',
            name='rpm_test',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, default=list, size=None),
        ),
    ]