from django.contrib import admin
from .models import ConfigurationInfo
# Register your models here.

@admin.register(ConfigurationInfo)
class ConfigurationInfoAdmin(admin.ModelAdmin):
     # Customize the admin interface
    list_display = [field.name for field in ConfigurationInfo._meta.fields]  # Dynamically include all fields
    search_fields = ('site_name','email')  # Fields you can search by