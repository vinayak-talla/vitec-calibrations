from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import *
from .utils import load_instrument_types
from .models import Institution


def get_paginated_page_range(page_obj):
    total_pages = page_obj.paginator.num_pages
    page_range = []
    if total_pages <= 4:
        page_range = list(range(1, total_pages + 1))
    else:
        curr = page_obj.number
        prev = curr-1
        next = curr+1
        
        page_range.append(1)

        if prev-1 > 1:
            page_range.append('...')

        if curr == total_pages:
            page_range.append(total_pages-2)

        if prev > 1:
            page_range.append(prev)
        
        if curr != 1 and curr != total_pages:
            page_range.append(curr)

        if next < total_pages:
            page_range.append(next)
        
        if curr == 1:
            page_range.append(3)
        
        if total_pages-next > 1:
            page_range.append('...')
        
        page_range.append(total_pages)

    return page_range



def parse_phone_number(phone_number, form):
    phone_part1 = phone_number[:3] if len(phone_number) >= 3 else phone_number[:len(phone_number)]
    phone_part2 = phone_number[3:6] if len(phone_number) >= 6 else phone_number[3:len(phone_number)]
    phone_part3 = phone_number[6:] if len(phone_number) >= 7 else ''

    context = {
        'form': form,
        'phone_part1': phone_part1,
        'phone_part2': phone_part2,
        'phone_part3': phone_part3
    }

    return context

def parse_array_fields(arr_str):
    res_arr = []
    if arr_str:
        for val in arr_str.split(","):
            res_arr.append(val)
    return res_arr

def add_instrument_type(instrument_form, parent_instrument, request):
    instrument = instrument_form.save(commit=False)
    instrument.id = parent_instrument.id  # Link with parent
    instrument.instrument_type = parent_instrument.instrument_type
    instrument.make = parent_instrument.make
    instrument.notes = parent_instrument.notes
    instrument.institution = parent_instrument.institution
    instrument.save()

def find_instrument_type(instrument_form, request):

    # Save the parent Instrument instance
    parent_instrument = instrument_form.save(commit=False)
    instrument_type = instrument_form.cleaned_data['instrument_type']
    context = {'instrument_form': instrument_form}

     # Handle child models based on type
    if instrument_type == 'Pipette':
        form = PipetteForm(request.POST)
        context['pipette_form']=  form
    elif instrument_type == 'RPM':
        print(request.POST)
        form = RPMForm(request.POST)
        print(form)
        context['rpm_form']=  form
        context['rpm_test_values'] = parse_array_fields(request.POST.get('rpm_test', ''))
        context['rpm_actual_values'] = parse_array_fields(request.POST.get('rpm_actual', ''))  
        context['rpm_timer_test_values'] = parse_array_fields(request.POST.get('timer_test', ''))
        context['rpm_timer_actual_values'] = parse_array_fields(request.POST.get('timer_actual', ''))    

    elif instrument_type == 'Temperature':
        form = TemperatureForm(request.POST)
        context['temperature_test_values'] = parse_array_fields(request.POST.get('temperature_test', ''))
        context['temperature_actual_values'] = parse_array_fields(request.POST.get('temperature_actual', ''))  
        context['temperature_form']=  form
    
    elif instrument_type == 'Microscope':
        form = MicroscopeForm(request.POST)
        context['microscope_form'] = form
    elif instrument_type == 'Timer':
        form = TimerForm(request.POST)
        context['timer_test_values'] = parse_array_fields(request.POST.get('timer_test', ''))
        context['timer_actual_values'] = parse_array_fields(request.POST.get('timer_actual', '')) 
        context['timer_form'] = form
    elif instrument_type == 'ThermoRPM':
        form = ThermoRPMForm(request.POST)
        context['thermoRPM_form']=  form
        context['thermoRPM_rpm_test_values'] = parse_array_fields(request.POST.get('rpm_test', ''))
        context['thermoRPM_rpm_actual_values'] = parse_array_fields(request.POST.get('rpm_actual', ''))  
        context['thermoRPM_timer_test_values'] = parse_array_fields(request.POST.get('timer_test', ''))
        context['thermoRPM_timer_actual_values'] = parse_array_fields(request.POST.get('timer_actual', ''))  
        context['thermoRPM_temperature_test_values'] = parse_array_fields(request.POST.get('temperature_test', ''))
        context['thermoRPM_temperature_actual_values'] = parse_array_fields(request.POST.get('temperature_actual', ''))
    elif instrument_type == 'Balance':
        print(request.POST)
        form = BalanceForm(request.POST)
        print(form)
        context['weight_test_values'] = parse_array_fields(request.POST.get('weight_test', ''))
        context['weight_actual_values'] = parse_array_fields(request.POST.get('weight_actual', '')) 
        context['balance_form'] = form
    elif instrument_type == 'pH Meter':
        form = PHMeterForm(request.POST)
        context['pH_meter_form'] = form
    elif instrument_type == 'Airflow':
        form = AirflowForm(request.POST)
        context['downflow_values'] = parse_array_fields(request.POST.get('downflow', ''))
        context['inflow_values'] = parse_array_fields(request.POST.get('inflow', '')) 
        context['pcr_airflow_values'] = parse_array_fields(request.POST.get('pcr_airflow', '')) 
        context['particle_size_values'] = parse_array_fields(request.POST.get('particle_size', '')) 
        context['airflow_form'] = form
    elif instrument_type == 'Refrigeration':
        print(request.POST)
        form = RefrigerationForm(request.POST)
        context['refrigeration_form'] = form  

    if form.is_valid():
            add_instrument_type(form,parent_instrument,request)
            return (True,context)
    else:
        return (False,context)

def form_not_valid(request, context):
    messages.error(request, 'There was an error with your submission. Please correct the errors below.')
    context.update(load_instrument_types())
    context["institutions"] = Institution.objects.all()

    # Map URLs or view names to templates
    template_mapping = {
        'add-instrument': 'add-instrument.html',
        'edit-instrument': 'edit-instrument.html',
        'add-instrument-service-order': 'add-instrument-service-order.html'
    }

    view_name = request.resolver_match.view_name
    template_name = template_mapping.get(view_name)
    
    return render(request, template_name, context)

def add_instrument_valid(request, instrument_id):
    messages.success(request, f"Instrument ID: '{instrument_id}' has been successfully added.")
    if 'save_and_add_another' in request.POST:
        return redirect('add-instrument')
    return redirect('view-instruments')


def edit_instrument_post(request, instrument):
    context = {}
    instrument_form = InstrumentForm(request.POST, instance=instrument)
    if instrument.instrument_type == "Pipette":
        instrument = instrument.pipette
        form = PipetteForm(request.POST, instance=instrument)
        context["pipette_form"] = form
    elif instrument.instrument_type == "RPM":
        instrument = instrument.rpm
        form = RPMForm(request.POST, instance=instrument)
        context["rpm_form"] = form
        context['rpm_test_values'] = instrument.rpm_test
        context['rpm_actual_values'] = instrument.rpm_actual
        context['rpm_timer_test_values'] = instrument.timer_test
        context['rpm_timer_actual_values'] = instrument.timer_actual
    elif instrument.instrument_type == "Temperature":
        instrument = instrument.temperature
        form = TemperatureForm(request.POST, instance=instrument)
        context['temperature_test_values'] = instrument.temperature_test
        context['temperature_actual_values'] = instrument.temperature_actual
        context["temperature_form"] = form
    elif instrument.instrument_type == 'Microscope':
        instrument = instrument.microscope
        form = MicroscopeForm(request.POST, instance=instrument)
        context['microscope_form'] = form
    elif instrument.instrument_type == 'Timer':
        instrument = instrument.timer
        form = TimerForm(request.POST, instance=instrument)
        context['timer_test_values'] = instrument.timer_test
        context['timer_actual_values'] = instrument.timer_actual
        context['timer_form'] = form
    elif instrument.instrument_type == 'ThermoRPM':
        instrument = instrument.thermorpm
        form = ThermoRPMForm(request.POST, instance=instrument)
        context['thermoRPM_form']=  form
        context['thermoRPM_rpm_test_values'] = instrument.rpm_test
        context['thermoRPM_rpm_actual_values'] = instrument.rpm_actual
        context['thermoRPM_timer_test_values'] =  instrument.timer_test
        context['thermoRPM_timer_actual_values'] = instrument.timer_actual
        context['thermoRPM_temperature_test_values'] = instrument.temperature_test
        context['thermoRPM_temperature_actual_values'] = instrument.temperature_actual
    elif instrument.instrument_type == 'Balance':
        instrument = instrument.balance
        form = BalanceForm(request.POST, instance=instrument)
        context['weight_test_values'] = instrument.weight_test
        context['weight_actual_values'] = instrument.weight_actual
        context['balance_form'] = form
    elif instrument.instrument_type == 'pH Meter':
        instrument = instrument.phmeter
        form = PHMeterForm(request.POST, instance=instrument)
        context['pH_meter_form'] = form
    elif instrument.instrument_type == 'Airflow':
        instrument = instrument.airflow
        form = AirflowForm(request.POST, instance=instrument)
        context['downflow_values'] = instrument.downflow
        context['inflow_values'] = instrument.inflow
        context['pcr_airflow_values'] = instrument.pcr_airflow
        context['particle_size_values'] = instrument.particle_size
        context['airflow_form'] = form
    elif instrument.instrument_type == 'Refrigeration':
        instrument = instrument.refrigeration
        form = RefrigerationForm(request.POST, instance=instrument)
        context['refrigeration_form'] = form  

    if instrument_form.is_valid() and form.is_valid():
        parent = instrument_form.save(commit=False)
        child = form.save(commit=False)
        child.id = parent.id  # Link with parent
        child.instrument_type = parent.instrument_type
        child.make = parent.make
        child.notes = parent.notes
        child.institution = parent.institution
        child.save()
        messages.success(request, f"Instrument '{instrument.id}' has been successfully updated.")
        return (True,context)

    else:
        context['instrument_form'] = instrument_form
        messages.error(request, 'There was an error with your update. Please correct the errors below.')
        return(False,context)

def edit_instrument_get(instrument):
    context = {}
    instrument_form = InstrumentForm(instance=instrument)
    if instrument.instrument_type == "Pipette":
        instrument = instrument.pipette
        context["pipette_form"] = PipetteForm(instance=instrument)
    elif instrument.instrument_type == "RPM":
        instrument = instrument.rpm
        context["rpm_form"] = RPMForm(instance=instrument)
        context['rpm_test_values'] = instrument.rpm_test
        context['rpm_actual_values'] = instrument.rpm_actual
        context['rpm_timer_test_values'] = instrument.timer_test
        context['rpm_timer_actual_values'] = instrument.timer_actual
    elif instrument.instrument_type == "Temperature":
        instrument = instrument.temperature
        context['temperature_test_values'] = instrument.temperature_test
        context['temperature_actual_values'] = instrument.temperature_actual
        context["temperature_form"] = TemperatureForm(instance=instrument)
    elif instrument.instrument_type == 'Microscope':
        instrument = instrument.microscope
        context['microscope_form'] = MicroscopeForm(instance=instrument)
    elif instrument.instrument_type == 'Timer':
        instrument = instrument.timer
        context['timer_test_values'] = instrument.timer_test
        context['timer_actual_values'] = instrument.timer_actual
        context['timer_form'] = TimerForm(instance=instrument)
    elif instrument.instrument_type == 'ThermoRPM':
        instrument = instrument.thermorpm
        form = ThermoRPMForm(instance=instrument)
        context['thermoRPM_form']=  form
        context['thermoRPM_rpm_test_values'] = instrument.rpm_test
        context['thermoRPM_rpm_actual_values'] = instrument.rpm_actual
        context['thermoRPM_timer_test_values'] =  instrument.timer_test
        context['thermoRPM_timer_actual_values'] = instrument.timer_actual
        context['thermoRPM_temperature_test_values'] = instrument.temperature_test
        context['thermoRPM_temperature_actual_values'] = instrument.temperature_actual
    elif instrument.instrument_type == 'Balance':
        instrument = instrument.balance
        form = BalanceForm(instance=instrument)
        context['weight_test_values'] = instrument.weight_test
        context['weight_actual_values'] = instrument.weight_actual
        context['balance_form'] = form
    elif instrument.instrument_type == 'pH Meter':
        instrument = instrument.phmeter
        form = PHMeterForm(instance=instrument)
        context['pH_meter_form'] = form
    elif instrument.instrument_type == 'Airflow':
        instrument = instrument.airflow
        form = AirflowForm(instance=instrument)
        context['downflow_values'] = instrument.downflow
        context['inflow_values'] = instrument.inflow
        context['pcr_airflow_values'] = instrument.pcr_airflow
        context['particle_size_values'] = instrument.particle_size
        context['airflow_form'] = form
    elif instrument.instrument_type == 'Refrigeration':
        instrument = instrument.refrigeration
        form = RefrigerationForm(instance=instrument)
        context['refrigeration_form'] = form  

    context['instrument_form'] = instrument_form

    return context
