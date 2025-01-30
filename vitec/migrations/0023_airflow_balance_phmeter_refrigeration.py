# Generated by Django 5.1.4 on 2025-01-29 23:21

import django.contrib.postgres.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vitec', '0022_thermorpm'),
    ]

    operations = [
        migrations.CreateModel(
            name='Airflow',
            fields=[
                ('instrument_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='vitec.instrument')),
                ('airflow_type', models.CharField(max_length=100)),
                ('airflow_model', models.CharField(blank=True, default='N/A', max_length=50)),
                ('downflow', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, default=list, size=None)),
                ('inflow', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, default=list, size=None)),
                ('uv_light_test', models.CharField(max_length=10)),
                ('filter_leak_test', models.CharField(max_length=10)),
                ('pcr_airflow', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, default=list, size=None)),
                ('particle_size', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, default=list, size=None)),
            ],
            bases=('vitec.instrument',),
        ),
        migrations.CreateModel(
            name='Balance',
            fields=[
                ('instrument_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='vitec.instrument')),
                ('balance_type', models.CharField(max_length=100)),
                ('balanace_model', models.CharField(blank=True, default='N/A', max_length=50)),
                ('unit_type', models.CharField(max_length=10)),
                ('weight_test', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, default=list, size=None)),
                ('weight_actual', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, default=list, size=None)),
            ],
            bases=('vitec.instrument',),
        ),
        migrations.CreateModel(
            name='PHMeter',
            fields=[
                ('instrument_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='vitec.instrument')),
                ('pH_meter_model', models.CharField(blank=True, default='N/A', max_length=50)),
                ('unit_type', models.CharField(max_length=10)),
                ('pH4_test', models.IntegerField()),
                ('pH4_actual', models.IntegerField()),
                ('pH7_test', models.IntegerField()),
                ('pH7_actual', models.IntegerField()),
                ('pH10_test', models.IntegerField()),
                ('pH10_actual', models.IntegerField()),
            ],
            bases=('vitec.instrument',),
        ),
        migrations.CreateModel(
            name='Refrigeration',
            fields=[
                ('instrument_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='vitec.instrument')),
                ('refrigeration_type', models.CharField(max_length=100)),
                ('refrigeration_model', models.CharField(blank=True, default='N/A', max_length=50)),
            ],
            bases=('vitec.instrument',),
        ),
    ]
