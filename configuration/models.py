from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog


# Create your models here.

def validate_two_characters(value):
    if len(value) != 2:
        raise ValidationError('This field must have exactly 2 characters.')
    
def validate_eight_characters(value):
    if len(value) != 8:
        raise ValidationError('This field must have exactly 8 characters.')

class ConfigurationInfo(models.Model):
    history = AuditlogHistoryField()
    # Adding a foreign key to link each DomesInformation entry to a user
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, related_name='configuration', help_text="The user who created this entry.")
   
    # Contact section
    prepared_by_full_name = models.CharField(max_length=150, help_text="Full name of the person prepaired the configuration.")
    email = models.EmailField(max_length=254, help_text="Email address of the contact person.")
    update_date = models.DateField(null=True, blank=True, default=None, help_text="The updated Date.")
    report_type = models.CharField(max_length=100, help_text="Type of the configuration report.")

    # Site Identification section
    site_name = models.CharField(max_length=100, blank=False, null=False, help_text="Name of the site.")
    site_8_letter_code = models.CharField( max_length=8, blank=False, null=False, validators=[validate_eight_characters], help_text="Exact 8-characters of the site.")
    site_2_letter_code = models.CharField( max_length=2, blank=False, null=False, validators=[validate_two_characters], help_text="Exact 2-characters of the site.")
    IERS_domes_number = models.CharField(max_length=50, blank=False, null=False, help_text="IERS DOMES number.")
    CDP_occupation_code = models.IntegerField(blank=True, null=True, default=0, help_text="CDP occupation code.")
    CDP_monument_number = models.IntegerField(blank=True, null=True, default=0, help_text="CDP monument number.")
    IGS_station_code = models.CharField(max_length=50, blank=False, null=False, help_text="IGS station code.")
    ILRS_station_name = models.CharField(max_length=50, blank=False, null=False, help_text="ILRS station name.")
    survey_into_national_network = models.BooleanField(default=False, verbose_name='Surveyed into national network?', help_text="Did it survey into national network?")
    start_date_of_operation = models.DateField(null=True, blank=True, default=None, help_text="The start date of configuration operation.")
    additional_info = models.TextField(blank=True, null=True, help_text="Additional information or comments (optional).")
    
    # Site local survey network information
    type_of_marker = models.CharField(max_length=250, help_text="Write the type of marker.")
    frequency_of_surveying = models.CharField(max_length=100, help_text="Mention the frequency of surveying.")
    surveying_method = models.CharField(max_length=250, help_text="Mention the surveying methods.")
    survey_instruments_used = models.CharField(max_length=250, help_text="Mention the surveying instruments which are used.")
    accuracy = models.CharField(max_length=100, help_text="Mention the accuracy of the surveying.")
    survey_performed_by = models.CharField(max_length=250, help_text="Mention who the survey was performed by.")
    survay_documentation = models.CharField(max_length=250, help_text="Mention how and by who the survey was documented.")
    responsible_person = models.CharField(max_length=150, help_text="Mention the responsible person.")
    most_recent_survey_date = models.DateField(null=True, blank=True, default=None, help_text="The most recent survey date.")
    results_provided_to_IERS = models.BooleanField(default=False, verbose_name='Results provided to IERS?', help_text="Did results provide to IERS?")
    results_provided_to_CDDIS = models.BooleanField(default=False, verbose_name='Results provided to CDDIS?', help_text="Did results provide to CDDIS?")
    number_of_reference_markers = models.CharField(max_length=100,blank=True, null=True, help_text="Number of reference markers (optional).")
    additional_info = models.TextField(blank=True, null=True, help_text="Additional information or comments (optional).")
    
    # Site Descriptive Information
    site_map = models.FileField(upload_to='site_map/', blank=True, null=True, help_text="Upload the site map.")
    site_map_url= models.URLField(max_length=200, blank=True, null=True, verbose_name="Site map reference URL (optional)")
    site_diagram = models.FileField(upload_to='site_diagram/', blank=True, null=True, help_text="Upload the site diagram.")
    site_diagram_url = models.URLField(max_length=200, blank=True, null=True, verbose_name="Site diagram reference URL (optional)")
    horizon_mask = models.FileField(upload_to='horizon_mask/', blank=True, null=True, help_text="Upload the horizon mask.")
    horizon_mask_url = models.URLField(max_length=200, blank=True, null=True, verbose_name="Horizon mask reference URL (optional)")
    monument_description = models.FileField(upload_to='monument_description/', blank=True, null=True, help_text="Upload the monument description.")
    monument_description_url = models.URLField(max_length=200, blank=True, null=True, verbose_name="Monument description reference URL (optional)")
    site_photographs = models.FileField(upload_to='site_photographs/', blank=True, null=True, help_text="Upload the site photographs.")
    site_photographs_url = models.URLField(max_length=200, blank=True, null=True, verbose_name="Site photographs reference URL (optional)")
    
    # Antenna Details section
    antenna_type = models.CharField(max_length=255, help_text="Mention the type of antenna.")
    diameter_m = models.FloatField(null=True, blank=True, default=0.0, help_text="Diameter of the antenna in meters.")
    axis_type = models.CharField(max_length=150, help_text="Mention the axis type.")
    axis_offset_m = models.FloatField(null=True, help_text="Axis offset in meters.")
    slew_rate_first_axis_deg_min = models.FloatField(null=True, help_text="Slew rate of the first axis in degrees per minute.")
    slew_rate_second_axis_deg_min = models.FloatField(null=True, help_text="Slew rate of the second axis in degrees per minute.")
    min_limit_first_axis_deg = models.FloatField(null=True, help_text="Minimum limit of the first axis in degrees.")
    max_limit_first_axis_deg = models.FloatField(null=True, help_text="Maximum limit of the first axis in degrees.")
    min_limit_second_axis_deg = models.FloatField(null=True, help_text="Minimum limit of the second axis in degrees.")
    max_limit_second_axis_deg = models.FloatField(null=True, help_text="Maximum limit of the second axis in degrees.")
    horizon_mask_data_azimuth_deg_coressponding_elevationmask_deg = models.CharField(max_length=500, help_text="Horizon mask data (like: azimuth(deg)/corresponding elevation mask(deg)) and seperating each pair of entries with (;).")
    start_date_of_occupation = models.DateField(null=True, blank=True, default=None, help_text="The start date of occupation.")
    end_date_of_occupation = models.DateField(null=True, blank=True, default=None, help_text="The end date of occupation.")
    additional_info = models.TextField(blank=True, null=True, help_text="Additional information or comments (optional).")
    
    # Receiver Information
    feed_location = models.CharField(max_length=150, help_text="Mention the feed location.")
    feed_type = models.CharField(max_length=150, help_text="Mention the feed type.")
    x_first_stage_amplifier = models.CharField(max_length=150, help_text="Mention the X first stage amplifier.")
    s_first_stage_amplifier = models.CharField(max_length=150, help_text="Mention the S first stage amplifier.")
    x_bandwidth_mhz = models.FloatField(null=True, blank=True, default=0.0, help_text="X bandwidth in MHz.")
    s_bandwidth_mhz = models.FloatField(null=True, blank=True, default=0.0, help_text="S bandwidth in MHz.")
    x_tsys_at_zenith_k = models.FloatField(null=True, blank=True, default=0.0, help_text="X Tsys at zenith in K.")
    s_tsys_at_zenith_k = models.FloatField(null=True, blank=True, default=0.0, help_text="S Tsys at zenith in K.")
    x_sefd_jy = models.FloatField(null=True, blank=True, default=0.0, help_text="X SEFD in Jy.")
    s_sefd_jy = models.FloatField(null=True, blank=True, default=0.0, help_text="S SEFD in Jy.")
    x_aperture_efficiency = models.CharField(max_length=150, help_text="Mention the X aperture efficiency in pecentage.")
    s_aperture_efficiency = models.CharField(max_length=150, help_text="Mention the S aperture efficiency in pecentage.")
    x_lo_frequencies_mhz = models.FloatField(null=True, blank=True, default=0.0, help_text="X LO frequencies in MHz.")
    s_lo_frequencies_mhz = models.FloatField(null=True, blank=True, default=0.0, help_text="S LO frequencies in MHz.")
    phase_calibrator_type = models.CharField(max_length=250, help_text="Mention the phase calibrator type including the MHz input and temp controller.")
    additional_info = models.TextField(blank=True, null=True, help_text="Additional information or comments (optional).")
    
    # Cables between Receiver and Backend
    length_of_cable_run_m = models.FloatField(null=True, blank=True, default=0.0, help_text="Length of cable run in meters.")
    x_band_cable_type = models.CharField(max_length=150, help_text="Mention the X band cable type.")
    x_band_freq_bandpass_mhz = models.CharField(max_length=150, help_text="X band frequency bandpass in MHz.")
    s_band_cable_type = models.CharField(max_length=150, help_text="Mention the S band cable type.") 
    s_band_freq_bandpass_mhz = models.CharField(max_length=150, help_text="S band frequency bandpass in MHz.")
    lo_ref_signal_cable_type = models.CharField(max_length=150, help_text="Mention the LO ref signal cable type.")
    lo_ref_signal_freq_mhz = models.CharField(max_length=150, help_text="LO ref signal frequency in MHz.")
    phase_cal_ref_signal_cable_type = models.CharField(max_length=150, help_text="Mention the phase cal ref signal cable type.")
    phase_cal_ref_signal_freq_mhz = models.FloatField(null=True, blank=True, default=0.0, help_text="Phase cal ref signal frequency in MHz.")
    cable_measure_system_type = models.CharField(max_length=250, help_text="Mention the cable measurement system type.")
    additional_info = models.TextField(blank=True, null=True, help_text="Additional information or comments (optional).")
    
    # Data Acquisition System information
    type_of_video_converter = models.CharField(max_length=150, help_text="Mention the type of video converter set.")
    number_of_mixers = models.IntegerField(null=True, blank=True, default=0, help_text="Number of mixers in video converter set.")
    sidebands_available = models.CharField(max_length=150, help_text="Mention the set's available sidebands.")
    number_of_mixers_with_2mhz_filter = models.IntegerField(null=True, blank=True, default=0, help_text="Number of mixers with 2 MHz filter in all sideband outputs.")
    number_of_mixers_with_4mhz_filter = models.IntegerField(null=True, blank=True, default=0, help_text="Number of mixers with 4 MHz filter in all sideband outputs.")
    number_of_mixers_with_8mhz_filter = models.IntegerField(null=True, blank=True, default=0, help_text="Number of mixers with 8 MHz filter in all sideband outputs.")
    number_of_mixers_with_16mhz_filter = models.IntegerField(null=True, blank=True, default=0, help_text="Number of mixers with 16 MHz filter in all sideband outputs.")
    number_of_mixers_with_32mhz_filter = models.IntegerField(null=True, blank=True, default=0, help_text="Number of mixers with 32 MHz filter in all sideband outputs.")
    additional_video_converter = models.CharField(max_length=400, blank=True, null=True, help_text="Additional information of the video converter.")
    formatter_type = models.CharField(max_length=150, help_text="Mention the formatter type.")
    serial_number_or_rack_id = models.CharField(max_length=150, help_text="Mention the serial number or rack ID of the formatter.")
    additional_formattter = models.CharField(max_length=400, blank=True, null=True, help_text="Additional information of the formatter.")
    decode_type = models.CharField(max_length=150, help_text="Mention the decode type of the decoder.")
    additional_decoder = models.CharField(max_length=400, blank=True, null=True, help_text="Additional information of the decoder.")
    IF_distributor_type = models.CharField(max_length=150, help_text="Mention the IF distributor type.")
    additional_IF_distributor = models.CharField(max_length=400, blank=True, null=True, help_text="Additional information of the IF distributor.")
    X_down_converter_freq = models.FloatField(null=True, blank=True, default=0.0, help_text="X down converter frequency in MHz.")
    S_up_down_converter_freq = models.CharField(max_length=250, null=True, help_text="S up/down converter frequency in MHz.") 
    additional_converter = models.CharField(max_length=400, blank=True, null=True, help_text="Additional information of the converter.")
    other_rack_equipment = models.CharField(max_length=150, help_text="Mention the other rack equipments or the planned ones.")
    additional_rack_equipment = models.CharField(max_length=400, blank=True, null=True, help_text="Additional information of the other rack equipments.")
    recorder_type = models.CharField(max_length=150, help_text="Mention the recorder type.")
    number_of_recorders = models.IntegerField(null=True, blank=True, default=0, help_text="Number of recorders.")
    tape_type = models.CharField(max_length=150, help_text="Mention the tape type of recorders.")
    additional_info = models.CharField(max_length = 400, blank=True, null=True, help_text="Additional information or comments (optional).")
    additional_recorder_type = models.CharField(max_length=400, blank=True, null=True, help_text="Additional information of the recorder type.")
    configuration_types_supported = models.CharField(max_length=400, help_text="Mention the configuration types supported (all in one line and seperated by ;).")
    additional_configuration_info = models.CharField(max_length=400, blank=True, null=True, help_text="Additional information or comments (optional).")
    
    # Meteorological Instrumentation
    humidity_sensor_manufacturer = models.CharField(max_length=150, help_text="Mention the manufacturer of the humidity sensor.")
    humidity_sensor_model = models.CharField(max_length=150, help_text="Mention the model of the humidity sensor.")
    humidity_sensor_accuracy = models.CharField(max_length=150, help_text="Mention the accuracy of the humidity sensor.")
    humidity_sensor_effective_dates = models.CharField(max_length=150, help_text="Mention the effective dates of the humidity sensor.")
    addtional_humidity_sensor_info = models.CharField(max_length=250, blank=True, null=True, help_text="Additional information or comments (optional).")
    pressure_sensor_manufacturer = models.CharField(max_length=150, help_text="Mention the manufacturer of the pressure sensor.")
    pressure_sensor_model = models.CharField(max_length=150, help_text="Mention the model of the pressure sensor.")
    pressure_sensor_accuracy = models.CharField(max_length=150, help_text="Mention the accuracy of the pressure sensor.")
    pressure_sensor_effective_dates = models.CharField(max_length=150, help_text="Mention the effective dates of the pressure sensor.")
    pressure_sensor_height_relative_to_VLBI_in_meters = models.FloatField(null=True, blank=True, default=0.0, help_text="Mention the height relative to VLBI in meters.")
    pressure_sensor_additional_info = models.CharField(max_length=250, blank=True, null=True, help_text="Additional information or comments (optional).")
    temperature_sensor_manufacturer = models.CharField(max_length=150, help_text="Mention the manufacturer of the temperature sensor.")
    temperature_sensor_model = models.CharField(max_length=150, help_text="Mention the model of the temperature sensor.")
    temperature_sensor_accuracy = models.CharField(max_length=150, help_text="Mention the accuracy of the temperature sensor.")
    temperature_sensor_effective_dates = models.CharField(max_length=150, help_text="Mention the effective dates of the temperature sensor.")
    temperature_sensor_additional_info = models.CharField(max_length=250, blank=True, null=True, help_text="Additional information or comments (optional).")

    # Time and frequency standards
    standard_type = models.CharField(max_length=250, help_text="Mention the standard type.")
    installed_dates_duration = models.CharField(max_length=250, help_text="Mention the installed dates duration.")
    manufacturer = models.CharField(max_length=200, help_text="Mention the manufacturer.")
    model_number_or_ID = models.CharField(max_length=150, blank=True, null=True, help_text="Mention the model number or ID.")
    additional_info = models.CharField(max_length=250, blank=True, null=True, help_text="Additional information or comments (optional).")
    
    # Auxilliary equipment information
    first_equipment_type = models.CharField(max_length=150, help_text="Mention the type of equipment.")
    first_installed_dates = models.CharField(max_length=250, help_text="Mention the installed dates.")
    fisrt_manufacturer = models.CharField(max_length=200, help_text="Mention the manufacturer.")
    fisrt_model_number_or_ID = models.CharField(max_length=150, blank=True, null=True, help_text="Mention the model number or ID.")
    first_additional_info = models.CharField(max_length=250, blank=True, null=True, help_text="Additional information or comments (optional).")
    
    second_equipment_type = models.CharField(max_length=150, help_text="Mention the type of equipment.")
    second_installed_dates = models.CharField(max_length=250, help_text="Mention the installed dates.")
    second_manufacturer = models.CharField(max_length=200, help_text="Mention the manufacturer.")
    second_model_number_or_ID = models.CharField(max_length=150, blank=True, null=True, help_text="Mention the model number or ID.")
    second_additional_info = models.CharField(max_length=250, blank=True, null=True, help_text="Additional information or comments (optional).")

    #Co-location information
    instrument_type = models.CharField(max_length=800, help_text="Mention the type of instruments in co_locations and seperate each location by ;.")
    instrument_name = models.CharField(max_length=800, help_text="Mention the name of the instrument in co_locations and seperate each location by ;.")
    status = models.CharField(max_length=800, help_text="Mention the status of the instrument in co_locations and seperate each location by ;.")
    effective_dates = models.CharField(max_length=800, help_text="Mention the effective dates of the instrument in in co_locations and seperate each location by ;.")
    included_in_local_survey = models.TextField(blank=False, null=False, help_text="Did it include in local survey of in co_locations? Seperate each location by ;.")
    additional_info = models.CharField(max_length=800, blank=True, null=True, help_text="Additional information or comments (optional) and seperate each location by ;.")
    
    # Field System computer information
    computer_system_vendor = models.CharField(max_length=250, help_text="Mention the computer system vendor.")
    computer_CPU = models.CharField(max_length=150, help_text="Mention the computer's CPU.")
    computer_CPU_speed_in_MHz = models.FloatField(null=True, blank=True, default=0.0, help_text = "Mention the computer's CPU speed in MHz.")
    computer_memory_in_Mbytes = models.FloatField(null=True, blank=True, default=0.0, help_text = "Mention the computer's memory in Mbytes.")
    computer_disk_in_Gbytes = models.FloatField(null=True, blank=True, default=0.0, help_text = "Mention the computer's disk in Gbytes.")
    computer_Linux_release = models.CharField(max_length=150, blank= True, null= True, help_text="Mention the computer's Linux release.")
    computer_internet_connection = models.CharField(max_length=250, help_text="Mention the computer's internet connection.")
    antenna_interface_type = models.CharField(max_length=150, help_text="Mention the antenna interface type.")
    spare_FS_computer = models.BooleanField(default=False, verbose_name='Spare FS computer?', help_text="Is it a spare FS computer?") 
    known_RFI_sources = models.CharField(max_length=250, help_text="Known RFI sources.")
    
    # On-site contact information
    agency = models.CharField(max_length=250, help_text="Mention the agency.")
    shipping_address = models.CharField(max_length=250, help_text="Mention the shipping address.")
    postal_address = models.CharField(max_length=250, help_text="Mention the postal address.")
    URL_of_site_web_page = models.URLField(max_length=200, blank=True, null=True, help_text="Mention the URL of the site web page.")
    on_site_friend_of_VLBI_name = models.CharField(max_length=150, help_text="Mention the name of the on-site friend of VLBI.")
    primary_telephone_of_on_site_friend_of_VLBI = models.CharField(max_length=50, help_text="Mention the primary telephone of the on-site friend of VLBI.")
    alternative_telephone_of_on_site_friend_of_VLBI = models.CharField(max_length=50, help_text="Mention the alternative telephone of the on-site friend of VLBI.")
    fax_of_on_site_friend_of_VLBI = models.CharField(max_length=50, help_text="Mention the fax of the on-site friend of VLBI.")
    email_of_on_site_friend_of_VLBI = models.EmailField(max_length=254, help_text="Mention the email of the on-site friend of VLBI.")
    primary_telephone_of_VLBI_operations_room = models.CharField(max_length=50, help_text="Mention the primary telephone of the VLBI operations room.")
    alternative_telephone_of_VLBI_operations_room = models.CharField(max_length=50, help_text="Mention the alternative telephone of the VLBI operations room.")
    fax_of_VLBI_operations_room = models.CharField(max_length=50, help_text="Mention the fax of the VLBI operations room.")
    email_of_VLBI_operations_room = models.EmailField(max_length=254, help_text="Mention the email of the VLBI operations room.")
    name_of_other_on_site_contact = models.CharField(max_length=150, help_text="Mention the name of the other on-site contact.")
    primary_telephone_of_other_on_site_contact = models.CharField(max_length=50, help_text="Mention the primary telephone of the other on-site contact.")
    alternative_telephone_of_other_on_site_contact = models.CharField(max_length=50, help_text="Mention the alternative telephone of the other on-site contact.")
    fax_of_other_on_site_contact = models.CharField(max_length=50, help_text="Mention the fax of the other on-site contact.")
    email_of_other_on_site_contact = models.EmailField(max_length=254, help_text="Mention the email of the other on-site contact.")
    additional_info = models.TextField(blank=True, null=True, help_text="Additional information or comments (optional).")
    
    # Responsible agency 
    responsible_agency = models.CharField(max_length=250, help_text="Mention the responsible agency.")
    responsible_agency_shipping_address = models.CharField(max_length=250, blank=True, default="", help_text="Mention the shipping address.")
    responsible_agency_postal_address = models.CharField(max_length=250, blank=True, default="", help_text="Mention the postal address.")
    URL_of_agency_web_page = models.URLField(max_length=200, blank=True, null=True, help_text="Mention the URL of the agency web page.")
    primary_administrative_agency_contact_person = models.CharField(max_length=150, help_text="Mention the primary administrative agency contact.")
    primary_telephone_of_contact_person = models.CharField(max_length=50, help_text="Mention the primary telephone of the contact person.")
    alternative_telephone_of_contact_person = models.CharField(max_length=50, help_text="Mention the alternative telephone of the contact person.")
    fax_of_contact_person = models.CharField(max_length=50, help_text="Mention the fax of the contact person.")
    email_of_contact_person = models.EmailField(max_length=254, help_text="Mention the email of the contact person.")
    alternative_agency_contact = models.CharField(max_length=250, help_text="Mention the alternative agency.")
    alternative_agency_shipping_address = models.CharField(default="Arcisstr. 21, 80333 Munich", max_length=250, help_text="Mention the alternative agency shipping address.")
    alternative_agency_postal_address = models.CharField(default="Arcisstr. 21, 80290 Munich", max_length=250, help_text="Mention the alternative agency postal address.")
    alternative_agency_URL_of_agency_web_page = models.URLField(max_length=200, blank=True, null=True, help_text="Mention the URL of the alternative agency web page.")
    primary_administrative_alternative_agency_contact_person = models.CharField(max_length=150, help_text="Mention the primary administrative alternative agency contact.")
    primary_telephone_of_alternative_agency_contact_person = models.CharField(max_length=50, help_text="Mention the primary telephone of the alternative agency contact person.")
    alternative_contact_person = models.CharField(max_length=150, help_text="Mention the alternative contact person.")
    alternative_telephone = models.CharField(max_length=50, help_text="Mention the alternative telephone.")
    fax_of_alternative_contact_person = models.CharField(max_length=50, help_text="Mention the fax of the alternative contact person.")
    email_of_alternative_contact_person = models.EmailField(max_length=254, help_text="Mention the email of the alternative contact person.")
    additional_info = models.TextField(blank=True, null=True, help_text="Additional information or comments (optional).")
    more_info = models.TextField(blank=True, null=True, help_text="More information (optional).")

    objects = models.Manager()

    #def __str__(self):
    #    return f"ConfigurationInfo (Surveyed: {'Yes' if self.surveyed_into_national_network else 'No'})"
    #def __str__(self):
    #    return f"ConfigurationInfo (IERSResults: {'Yes' if self.results_provided_to_IERS else 'No'})"
    #def __str__(self):
    #    return f"ConfigurationInfo (CDISResults: {'Yes' if self.results_provided_to_CDDIS else 'No'})"
    #def __str__(self):
    #    return f"ConfigurationInfo (SpareFSComputerResults: {'Yes' if self.spare_FS_computer else 'No'})"
    #def __str__(self):
    #   return f"ConfigurationInfo (URLs and files for reference)"
    def __str__(self):
        return f'{self.site_name} - {self.user.username}'
    
auditlog.register(ConfigurationInfo)
