from django import forms
from .models import LogbookInfo

class LogbookInfoForm(forms.ModelForm):
    class Meta:
        model = LogbookInfo
        fields = ['entry_time', 'event_time', 'technician_editor', 'participants', 'telescope', 'component', 'new_component', 'detailed_info', 'attachment']
        widgets = {
            'entry_time': forms.DateTimeInput(attrs={'class': 'form-control','type': 'datetime-local', 'placeholder': 'YYYY-MM-DD HH:MM'}),
            'event_time': forms.DateTimeInput(attrs={'class': 'form-control','type': 'datetime-local', 'placeholder': 'YYYY-MM-DD HH:MM'}),
            'technician_editor': forms.TextInput(attrs={'class': 'form-control'}),
            'participants': forms.Textarea(attrs={'class': 'form-control'}),
            'telescope': forms.TextInput(attrs={'class': 'form-control'}),
            'component': forms.Select(attrs={'class': 'form-control'}),
            'new_component': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter new component (if needed)'}),
            'detailed_info': forms.Textarea(attrs={'class': 'form-control'}),
            'attachment': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
