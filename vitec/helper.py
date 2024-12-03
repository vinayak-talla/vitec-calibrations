from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import PipetteForm, RPMForm, TemperatureForm
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
        for rpm in rpm_test.split(";"):
            rpm_test_values.append(rpm)
    if rpm_actual:
        for rpm in rpm_actual.split(";"):
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

    messages.success(request, f"Instrument ID: '{instrument.id}' has been successfully added.")

    if 'save_and_add_another' in request.POST:
                return redirect('add-instrument')
    return redirect('view-instruments')


def find_instrument_type(instrument_type, instrument_form, request):
    # Save the parent Instrument instance
    parent_instrument = instrument_form.save(commit=False)

     # Handle child models based on type
    if instrument_type == 'Pipette':
        pipette_form = PipetteForm(request.POST)
        if pipette_form.is_valid():
            return add_instrument_type(pipette_form,parent_instrument,request)
        else:
            context= {
                'pipette_form': pipette_form,
                'instrument_form': instrument_form,
            }
            return form_not_valid(request, pipette_form, context)
        
    elif instrument_type == 'RPM':
        rpm_form = RPMForm(request.POST)
        if rpm_form.is_valid():
            return add_instrument_type(rpm_form,parent_instrument,request)
        else:
            rpm_fields = parse_rpm_fields(request.POST.get('rpm_test', ''), request.POST.get('rpm_actual', ''))
            context = {
                'rpm_form': rpm_form,
                'instrument_form': instrument_form,
            }
            context.update(rpm_fields)
            return form_not_valid(request, context)
    
    elif instrument_type == 'Temperature':
        temperature_form = TemperatureForm(request.POST)
        if temperature_form.is_valid():
            return add_instrument_type(temperature_form,parent_instrument,request)
        else:
            context = {
                'temperature_form': temperature_form,
                'instrument_form': instrument_form,
            }
            return form_not_valid(request, context)
        

def form_not_valid(request, context):
    messages.error(request, 'There was an error with your submission. Please correct the errors below.')
    context.update(load_instrument_types())
    context["institutions"] = Institution.objects.all()
    return render(request, 'add-instrument.html', context)
