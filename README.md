# Vitec Admin


## Add Instrument Type
models.py
    Create new model and make it of Instrument type
types.json
    Add to instrument_types. Create new array for new instrument types
forms.py
    Add new form class for new type
views.py - add_instrument(request)
    Add form for new instrument type to context
helper.py - find_instrument_type(instrument_form, request)
    Add if statement for new instrument type
helper.py - edit_instrument_post(request, instrument)
    Add if statement for new instrument type
helper.py - edit_instrument_get(instrument)
    Add if statement for new instrument type
views.py - service_order(request, so_number)
    Add if statement for casting instruments
forms.py
    Add new ValuesForm class for instrument type
views.py - update_instrument_values(request, instrument_id)
    Add if statement for new instrument type
views.py - add_instrument_service_order(request, so_number)
    Add form for new instrument type to context
instrument-type-fields.html
    Create div and respective fields for new instrument type
customAddInstrument.js - toggleFields()
    Add variable for new instrument type fields and add it to if statement
service-order.html
    Add fields to modal
customAddServiceOrder.html
    Add code for fields 
so_pdf_generation.py
    Add code for creating table of new type

## Add Instrument Type Fields
models.py
    Add new fields to correct model
forms.py 
    Add necessary fields to the respective form class
instrument-type-fields.html
    Add fields to respective instrument type fields

FOR ARRAY FIELDS:
customAddInstrument.js
    Add code for multiple fields and field consolidation
helper.py - find_instrument_type(instrument_form, request)
    Call parser to if statement 
helper.py - edit_instrument_post(request, instrument)
    Add array to context
helper.py - edit_instrument_get(instrument)
    Add array to context

FOR VALUE FIELDS:
forms.py
    Add fields to respestive ValuesForm class
service-order.html
    Add code to the modal
customAddServiceOrder.js - IF ARRAY FIELD
    Add code for consolidation and toggle btn