from django import forms
from .models import AntennaInfo

class RequestForm(forms.ModelForm):
    class Meta:
        model = AntennaInfo
        fields = ['full_name', 'agency', 'email', 'date']
        widgets = {'date': forms.DateInput(attrs={'type': 'date'})}

class SiteDescriptionForm(forms.ModelForm):
    class Meta:
        model = AntennaInfo
        fields = ['site_name', 'city_or_town', 'state_or_province', 'country', 'point_description', 'support_description', 'picture']

class DomesInfoForm(forms.ModelForm):
    class Meta:
        model = AntennaInfo
        fields = ['domes_number', 'local_number', 'four_char_code']

class ApproximatePositionForm(forms.ModelForm):
    class Meta:
        model = AntennaInfo
        fields = ['x_coordinate_m', 'y_coordinate_m', 'z_coordinate_m', 'latitude_deg_min', 'longitude_deg_min', 'elevation_m', 'tectonic_plate']
        
class InstrumentForm(forms.ModelForm):
    class Meta:
        model = AntennaInfo
        fields = ['instrument', 'date_of_installation']
        widgets = {'date_of_installation': forms.DateInput(attrs={'type': 'date'})}
        
class OperationContactForm(forms.ModelForm):
    class Meta:
        model = AntennaInfo
        fields = ['operation_contact_name', 'operation_agency', 'operation_email_one', 'operation_email_two']

class SiteContactForm(forms.ModelForm):
    class Meta:
        model = AntennaInfo
        fields = ['site_contact_name', 'site_agency', 'site_email', 'additional_info']