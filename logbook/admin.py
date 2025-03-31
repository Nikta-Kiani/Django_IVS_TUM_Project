from django.contrib import admin
from .models import LogbookInfo
# Register your models here.

@admin.register(LogbookInfo)
class LogbookInfoAdmin(admin.ModelAdmin):
     # Customize the admin interface
    list_display = [field.name for field in LogbookInfo._meta.fields]  # Dynamically include all fields
    search_fields = ('technician_editor','event_time')  # Fields you can search by