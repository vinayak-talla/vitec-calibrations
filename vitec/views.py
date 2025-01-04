from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from django.contrib import messages
from .forms import InstitutionForm, InstrumentForm, PipetteForm, RPMForm, TemperatureForm, RPMValueForm, TemperatureValueForm
from .models import Institution, Instrument, Pipette, RPM, Temperature, Service_Order
from django.db.models import Case, When
from django.core.paginator import Paginator
from .helper import get_paginated_page_range, parse_phone_number, add_instrument_type, find_instrument_type, form_not_valid, parse_rpm_fields, edit_instrument_post, edit_instrument_get, add_instrument_valid
from .utils import add_dropdown_option, load_instrument_types
from django.db.models import Max
from django.utils.cache import add_never_cache_headers



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
        return redirect('service-order', so_number=so_number)
    
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
            valid_post,data = find_instrument_type(instrument_form,request)

            if valid_post:
                return add_instrument_valid(request,instrument_form.cleaned_data['id'])
            else:
                return form_not_valid(request,data)
        
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
        valid_post,data = edit_instrument_post(request,instrument)
        if valid_post:
            if 'save_and_add_another' in request.POST:
                return redirect('add-instrument')
            else:
                return redirect('view-instruments') 
        else:
            context.update(data)
            return render(request, 'edit-instrument.html', context) 

    context.update(edit_instrument_get(instrument))
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


def service_order(request, so_number):
    if not request.user.is_authenticated:
        messages.warning(request, 'Restricted Access. You must login before accessing Vitec Admin.')
        return redirect('login')

    if Service_Order.objects.filter(so_number=so_number).exists():
        so_exists = True
    else:
        so_exists = False

    context = {}
    
    if request.method == "POST":
        instrument_id = request.POST.get('instrument_id', '').strip()
        if instrument_id:
            # Check if the instrument exists in the database
            try:
                instrument = Instrument.objects.get(id=instrument_id)
            except Instrument.DoesNotExist:
                messages.error(request, f"Instrument with id: {instrument_id} does not exist.")
                return redirect('service-order', so_number=so_number)
                
            if not so_exists:
                service_order = Service_Order.objects.create(
                        institution=instrument.institution,
                        instrument_list=[instrument.id]
                    )
                messages.success(request, f"Instrument {instrument_id} added successfully")
                if service_order.so_number != so_number:
                    return redirect('service-order', so_number=service_order.so_number)
            else:
                # Add the instrument to the session list if not already there
                service_order = Service_Order.objects.get(so_number=so_number)
                if not service_order.instrument_list:
                    service_order.institution = instrument.institution
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

        # Redirect to prevent form resubmission on refresh
        return redirect('service-order', so_number=so_number)

    if so_exists:
        service_order = Service_Order.objects.get(so_number=so_number)
        instrument_list = service_order.instrument_list[::-1]
        context['service_order'] = service_order
        context['lab_contact'] = Institution.objects.get(name=service_order.institution).contact
        
    else:
        instrument_list = []

    # Get the search query from the GET request
    search_query = request.GET.get('search', '')

    # Define a custom ordering
    ordering = Case(*[When(id=pk, then=pos) for pos, pk in enumerate(instrument_list)])


    # Filter institutions by name if search query exists
    if search_query:
        so_instruments = Instrument.objects.filter(id__in=instrument_list, id__icontains=search_query).order_by(ordering)
    else:
        # Fetch the list of Instrument objects for rendering
        so_instruments = Instrument.objects.filter(id__in=instrument_list).order_by(ordering)

    
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
    
    context.update({
        'timestamp': now().timestamp(), 
        'page_obj': page_obj, 
        'page_range': page_range, 
        'search_query': search_query,
        'is_full': len(page_obj),
        'so_number': so_number
    })

    return render(request, 'service-order.html', context)

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
        else:
            temp_instrument = instrument.temperature  # Cast to Temperature child model
            form = TemperatureValueForm(request.POST, instance=temp_instrument)

        if form.is_valid():
            form.save()  # Saves the cleaned data to the model
            messages.success(request, f"Values updated successfully for Instrument ID {instrument_id}.")
            # return None
            return JsonResponse({'success': True, 'message': 'Instrument values updated successfully.'})
        
        return JsonResponse({'success': False, 'errors': form.errors})



def delete_instrument_service_order(request, so_number, instrument_id):
    if not request.user.is_authenticated:
        messages.warning(request, 'Restricted Access. You must login before accessing Vitec Admin.')
        return redirect('login')
    
    servive_order = get_object_or_404(Service_Order, so_number=so_number)
    
    if request.method == "POST":
        if instrument_id in servive_order.instrument_list:
            servive_order.instrument_list.remove(instrument_id)
            servive_order.save()
            messages.success(request, f"Instrument '{instrument_id}' has been removed from the service order.")
            return JsonResponse({'success': True})
        else:
            messages.warning(request, f"Instrument '{instrument_id}' doesn't exist in this service order.")
            return JsonResponse({'success': False})

    messages.error(request, "Invalid request method.")
    return JsonResponse({'success': False})



def edit_instrument_service_order(request, so_number, instrument_id):
    if not request.user.is_authenticated:
        messages.warning(request, 'Restricted Access. You must login before accessing Vitec Admin.')
        return redirect('login')
    
    instrument = get_object_or_404(Instrument, id=instrument_id)

    context = {
        'timestamp': now().timestamp(),
        'so_number': so_number,
        'institutions': Institution.objects.all()
    }
    context.update(load_instrument_types())

    if request.method == "POST":
        valid_post,data = edit_instrument_post(request,instrument)
        if valid_post:
            return redirect('service-order', so_number=so_number)
        else:
            context.update(data)
            return render(request, 'edit-instrument-service-order.html', context) 

    context.update(edit_instrument_get(instrument))
    return render(request, 'edit-instrument-service-order.html', context)




def add_instrument_service_order(request, so_number):
    if not request.user.is_authenticated:
        messages.warning(request, 'Restricted Access. You must login before accessing Vitec Admin.')
        return redirect('login')
    
    if request.method == "POST":
        instrument_form = InstrumentForm(request.POST)
        if instrument_form.is_valid():
            valid_post,data = find_instrument_type(instrument_form,request)

            if valid_post:
                instrument = get_object_or_404(Instrument, id=instrument_form.cleaned_data['id'])
                if Service_Order.objects.filter(so_number=so_number).exists():
                    service_order = Service_Order.objects.get(so_number=so_number)
                    if not service_order.instrument_list:
                        service_order.institution = instrument.institution
                    if instrument.institution == service_order.institution:
                        service_order.instrument_list.append(instrument.id)
                        service_order.save()
                        messages.success(request, f"Instrument ID: '{instrument.id}' has been successfully created and added to the service order.")
                    else:
                        messages.success(request, f"Instrument ID: '{instrument.id}' has been successfully created")
                        messages.warning(request, f"Instrument ID: '{instrument.id}' can't be added to the service order because it belongs to a different institution")
                else:
                    service_order = Service_Order.objects.create(
                        institution=instrument.institution,
                        instrument_list=[instrument.id]
                    )
                    if service_order.so_number != so_number:
                        so_number = service_order.so_number
                
                    messages.success(request, f"Instrument ID: '{instrument.id}' has been successfully created and added to the service order.")
                if 'save_and_add_another' in request.POST:
                    return redirect('add-instrument-service-order', so_number=so_number)
                return redirect('service-order', so_number=so_number)
                    
            else:
                # change form not valid to check if so_number is in context and render correct template accordingly
                print("NHFJFJJFIFIIFII")
                data['so_number'] = so_number
                return form_not_valid(request,data)
        
        else:
            messages.error(request, 'There was an error with your submission. Please correct the errors below.')
            context = {'timestamp': now().timestamp(),
                    'instrument_form': instrument_form,
                    'institutions': Institution.objects.all(),
                    'so_number': so_number
                    }
            context.update(load_instrument_types())
            return render(request, 'add-instrument-service-order.html', context)


    instrument_form = InstrumentForm()
    if Service_Order.objects.filter(so_number=so_number).exists():
        service_order = Service_Order.objects.get(so_number=so_number)
        if service_order.instrument_list:
            instrument_form = InstrumentForm(initial={'institution': service_order.institution})


    context = {'timestamp': now().timestamp(),
        'instrument_form': instrument_form,
        'pipette_form': PipetteForm(),
        'centrifuge_form': RPMForm(),
        'thermometer_form': TemperatureForm(),
        'institutions': Institution.objects.all(),
        'so_number': so_number
        }
    context.update(load_instrument_types())

    return render(request, 'add-instrument-service-order.html', context)


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