from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import PipetteForm, RPMForm, TemperatureForm, InstrumentForm
from django.utils.timezone import now
from .models import Institution, Instrument
from django.core.paginator import Paginator
from .utils import load_instrument_types



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

def parse_rpm_fields(rpm_test, rpm_actual):
    rpm_test_values = []
    rpm_actual_values = []
    if rpm_test:
        for rpm in rpm_test.split(","):
            rpm_test_values.append(rpm)
    if rpm_actual:
        for rpm in rpm_actual.split(","):
            rpm_actual_values.append(rpm)
    return {'rpm_test_values': rpm_test_values, 'rpm_actual_values': rpm_actual_values}


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
        form = RPMForm(request.POST)
        context['rpm_form']=  form
        context.update(parse_rpm_fields(request.POST.get('rpm_test', ''), request.POST.get('rpm_actual', '')))
    
    elif instrument_type == 'Temperature':
        form = TemperatureForm(request.POST)
        context['temperature_form']=  form

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
    elif instrument.instrument_type == "Temperature":
        instrument = instrument.temperature
        form = TemperatureForm(request.POST, instance=instrument)
        context["temperature_form"] = form

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
    elif instrument.instrument_type == "Temperature":
        instrument = instrument.temperature
        context["temperature_form"] = TemperatureForm(instance=instrument)

    context['instrument_form'] = instrument_form

    return context
