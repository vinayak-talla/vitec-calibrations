from django.contrib import admin
from .models import Institution, Instrument, Pipette, RPM, Temperature, Service_Order

admin.site.register(Instrument)
admin.site.register(Institution)
admin.site.register(Pipette)
admin.site.register(RPM)
admin.site.register(Temperature)
admin.site.register(Service_Order)





