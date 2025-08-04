from django import forms
from .models import *

class InstitutionForm(forms.ModelForm):
    class Meta:
        model = Institution
        fields = ['name', 'contact', 'department', 'address', 'phone_number', 'email']
        labels = {
            'name': 'Institution Name',
            'contact': 'Contact Name',
            'lab_name': 'Lab Name',
            'address': 'Address',
            'phone_number': 'Phone Number',
            'email': 'Email'
        }
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if len(phone_number) != 10:
            raise forms.ValidationError('Phone number must be exactly 10 digits.')
        if not phone_number.isdigit():
            raise forms.ValidationError('Phone number must contain only digits.')
        return phone_number

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        contact = cleaned_data.get('contact')

        # Check for duplicate institution names
        if name and contact:
            duplicate = Institution.objects.filter(
                name=name,
                contact=contact
            ).exclude(pk=self.instance.pk)

            if duplicate.exists():
                self.add_error('name', 'This institution and contact combination already exists.')
                self.add_error('contact', 'This institution and contact combination already exists.')




class InstrumentForm(forms.ModelForm):
    institution = forms.ModelChoiceField(queryset=Institution.objects.all(), required=True)
    class Meta:
        model = Instrument
        fields = ['id', 'instrument_type', 'make', 'notes', 'institution']
        error_messages = {
            'id': {'unique': 'This instrument id already exists.'},
        }

class PipetteForm(forms.ModelForm):
    class Meta:
        model = Pipette
        fields = ['pipette_type', 'volume']

class RPMForm(forms.ModelForm):
    rpm_model = forms.CharField(
        max_length=50,
        required=False,
        initial='',  # Set initial value to empty
    )
    class Meta:
        model = RPM
        fields = ['rpm_type', 'rpm_model', 'rpm_test', 'rpm_actual', 'timer_test', 'timer_actual']

class TemperatureForm(forms.ModelForm):
    temperature_model = forms.CharField(
        max_length=50,
        required=False,
        initial='',  # Set initial value to empty
    )
    class Meta:
        model = Temperature
        fields = ['temperature_type', 'temperature_model', 'temperature_test', 'temperature_actual', 'humidity_test', 'humidity_actual']

class MicroscopeForm(forms.ModelForm):
    microscope_model = forms.CharField(
        max_length=50,
        required=False,
        initial='',  # Set initial value to empty
    )
    class Meta:
        model = Microscope
        fields = ['microscope_type', 'microscope_model']

class TimerForm(forms.ModelForm):
    timer_model = forms.CharField(
        max_length=50,
        required=False,
        initial='',  # Set initial value to empty
    )
    class Meta:
        model = Timer
        fields = ['timer_type', 'timer_model', 'timer_test', 'timer_actual']

class ThermoRPMForm(forms.ModelForm):
    thermoRPM_model = forms.CharField(
        max_length=50,
        required=False,
        initial='',  # Set initial value to empty
    )
    class Meta:
        model = ThermoRPM
        fields = ['thermoRPM_type', 'thermoRPM_model', 'rpm_test', 'rpm_actual', 'temperature_test', 'temperature_actual', 'timer_test', 'timer_actual']

class BalanceForm(forms.ModelForm):
    balance_model = forms.CharField(
        max_length=50,
        required=False,
        initial='',  # Set initial value to empty
    )
    class Meta:
        model = Balance
        fields = ['balance_type', 'balance_model', 'unit_type', 'weight_test', 'weight_actual']

class PHMeterForm(forms.ModelForm):
    pH_meter_model = forms.CharField(
        max_length=50,
        required=False,
        initial='',  # Set initial value to empty
    )
    class Meta:
        model = PHMeter
        fields = ['pH_meter_model','pH4_test', 'pH4_actual','pH7_test', 'pH7_actual','pH10_test', 'pH10_actual']

class AirflowForm(forms.ModelForm):
    airflow_model = forms.CharField(
        max_length=50,
        required=False,
        initial='',  # Set initial value to empty
    )
    class Meta:
        model = Airflow
        fields = '__all__'

class RefrigerationForm(forms.ModelForm):
    refrigeration_model = forms.CharField(
        max_length=50,
        required=False,
        initial='',  # Set initial value to empty
    )
    class Meta:
        model = Refrigeration
        fields = '__all__'



class RPMValueForm(forms.ModelForm):
    class Meta:
        model = RPM
        fields = ['rpm_test', 'rpm_actual', 'timer_test', 'timer_actual']

class TemperatureValueForm(forms.ModelForm):
    class Meta:
        model = Temperature
        fields = ['temperature_test', 'temperature_actual', 'humidity_test', 'humidity_actual']

class TimerValueForm(forms.ModelForm):
    class Meta:
        model = Timer
        fields = ['timer_test', 'timer_actual']

class ThermoRPMValueForm(forms.ModelForm):
    class Meta:
        model = ThermoRPM
        fields = ['rpm_test', 'rpm_actual', 'temperature_test', 'temperature_actual', 'timer_test', 'timer_actual']

class BalanceValueForm(forms.ModelForm):
    class Meta:
        model = Balance
        fields = ['weight_test', 'weight_actual']

class PHMeterValueForm(forms.ModelForm):
    class Meta:
        model = PHMeter
        fields = ['pH4_test', 'pH4_actual','pH7_test', 'pH7_actual','pH10_test', 'pH10_actual']

class AirflowValueForm(forms.ModelForm):
    class Meta:
        model = Airflow
        fields = ['downflow', 'inflow', 'uv_light_test', 'filter_leak_test', 'pcr_airflow', 'particle_size']

class RefrigerationValueForm(forms.ModelForm):
    class Meta:
        model = Refrigeration
        fields = ['temperature1_test', 'temperature1_actual', 'temperature2_test', 'temperature2_actual', 'voltage']

class ServiceOrderForm(forms.ModelForm):
    class Meta:
        model = Service_Order
        fields = ['additional_contact']


