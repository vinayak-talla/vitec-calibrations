from django.db import models
from django.contrib.postgres.fields import ArrayField


class Institution(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    department = models.CharField(max_length=150, blank=True)
    contact = models.CharField(max_length=120)
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=10)
    email = models.EmailField(max_length=100)
    class Meta:
        # Ensure no duplicate combinations of name and contact
        unique_together = ['name', 'contact']

    def __str__(self):
        return f"{self.name}"
    
class Instrument(models.Model):
    id = models.CharField(primary_key=True,max_length=50)
    instrument_type = models.CharField(max_length=75)
    make = models.CharField(max_length=50)
    notes = models.TextField(max_length=300, blank=True)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.instrument_type} {self.id}"

class Pipette(Instrument):
    pipette_type = models.CharField(max_length=100)
    volume = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.id} {self.volume}"

class RPM(Instrument):
    rpm_type = models.CharField(max_length=100)
    rpm_model = models.CharField(max_length=50, blank=True, default="N/A")
    rpm_test = ArrayField(
        models.IntegerField(
            error_messages={
                'invalid': 'Please enter a valid whole number for each RPM Test value.'
            }
        ),
        blank=True,   # Allows the field to be blank in forms
        default=list  # Ensures an empty list is used if no value is provided
    )
    rpm_actual = ArrayField(
        models.IntegerField(
            error_messages={
                'invalid': 'Please enter a valid whole number for each RPM Actual value.'
            }
        ),
        blank=True,   # Allows the field to be blank in forms
        default=list  # Ensures an empty list is used if no value is provided
    )
    timer_test = ArrayField(
        models.DurationField(),
        blank=True,   # Allows the field to be blank in forms
        default=list  # Ensures an empty list is used if no value is provided
    )
    timer_actual = ArrayField(
        models.DurationField(),
        blank=True,   # Allows the field to be blank in forms
        default=list  # Ensures an empty list is used if no value is provided
    )
    def __str__(self):
        return f"{self.id} {self.rpm_test} {self.rpm_actual}"
    def save(self, *args, **kwargs):
        if not self.rpm_model.strip():  # Replace empty or whitespace-only values
            self.rpm_model = "N/A"
        super().save(*args, **kwargs)

class Temperature(Instrument):
    temperature_type = models.CharField(max_length=100)
    temperature_model = models.CharField(max_length=50, blank=True, default="N/A")
    temperature_test = ArrayField(
        models.DecimalField(max_digits=6, decimal_places=3),
        blank=True,   # Allows the field to be blank in forms
        default=list  # Ensures an empty list is used if no value is provided
    )
    temperature_actual = ArrayField(
        models.DecimalField(max_digits=6, decimal_places=3),
        blank=True,   # Allows the field to be blank in forms
        default=list  # Ensures an empty list is used if no value is provided
    )
    humidity_test = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    humidity_actual = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    def __str__(self):
        return f"{self.id} {self.temperature_type} {self.temperature_test} {self.temperature_actual}"
    def save(self, *args, **kwargs):
        if not self.temperature_model.strip():  # Replace empty or whitespace-only values
            self.temperature_model = "N/A"
        super().save(*args, **kwargs)
    
class Microscope(Instrument):
    microscope_type = models.CharField(max_length=100)
    microscope_model = models.CharField(max_length=50, blank=True, default="N/A")
    def save(self, *args, **kwargs):
        if not self.microscope_model.strip():  # Replace empty or whitespace-only values
            self.microscope_model = "N/A"
        super().save(*args, **kwargs)

class Timer(Instrument):
    timer_type = models.CharField(max_length=100)
    timer_model = models.CharField(max_length=50, blank=True, default="N/A")
    timer_test = ArrayField(
        models.DurationField(),
        blank=True,   # Allows the field to be blank in forms
        default=list  # Ensures an empty list is used if no value is provided
    )
    timer_actual = ArrayField(
        models.DurationField(),
        blank=True,   # Allows the field to be blank in forms
        default=list  # Ensures an empty list is used if no value is provided
    )
    def save(self, *args, **kwargs):
        if not self.timer_model.strip():  # Replace empty or whitespace-only values
            self.timer_model = "N/A"
        super().save(*args, **kwargs)

class ThermoRPM(Instrument):
    thermoRPM_type = models.CharField(max_length=100)
    thermoRPM_model = models.CharField(max_length=50, blank=True, default="N/A")
    rpm_test = ArrayField(
        models.IntegerField(),
        blank=True,   # Allows the field to be blank in forms
        default=list  # Ensures an empty list is used if no value is provided
    )
    rpm_actual = ArrayField(
        models.IntegerField(),
        blank=True,   # Allows the field to be blank in forms
        default=list  # Ensures an empty list is used if no value is provided
    )
    temperature_test = ArrayField(
        models.DecimalField(max_digits=6, decimal_places=3),
        blank=True,   # Allows the field to be blank in forms
        default=list  # Ensures an empty list is used if no value is provided
    )
    temperature_actual = ArrayField(
        models.DecimalField(max_digits=6, decimal_places=3),
        blank=True,   # Allows the field to be blank in forms
        default=list  # Ensures an empty list is used if no value is provided
    )
    timer_test = ArrayField(
        models.DurationField(),
        blank=True,   # Allows the field to be blank in forms
        default=list  # Ensures an empty list is used if no value is provided
    )
    timer_actual = ArrayField(
        models.DurationField(),
        blank=True,   # Allows the field to be blank in forms
        default=list  # Ensures an empty list is used if no value is provided
    )
    def save(self, *args, **kwargs):
        if not self.thermoRPM_model.strip():  # Replace empty or whitespace-only values
            self.thermoRPM_model = "N/A"
        super().save(*args, **kwargs)

class Balance(Instrument):
    balance_type = models.CharField(max_length=100)
    balance_model = models.CharField(max_length=50, blank=True, default="N/A")
    unit_type = models.CharField(max_length=10)
    weight_test = ArrayField(
        models.IntegerField(),
        blank=True,   # Allows the field to be blank in forms
        default=list  # Ensures an empty list is used if no value is provided
    )
    weight_actual = ArrayField(
        models.IntegerField(),
        blank=True,   # Allows the field to be blank in forms
        default=list  # Ensures an empty list is used if no value is provided
    )
    def save(self, *args, **kwargs):
        if not self.balance_model.strip():  # Replace empty or whitespace-only values
            self.balance_model = "N/A"
        super().save(*args, **kwargs)

class PHMeter(Instrument):
    pH_meter_model = models.CharField(max_length=50, blank=True, default="N/A")
    pH4_test = models.IntegerField(null=True, blank=True)
    pH4_actual = models.IntegerField(null=True, blank=True)
    pH7_test = models.IntegerField(null=True, blank=True)
    pH7_actual = models.IntegerField(null=True, blank=True)
    pH10_test = models.IntegerField(null=True, blank=True)
    pH10_actual = models.IntegerField(null=True, blank=True)
    def save(self, *args, **kwargs):
        if not self.pH_meter_model.strip():  # Replace empty or whitespace-only values
            self.pH_meter_model = "N/A"
        super().save(*args, **kwargs)

class Airflow(Instrument):
    airflow_type = models.CharField(max_length=100)
    airflow_model = models.CharField(max_length=50, blank=True, default="N/A")
    downflow = ArrayField(
        models.IntegerField(),
        blank=True,   # Allows the field to be blank in forms
        default=list  # Ensures an empty list is used if no value is provided
    )
    inflow = ArrayField(
        models.IntegerField(),
        blank=True,   # Allows the field to be blank in forms
        default=list  # Ensures an empty list is used if no value is provided
    )
    uv_light_test = models.CharField(max_length=10, blank=True)
    filter_leak_test = models.CharField(max_length=10, blank=True)
    pcr_airflow = ArrayField(
        models.IntegerField(),
        blank=True,   # Allows the field to be blank in forms
        default=list  # Ensures an empty list is used if no value is provided
    )
    particle_size = ArrayField(
        models.IntegerField(),
        blank=True,   # Allows the field to be blank in forms
        default=list  # Ensures an empty list is used if no value is provided
    )
    def save(self, *args, **kwargs):
        if not self.airflow_model.strip():  # Replace empty or whitespace-only values
            self.airflow_model = "N/A"
        super().save(*args, **kwargs)


class Refrigeration(Instrument):
    refrigeration_type = models.CharField(max_length=100)
    refrigeration_model = models.CharField(max_length=50, blank=True, default="N/A")
    voltage = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True)
    temperature1_test = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    temperature1_actual = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    temperature2_test = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    temperature2_actual = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    def save(self, *args, **kwargs):
        if not self.refrigeration_model.strip():  # Replace empty or whitespace-only values
            self.refrigeration_model = "N/A"
        super().save(*args, **kwargs)


class Service_Order(models.Model):
    so_number = models.AutoField(primary_key=True)
    date = models.DateField(auto_now_add=True)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    instrument_list = ArrayField(models.CharField(max_length=50))
    additional_contact = models.CharField(max_length=120, blank=True)

    def __str__(self):
        return f"{self.so_number} {self.date} {self.institution}"

