from django.contrib import admin

from .models import Airplane, User, Ticket, Flight, Crew

admin.site.register(Airplane)
admin.site.register(User)
admin.site.register(Ticket)
admin.site.register(Flight)
admin.site.register(Crew)

