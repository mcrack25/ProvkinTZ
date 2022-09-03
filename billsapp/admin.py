from django.contrib import admin
from .models import Bill, Client, Organization, Service


admin.site.register(Bill)
admin.site.register(Client)
admin.site.register(Organization)
admin.site.register(Service)
