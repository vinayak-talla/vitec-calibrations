from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from django.contrib import messages
from .forms import InstitutionForm, InstrumentForm, PipetteForm, RPMForm, TemperatureForm, RPMValueForm
from .models import Institution, Instrument, Pipette, RPM, Temperature, Service_Order
from django.core.paginator import Paginator
from .helper import get_paginated_page_range, parse_phone_number, add_instrument_type, find_instrument_type, form_not_valid, parse_rpm_fields
from .utils import add_dropdown_option, load_instrument_types
from django.db.models import Max



def home(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Restricted Access. You must login before accessing Vitec Admin.')
        return redirect('login')
    
    if request.method == "POST":
        # Clear any existing session service order
        if 'session_so_number' in request.session:
            del request.session['session_so_number']

        last_so_number = Service_Order.objects.aggregate(Max('so_number'))['so_number__max']
        so_number = last_so_number + 1 if last_so_number else 1

        # Redirect to the Add Service Order page with the `so_number`
        return redirect('add-service-order', so_number=so_number)
    
    return render(request, 'home.html', {'timestamp': now().timestamp()})


def add_institution(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Restricted Access. You must login before accessing Vitec Admin.')
        return redirect('login')
    
    if request.method == "POST":
        form = InstitutionForm(request.POST)
        if form.is_valid():
            
            institution = form.save()
            messages.success(request, f"Institution '{institution.name}' has been successfully added.")
            if 'save_and_add_another' in request.POST:
                return redirect('add-institution')
            else:
                return redirect('view-institutions') 
        else:
            context = parse_phone_number(request.POST.get('phone_number', ''),form)

            messages.error(request, 'There was an error with your submission. Please correct the errors below.')
            return render(request, 'add-institution.html', context)
            
    else:
        form = InstitutionForm()
    return render(request, 'add-institution.html', {'timestamp': now().timestamp(), 'form': form })



def view_institutions(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Restricted Access. You must login before accessing Vitec Admin.')
        return redirect('login')
    
    # Get the search query from the GET request
    search_query = request.GET.get('search', '')

    # Filter institutions by name if search query exists
    if search_query:
        institutions = Institution.objects.filter(name__icontains=search_query)
    else:
        institutions = Institution.objects.all()
    
    institutions = institutions.order_by('name')
    paginator = Paginator(institutions, 10)  # Show 10 institutions per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # Calculate the range of pages for pagination 
    page_range = get_paginated_page_range(page_obj)

    return render(request, 'view-institutions.html', {'timestamp': now().timestamp(), 
                                                      'page_obj': page_obj, 
                                                      'page_range': page_range, 
                                                      'search_query': search_query,
                                                      'is_full': len(page_obj)})


def edit_institution(request, institution_name):
    if not request.user.is_authenticated:
        messages.warning(request, 'Restricted Access. You must login before accessing Vitec Admin.')
        return redirect('login')
    
    institution = get_object_or_404(Institution, name=institution_name)

    if request.method == "POST":
        form = InstitutionForm(request.POST, instance=institution)
        if form.is_valid():
            
            institution = form.save()
            messages.success(request, f"Institution '{institution.name}' has been successfully updated.")
            if 'save_and_add_another' in request.POST:
                return redirect('add-institution')
            else:
                return redirect('view-institutions') 
        else:
            context = parse_phone_number(request.POST.get('phone_number', ''),form)

            messages.error(request, 'There was an error with your update. Please correct the errors below.')
            return render(request, 'edit-institution.html', context) 
        
    else:
        form = InstitutionForm(instance=institution)

        phone_number = institution.phone_number
        phone_part1 = phone_number[:3] 
        phone_part2 = phone_number[3:6]
        phone_part3 = phone_number[6:]

    return render(request, 'edit-institution.html', {
        'timestamp': now().timestamp(),
        'form': form,
        'phone_part1': phone_part1,
        'phone_part2': phone_part2,
        'phone_part3': phone_part3,
    })
    
def delete_institution(request, institution_name):
    if not request.user.is_authenticated:
        messages.warning(request, 'Restricted Access. You must login before accessing Vitec Admin.')
        return redirect('login')
    
    institution = get_object_or_404(Institution, name=institution_name)
    
    if request.method == "POST":
        institution.delete()
        messages.success(request, f"Institution '{institution_name}' has been deleted successfully.")
        return redirect('view-institutions')  # Adjust to your view's URL name

    messages.error(request, "Invalid request method.")
    return redirect('edit_institution', institution_name=institution_name) 


def add_instrument(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Restricted Access. You must login before accessing Vitec Admin.')
        return redirect('login')
    
    if request.method == "POST":
        instrument_form = InstrumentForm(request.POST)
        if instrument_form.is_valid():
            # Extract the type from the form
            instrument_type = instrument_form.cleaned_data['instrument_type']


            # Handle child models based on type
            return find_instrument_type(instrument_type,instrument_form,request)

        else:
            messages.error(request, 'There was an error with your submission. Please correct the errors below.')
            context = {'timestamp': now().timestamp(),
                    'instrument_form': instrument_form,
                    'institutions': Institution.objects.all()
                    }
            context.update(load_instrument_types())
            return render(request, 'add-instrument.html', context)

    context = {'timestamp': now().timestamp(),
        'instrument_form': InstrumentForm(),
        'pipette_form': PipetteForm(),
        'centrifuge_form': RPMForm(),
        'thermometer_form': TemperatureForm(),
        'institutions': Institution.objects.all()
        }
    context.update(load_instrument_types())

    return render(request, 'add-instrument.html', context)


def add_dropdown_option_view(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Restricted Access. You must login before accessing Vitec Admin.')
        return redirect('login')
    """Handle AJAX request to add a new option to a dropdown."""
    if request.method == "POST":
        dropdown_key = request.POST.get("dropdown_key", "").strip()
        new_option = request.POST.get("new_option", "").strip()

        if dropdown_key and new_option:
            added = add_dropdown_option(dropdown_key, new_option)
            if added:
                return JsonResponse({"success": True, "message": f"'{new_option}' added successfully to {dropdown_key}."})
            else:
                return JsonResponse({"success": False, "message": f"'{new_option}' already exists in {dropdown_key}."})

    return JsonResponse({"success": False, "message": "Invalid request."})


def view_instruments(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Restricted Access. You must login before accessing Vitec Admin.')
        return redirect('login')
    
    # Get the search query from the GET request
    search_query = request.GET.get('search', '')

    # Filter institutions by name if search query exists
    if search_query:
        instruments = Instrument.objects.filter(id__icontains=search_query)
    else:
        instruments = Instrument.objects.all()
    
    instruments = instruments.order_by('institution')
    paginator = Paginator(instruments, 10)  # Show 10 institutions per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # Calculate the range of pages for pagination 
    page_range = get_paginated_page_range(page_obj)

    return render(request, 'view-instruments.html', {'timestamp': now().timestamp(), 
                                                      'page_obj': page_obj, 
                                                      'page_range': page_range, 
                                                      'search_query': search_query,
                                                      'is_full': len(page_obj)})


def edit_instrument(request, instrument_id):
    if not request.user.is_authenticated:
        messages.warning(request, 'Restricted Access. You must login before accessing Vitec Admin.')
        return redirect('login')
    
    instrument = get_object_or_404(Instrument, id=instrument_id)

    context = {
        'timestamp': now().timestamp(),
        'institutions': Institution.objects.all()
    }
    context.update(load_instrument_types())

    if request.method == "POST":

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
            if 'save_and_add_another' in request.POST:
                return redirect('add-instrument')
            else:
                return redirect('view-instruments') 
        else:
            context['instrument_form'] = instrument_form
            messages.error(request, 'There was an error with your update. Please correct the errors below.')
            return render(request, 'edit-instrument.html', context) 

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
    return render(request, 'edit-instrument.html', context)
    


def delete_instrument(request, instrument_id):
    if not request.user.is_authenticated:
        messages.warning(request, 'Restricted Access. You must login before accessing Vitec Admin.')
        return redirect('login')
    
    instrument = get_object_or_404(Instrument, id=instrument_id)
    
    if request.method == "POST":
        instrument.delete()
        messages.success(request, f"Instrument '{instrument_id}' has been deleted successfully.")
        return redirect('view-instruments')  # Adjust to your view's URL name

    messages.error(request, "Invalid request method.")
    return redirect('edit_instrument', instrument_id=instrument_id) 


def add_service_order(request, so_number):
    if not request.user.is_authenticated:
        messages.warning(request, 'Restricted Access. You must login before accessing Vitec Admin.')
        return redirect('login')
    
    # Retrieve the service order session or initialize it
    session_so_number = request.session.get('session_so_number', None)
        
    if request.method == "POST":
        instrument_id = request.POST.get('instrument_id', '').strip()
        if instrument_id:
            # Check if the instrument exists in the database
            try:
                instrument = Instrument.objects.get(id=instrument_id)
            except Instrument.DoesNotExist:
                messages.error(request, f"Instrument with id: {instrument_id} does not exist.")
                return redirect('add-service-order', so_number=so_number)

            if not session_so_number:
                service_order = Service_Order.objects.create(
                        institution=instrument.institution,
                        instrument_list=[instrument.id]
                    )
                request.session['session_so_number'] = service_order.so_number
                session_so_number = request.session.get('session_so_number', None)
                messages.success(request, f"Instrument {instrument_id} added successfully")
            else:
                # Add the instrument to the session list if not already there
                service_order = Service_Order.objects.get(so_number=session_so_number)
                if instrument.id not in service_order.instrument_list:
                    if instrument.institution == service_order.institution:
                        service_order.instrument_list.append(instrument.id)
                        service_order.save()
                        messages.success(request, f"Instrument {instrument_id} added successfully")
                    else:
                        messages.warning(request, f"Instrument {instrument_id} belongs to a different institution")
                else:
                    messages.warning(request, f"Instrument {instrument_id} is already in the service order")
        else:
            messages.error(request, "Invalid instrument ID.")

    if session_so_number:
        instrument_list = Service_Order.objects.get(so_number=session_so_number).instrument_list
    else:
        instrument_list = []

    # Get the search query from the GET request
    search_query = request.GET.get('search', '')

    # Filter institutions by name if search query exists
    if search_query:
        so_instruments = Instrument.objects.filter(id__in=instrument_list, id__icontains=search_query)
    else:
        # Fetch the list of Instrument objects for rendering
        so_instruments = Instrument.objects.filter(id__in=instrument_list)
    
    # Cast each instrument to the appropriate child model
    cast_so_instruments = []
    for instrument in so_instruments:
        if instrument.instrument_type == "RPM":
            cast_so_instruments.append(RPM.objects.get(id=instrument.id))
        elif instrument.instrument_type == "Temperature":
            cast_so_instruments.append(Temperature.objects.get(id=instrument.id))
        elif instrument.instrument_type == "Pipette":
            cast_so_instruments.append(Pipette.objects.get(id=instrument.id))
    
    paginator = Paginator(cast_so_instruments, 2)  # Show 10 institutions per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # Calculate the range of pages for pagination 
    page_range = get_paginated_page_range(page_obj)


    context = {
        'timestamp': now().timestamp(), 
        'page_obj': page_obj, 
        'page_range': page_range, 
        'search_query': search_query,
        'is_full': len(page_obj),
    }

    return render(request, 'add-service-order.html', context)

def update_instrument_values(request, instrument_id):
    if not request.user.is_authenticated:
        messages.warning(request, 'Restricted Access. You must login before accessing Vitec Admin.')
        return redirect('login')
    
    if request.method == "POST":
        instrument = get_object_or_404(Instrument, id=instrument_id)
        instrument_type = instrument.instrument_type

        if instrument_type == "RPM":
            rpm_instrument = instrument.rpm  # Cast to RPM child model
            form = RPMValueForm(request.POST, instance=rpm_instrument)
            print(request.POST)
            if form.is_valid():
                form.save()  # Saves the cleaned data to the model
                messages.success(request, f"Values updated successfully for Instrument ID {instrument_id}.")
                # return None
                return JsonResponse({'success': True, 'message': 'Instrument values updated successfully.'})
            else:
                return JsonResponse({'success': False, 'errors': form.errors})

        elif instrument_type == "Temperature":
            temp_instrument = Temperature.objects.get(id=instrument.id)  # Cast to Temperature child model
            temp_instrument.temperature_test = request.POST.get('temperature_test', temp_instrument.temperature_test)
            temp_instrument.temperature_actual = request.POST.get('temperature_actual', temp_instrument.temperature_actual)
            temp_instrument.save()


        return redirect('add-service-order', so_number=request.session.get('session_so_number'))

    messages.error(request, "Invalid request.")
    return redirect('add-service-order', so_number=request.session.get('session_so_number'))



# def view_service_orders(request):
#     if not request.user.is_authenticated:
#         messages.warning(request, 'Restricted Access. You must login before accessing Vitec Admin.')
#         return redirect('login')
    
#     return render(request, 'view-service-orders.html', {'timestamp': now().timestamp() })


# def edit_service_order(request, so_number):
#     if not request.user.is_authenticated:
#         messages.warning(request, 'Restricted Access. You must login before accessing Vitec Admin.')
#         return redirect('login')
    
#     return render(request, 'edit-service-order.html', {'timestamp': now().timestamp() })


# def delete_service_order(request, so_number):
#     if not request.user.is_authenticated:
#         messages.warning(request, 'Restricted Access. You must login before accessing Vitec Admin.')
#         return redirect('login')
    
#     return render(request, 'delete-service-order.html', {'timestamp': now().timestamp() })