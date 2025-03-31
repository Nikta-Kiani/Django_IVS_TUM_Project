from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

COMPONENTS = [
    ('1.1', 'Radio telescope'),
    ('1.1.1', 'Servosystem / Drives / Power Electronics'),
    ('1.1.2', 'Antenna Control System'),
    ('1.1.3', 'Cabeling'),
    ('1.1.4', 'Mechanics'),
    ('1.1.5', 'Pointing'),
    ('1.2', 'Frontend'),
    ('1.2.1', 'RF Receiver'),
    ('1.2.2', 'Cryo system / Dewar'),
    ('1.2.3', 'Local oscillator'),
    ('1.2.4', 'IF converter / Down-Converter / Up-Down-Converter'),
    ('1.3', 'Backend'),
    ('1.3.1', 'IF distributor'),
    ('1.3.2', 'Baseband converter (DBBC/RDBE/FILA10G/etc.)'),
    ('1.3.3', 'Data transfer network'),
    ('1.3.4', 'Recorder (Mark6/Flexbuff/etc.)'),
    ('1.4', 'Calibration systems'),
    ('1.4.1', 'Cable calibration system'),
    ('1.4.2', 'Phasen calibration system'),
    ('1.4.3', 'Noise calibration system'),
    ('1.4.4', 'Other calibration systems'),
    ('1.5', 'Time and frequency'),
    ('1.5.1', 'Maser'),
    ('1.5.2', 'GNSS time receiver'),
    ('1.5.3', 'Time and frequency distribution system'),
    ('1.5.4', 'Counter / Dotmon (fmout-gps)'),
    ('1.6', 'Control and Monitoring System'),
    ('1.6.1', 'NASA Field System'),
    ('1.6.2', 'Station code'),
    ('1.6.3', 'Monitoring system'),
    ('1.7', 'IT infrastructure'),
    ('1.7.1', 'Network (LAN)'),
    ('1.7.2', 'Internet'),
    ('1.7.3', 'Transfer server hardware'),
    ('1.7.4', 'Local correlator'),
    ('1.7.5', 'Other hardware'),
    ('1.8', 'Sensors'),
    ('1.8.1', 'Meteorology (Pressure, Temperature, Humidity, Wind speed, Wind direction)'),
    ('1.8.2', 'Other (Radiometer, Tower temps.)'),
    ('1.9', 'Building infrastructure'),
    ('1.9.1', 'Air conditioning'),
    ('1.9.2', 'Power / UPS'),
    ('1.10', 'Buildings'),
    ('1.11', 'Known RFI'),
    ('1.11.1', 'Terrestrial RFI (e.g. 5G / Radar / in-house)'),
    ('1.11.2', 'Satellite signals (e.g. Starlink)'),
    ('1.11.3', 'Local sender (e.g. DORIS)'),
] 
  
class LogbookInfo(models.Model):
    # Adding a foreign key to link each DomesInformation entry to a user
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='logbook', help_text="The user who created this entry.")
    
    entry_time = models.DateTimeField(default=timezone.now, blank = False, null=False, help_text="The current entry date and time.")
    event_time = models.DateTimeField(blank = False, null=False, help_text="Please enter the event date and time.")
    technician_editor = models.TextField(blank=True, null= True, help_text="Please enter the main Editor/User technician name.")  # You can also use a ForeignKey to a User model
    participants = models.TextField(blank=True, null= True, help_text="Please enter other possible participants name." )  # To list additional participants
    telescope = models.CharField(max_length=100, help_text="Please enter the Telescope name.")
    component = models.CharField(max_length=100, choices=COMPONENTS, blank=True, null=True, help_text="Please select the component.")  # Predefined dropdown for component
    new_component = models.CharField(max_length=100, blank=True, null=True, help_text="Add a new component if needed.")  # For users to add a new component if needed
    detailed_info = models.CharField(max_length=350, blank=True, null=True, help_text="Please enter the detailed information about the log entry.")
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True, help_text="Please upload any relevant helpful pdfs, files, or images like a diagram plot or a quality plot.")

    def __str__(self):
        return f"LogbookInfo (URLs, Image, PDF, and other file which is helpful (like a diagram plot or a quality plot) for reference)"
    def __str__(self):
        return f"{self.technician} - {self.entry_time}"

    def __str__(self):
        return f'{self.event_time} - {self.user.username}'
    
    def get_component(self):
        """ Return new component if provided, otherwise return selected from the dropdown. """
        return self.new_component or self.get_component_display()