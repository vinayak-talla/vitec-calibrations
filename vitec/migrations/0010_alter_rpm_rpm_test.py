# Generated by Django 5.1.2 on 2024-12-20 23:53

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vitec', '0009_alter_rpm_rpm_actual_alter_rpm_rpm_test'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rpm',
            name='rpm_test',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), blank=True, default=list, size=None),
        ),
    ]