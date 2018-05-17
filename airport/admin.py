from django.contrib import admin

from .models import Airplane, User, Ticket, Flight

admin.site.register(Airplane)
admin.site.register(User)
admin.site.register(Ticket)
admin.site.register(Flight)
