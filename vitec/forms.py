from django import forms
from .models import Institution, Instrument, Pipette, RPM, Temperature

class InstitutionForm(forms.ModelForm):
    class Meta:
        model = Institution
        fields = ['name', 'contact', 'address', 'phone_number', 'email']
        labels = {
            'name': 'Institution Name',
            'contact': 'Contact Name',
            'address': 'Address',
            'phone_number': 'Phone Number',
            'email': 'Email'
        }
        error_messages = {
            'name': {'unique': 'This institution name already exists.'},
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

        # Check for duplicate institution names
        if name and Institution.objects.filter(name=name).exclude(pk=self.instance.pk).exists():
            self.add_error('name', 'This institution has already been added.')




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
    class Meta:
        model = RPM
        fields = ['rpm_type', 'rpm_test', 'rpm_actual']

class TemperatureForm(forms.ModelForm):
    class Meta:
        model = Temperature
        fields = ['temperature_type', 'temperature_test', 'temperature_actual', 'humidity_test', 'humidity_actual']