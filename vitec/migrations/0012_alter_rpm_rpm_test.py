# Generated by Django 5.1.2 on 2024-12-21 01:23

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vitec', '0011_alter_rpm_rpm_actual_alter_rpm_rpm_test'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rpm',
            name='rpm_test',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, default=list, size=None),
        ),
    ]
