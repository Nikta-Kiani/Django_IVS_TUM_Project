from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import LogbookInfo

class LogbookInfoForm(forms.ModelForm):
    class Meta:
        model = LogbookInfo
        fields = ['entry_time', 'event_time', 'technician_editor', 'participants', 'telescope', 'component', 'new_component', 'detailed_info', 'attachment']
        widgets = {
            'entry_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'required': True}),
            'event_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'required': True}),
            'technician_editor': forms.TextInput(attrs={'required': True, 'maxlength': 200}),
            'participants': forms.Textarea(attrs={'rows': 3, 'maxlength': 500}),
            'telescope': forms.TextInput(attrs={'required': True, 'maxlength': 100}),
            'component': forms.Select(attrs={'required': True}),
            'new_component': forms.TextInput(attrs={'maxlength': 100, 'placeholder': 'Enter new component (if needed)'}),
            'detailed_info': forms.Textarea(attrs={'rows': 4, 'required': True}),
            'attachment': forms.ClearableFileInput(),
        }
    
    def clean_event_time(self):
        event_time = self.cleaned_data.get('event_time')
        if event_time and event_time > timezone.now():
            raise ValidationError('Event time cannot be in the future.')
        return event_time
    
    def clean_technician_editor(self):
        technician = self.cleaned_data.get('technician_editor')
        if not technician or len(technician.strip()) < 2:
            raise ValidationError('Technician/Editor name must be at least 2 characters long.')
        return technician.strip()
    
    def clean_detailed_info(self):
        info = self.cleaned_data.get('detailed_info')
        if not info or len(info.strip()) < 10:
            raise ValidationError('Detailed information must be at least 10 characters long.')
        return info.strip()
