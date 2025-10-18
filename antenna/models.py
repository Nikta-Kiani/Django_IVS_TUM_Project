from django.db import models
from django.contrib.auth.models import User
from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
# Create your models here.

class AntennaInfo(models.Model):
    history = AuditlogHistoryField()
    # Adding a foreign key to link each DomesInformation entry to a user
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, related_name='antenna', help_text="The user who created this entry.")
    # Tab 1: Request Form
    full_name = models.CharField(max_length=150, help_text="Full name of the person making the request.")
    agency = models.CharField(max_length=150, help_text="Agency name of the requester.")
    email = models.EmailField(max_length=254, help_text="Email address of the requester.")
    date = models.DateField(null=False, help_text="Date of the request.")

    # Tab 2: Site Description
    site_name = models.CharField(max_length=100, null=False, help_text="Name of the site.")
    city_or_town = models.CharField(default= "Koetzting", max_length=50, blank=False, null=False, help_text="City or Town where the site is located.")
    state_or_province = models.CharField(default= "Bayern", max_length=50, blank=False, null=False, help_text="State or Province where the site is located.")
    country = models.CharField(default= "Germany", max_length=50, null=False, help_text="Country where the site is located.")
    point_description = models.CharField(max_length=500, help_text="Description of the point.")
    support_description = models.CharField(max_length=500, blank=True, null=True, help_text="Description of the support (optional).")
    # Optional fields for images or other media
    picture = models.ImageField(upload_to='images/', blank=True, null=True,  help_text="Upload an optional image (optional).")
    
    # Tab 3: Domes Info
    domes_number = models.CharField(max_length=20, help_text="Domes identification number.")
    local_number = models.CharField(max_length=50, help_text="Local identification number.")
    four_char_code = models.CharField(max_length=4, help_text="4-character site code.")

    # Tab 4: Approximate Position
    x_coordinate_m = models.FloatField(default="0", null=False, help_text="X coordinate in meters.")
    y_coordinate_m = models.FloatField(default="0", null=False, help_text="Y coordinate in meters.")
    z_coordinate_m = models.FloatField(default="0", null=False, help_text="Z coordinate in meters.")
    latitude_deg_min = models.CharField(max_length=50, null=False, help_text="Latitude in degrees and minutes.")
    longitude_deg_min = models.CharField(max_length=50, null=False, help_text="Longitude in degrees and minutes.")
    elevation_m = models.FloatField(null=False,  help_text="Elevation in meters.")
    tectonic_plate = models.CharField(max_length=100 , null=True, blank=True, help_text="Name of the tectonic plate (optional).")
    source_of_position = models.CharField(max_length=100, null=True, blank=True, help_text="Name of the position's source (optional).")
    
    # Tab 5: Instrument
    instrument = models.CharField(max_length=200, help_text="Name of the installed instrument.")
    date_of_installation = models.DateField(null=False, help_text="Date of the instrument installation.")

    # Tab 6: Operation Contact
    operation_contact_name = models.CharField(max_length=100, help_text="Full name of the operation contact.")
    operation_agency = models.CharField(max_length=250, help_text="Agency name of the operation contact.")
    operation_email_one = models.EmailField(default='example@example.com', null=False, blank=False, help_text="Email of the first operation contact.")
    operation_email_two = models.EmailField(null=True, blank=True, help_text="Email of the second operation contact (optional).")

    # Tab 7: Site Contact
    site_contact_name = models.CharField(max_length=100, help_text="Full name of the site contact.")
    site_agency = models.CharField(max_length=250, help_text="Agency name of the site contact.")
    site_email = models.EmailField(help_text="Email of the site contact.")
    additional_info = models.TextField(blank=True, null=True, help_text="Additional information or comments (optional).")

    def __str__(self):
        return f'{self.site_name} - {self.user.username}'
     #return f"DOMES Info for {self.site_name} by {self.user.username}"
     
    class Meta:
        verbose_name_plural = "Antenna Information"
       
        
 # Register the model with auditlog
auditlog.register(AntennaInfo)