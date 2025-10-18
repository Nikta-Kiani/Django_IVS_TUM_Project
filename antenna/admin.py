from django.contrib import admin
from .models import AntennaInfo
#from auditlog.models import LogEntry

# Register your models here.
@admin.register(AntennaInfo)
class AntennaInfoAdmin(admin.ModelAdmin):
     # Customize the admin interface
    list_display = [field.name for field in AntennaInfo._meta.fields]  # Dynamically include all fields
    search_fields = ('site_name', 'country')  # Fields you can search by

# admin.site.register(LogEntry)