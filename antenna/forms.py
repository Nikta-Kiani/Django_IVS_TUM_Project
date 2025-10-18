from django import forms
from django.core.exceptions import ValidationError
from .models import AntennaInfo

class RequestForm(forms.ModelForm):
    class Meta:
        model = AntennaInfo
        fields = ['full_name', 'agency', 'email', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'full_name': forms.TextInput(attrs={'required': True, 'maxlength': 150}),
            'agency': forms.TextInput(attrs={'required': True, 'maxlength': 150}),
            'email': forms.EmailInput(attrs={'required': True, 'maxlength': 254}),
        }
    
    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if not full_name or len(full_name.strip()) < 2:
            raise ValidationError('Full name must be at least 2 characters long.')
        return full_name.strip()
    
    def clean_agency(self):
        agency = self.cleaned_data.get('agency')
        if not agency or len(agency.strip()) < 2:
            raise ValidationError('Agency name must be at least 2 characters long.')
        return agency.strip()

class SiteDescriptionForm(forms.ModelForm):
    class Meta:
        model = AntennaInfo
        fields = ['site_name', 'city_or_town', 'state_or_province', 'country', 'point_description', 'support_description', 'picture']
        widgets = {
            'site_name': forms.TextInput(attrs={'required': True, 'maxlength': 100}),
            'city_or_town': forms.TextInput(attrs={'required': True, 'maxlength': 50}),
            'state_or_province': forms.TextInput(attrs={'required': True, 'maxlength': 50}),
            'country': forms.TextInput(attrs={'required': True, 'maxlength': 50}),
            'point_description': forms.Textarea(attrs={'rows': 3, 'maxlength': 500}),
            'support_description': forms.Textarea(attrs={'rows': 3, 'maxlength': 500}),
        }
    
    def clean_site_name(self):
        site_name = self.cleaned_data.get('site_name')
        if not site_name or len(site_name.strip()) < 2:
            raise ValidationError('Site name must be at least 2 characters long.')
        return site_name.strip()

class DomesInfoForm(forms.ModelForm):
    class Meta:
        model = AntennaInfo
        fields = ['domes_number', 'local_number', 'four_char_code']
        widgets = {
            'domes_number': forms.TextInput(attrs={'required': True, 'maxlength': 20}),
            'local_number': forms.TextInput(attrs={'required': True, 'maxlength': 50}),
            'four_char_code': forms.TextInput(attrs={'required': True, 'maxlength': 4, 'pattern': '[A-Za-z0-9]{4}'}),
        }
    
    def clean_four_char_code(self):
        four_char_code = self.cleaned_data.get('four_char_code')
        if four_char_code and len(four_char_code) != 4:
            raise ValidationError('Four character code must be exactly 4 characters long.')
        return four_char_code.upper() if four_char_code else four_char_code

class ApproximatePositionForm(forms.ModelForm):
    class Meta:
        model = AntennaInfo
        fields = ['x_coordinate_m', 'y_coordinate_m', 'z_coordinate_m', 'latitude_deg_min', 'longitude_deg_min', 'elevation_m', 'tectonic_plate']
        widgets = {
            'latitude_deg_min': forms.TextInput(attrs={'required': True, 'maxlength': 50, 'placeholder': 'e.g., 49° 12\' 34" N'}),
            'longitude_deg_min': forms.TextInput(attrs={'required': True, 'maxlength': 50, 'placeholder': 'e.g., 12° 34\' 56" E'}),
            'elevation_m': forms.NumberInput(attrs={'required': True, 'step': '0.01'}),
        }
    
    def clean_elevation_m(self):
        elevation = self.cleaned_data.get('elevation_m')
        if elevation is not None and elevation < -1000:
            raise ValidationError('Elevation cannot be less than -1000 meters.')
        if elevation is not None and elevation > 10000:
            raise ValidationError('Elevation cannot be greater than 10000 meters.')
        return elevation
        
class InstrumentForm(forms.ModelForm):
    class Meta:
        model = AntennaInfo
        fields = ['instrument', 'date_of_installation']
        widgets = {
            'date_of_installation': forms.DateInput(attrs={'type': 'date', 'required': True}),
            'instrument': forms.TextInput(attrs={'required': True, 'maxlength': 200}),
        }
        
class OperationContactForm(forms.ModelForm):
    class Meta:
        model = AntennaInfo
        fields = ['operation_contact_name', 'operation_agency', 'operation_email_one', 'operation_email_two']
        widgets = {
            'operation_contact_name': forms.TextInput(attrs={'required': True, 'maxlength': 100}),
            'operation_agency': forms.TextInput(attrs={'required': True, 'maxlength': 250}),
            'operation_email_one': forms.EmailInput(attrs={'required': True, 'maxlength': 254}),
            'operation_email_two': forms.EmailInput(attrs={'maxlength': 254}),
        }

class SiteContactForm(forms.ModelForm):
    class Meta:
        model = AntennaInfo
        fields = ['site_contact_name', 'site_agency', 'site_email', 'additional_info']
        widgets = {
            'site_contact_name': forms.TextInput(attrs={'required': True, 'maxlength': 100}),
            'site_agency': forms.TextInput(attrs={'required': True, 'maxlength': 250}),
            'site_email': forms.EmailInput(attrs={'required': True, 'maxlength': 254}),
            'additional_info': forms.Textarea(attrs={'rows': 4}),
        }