from django.db import models
from django.contrib.postgres.fields import ArrayField


class Institution(models.Model):
    name = models.CharField(primary_key=True,max_length=150)
    contact = models.CharField(max_length=120)
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=10)
    email = models.EmailField(max_length=100)

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
    rpm_test = models.CharField(max_length=200, blank=True)
    rpm_actual = models.CharField(max_length=200, blank=True)
    def __str__(self):
        return f"{self.id} {self.rpm_test} {self.rpm_actual}"

class Temperature(Instrument):
    temperature_type = models.CharField(max_length=100)
    temperature_test = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    temperature_actual = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    humidity_test = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    humidity_actual = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    def __str__(self):
        return f"{self.id} {self.temperature_type} {self.temperature_test} {self.temperature_actual}"

class Service_Order(models.Model):
    so_number = models.AutoField(primary_key=True)
    date = models.DateField(auto_now_add=True)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    instrument_list = ArrayField(models.CharField(max_length=50))
    def __str__(self):
        return f"{self.so_number} {self.date} {self.institution}"

