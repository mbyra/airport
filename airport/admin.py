from django.contrib import admin

from .models import Airplane, Passenger, Ticket, Flight

admin.site.register(Airplane)
admin.site.register(Passenger)
admin.site.register(Ticket)
admin.site.register(Flight)
