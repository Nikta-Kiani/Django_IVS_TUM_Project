from django import forms
from .models import ConfigurationInfo

class ContactForm(forms.ModelForm):
    class Meta:
        model = ConfigurationInfo
        fields = ['prepared_by_full_name', 'email', 'update_date', 'report_type']
        widgets = {'update_date': forms.DateInput(attrs={'type': 'date'})}

class SiteIdentificationForm(forms.ModelForm):
    class Meta:
        model = ConfigurationInfo
        fields = ['site_name', 'site_8_letter_code', 'site_2_letter_code', 'IERS_domes_number', 'CDP_occupation_code', 'CDP_monument_number',
                  'IGS_station_code', 'ILRS_station_name', 'survey_into_national_network', 'start_date_of_operation', 'additional_info']
        widgets = {'start_date_of_operation': forms.DateInput(attrs={'type': 'date'})}

class SiteLocalNetworkInfoForm(forms.ModelForm):
    class Meta:
        model = ConfigurationInfo
        fields = ['type_of_marker', 'frequency_of_surveying', 'surveying_method', 'survey_instruments_used', 'accuracy', 'survey_performed_by',
                  'survay_documentation', 'responsible_person', 'most_recent_survey_date', 'results_provided_to_IERS', 'results_provided_to_CDDIS',
                  'number_of_reference_markers', 'additional_info']
        widgets = {'most_recent_survey_date': forms.DateInput(attrs={'type': 'date'})}
    
class SiteDescriptiveInfoForm(forms.ModelForm):
    class Meta:
        model = ConfigurationInfo
        fields = ['site_map', 'site_map_url', 'site_diagram', 'site_diagram_url', 'horizon_mask', 'horizon_mask_url', 'monument_description',
                  'monument_description_url', 'site_photographs', 'site_photographs_url']
        
class AntennaDetailsForm(forms.ModelForm):
    class Meta:
        model = ConfigurationInfo
        fields = ['antenna_type', 'diameter_m', 'axis_type', 'axis_offset_m', 'slew_rate_first_axis_deg_min', 'slew_rate_second_axis_deg_min',
                  'min_limit_first_axis_deg', 'max_limit_first_axis_deg', 'min_limit_second_axis_deg', 'max_limit_second_axis_deg',
                  'horizon_mask_data_azimuth_deg_coressponding_elevationmask_deg', 'start_date_of_occupation', 'end_date_of_occupation', 'additional_info']
        widgets = {'start_date_of_occupation': forms.DateInput(attrs={'type': 'date'})}
        widgets = {'end_date_of_occupation': forms.DateInput(attrs={'type': 'date'})}
        
class ReceiverForm(forms.ModelForm):
    class Meta:
        model = ConfigurationInfo
        fields = ['feed_location', 'feed_type', 'x_first_stage_amplifier', 's_first_stage_amplifier', 'x_bandwidth_mhz', 's_bandwidth_mhz', 'x_tsys_at_zenith_k',
                  's_tsys_at_zenith_k', 'x_sefd_jy', 's_sefd_jy', 'x_aperture_efficiency', 's_aperture_efficiency', 'x_lo_frequencies_mhz', 's_lo_frequencies_mhz',
                  'phase_calibrator_type', 'additional_info']

class CablesReceiverAndBackendForm(forms.ModelForm):
    class Meta:
        model = ConfigurationInfo
        fields = ['length_of_cable_run_m', 'x_band_cable_type', 'x_band_freq_bandpass_mhz', 's_band_cable_type', 's_band_freq_bandpass_mhz', 'lo_ref_signal_cable_type',
                  'lo_ref_signal_freq_mhz', 'phase_cal_ref_signal_cable_type', 'phase_cal_ref_signal_freq_mhz', 'cable_measure_system_type', 'additional_info']
        
class DataAcquisitionSystemForm(forms.ModelForm):
    class Meta:
        model = ConfigurationInfo
        fields = ['type_of_video_converter', 'number_of_mixers', 'sidebands_available', 'number_of_mixers_with_2mhz_filter', 'number_of_mixers_with_4mhz_filter',
                  'number_of_mixers_with_8mhz_filter', 'number_of_mixers_with_16mhz_filter', 'number_of_mixers_with_32mhz_filter', 'additional_video_converter',
                  'formatter_type', 'serial_number_or_rack_id', 'additional_formattter', 'decode_type', 'additional_decoder', 'IF_distributor_type',
                  'additional_IF_distributor', 'X_down_converter_freq', 'S_up_down_converter_freq', 'additional_converter', 'other_rack_equipment',
                  'additional_rack_equipment', 'recorder_type', 'number_of_recorders', 'tape_type', 'additional_info', 'additional_recorder_type',
                  'configuration_types_supported', 'additional_configuration_info']
        
class MeteorologicalInstrumentationForm(forms.ModelForm):
    class Meta:
        model = ConfigurationInfo
        fields = ['humidity_sensor_manufacturer', 'humidity_sensor_model', 'humidity_sensor_accuracy', 'humidity_sensor_effective_dates',
                  'addtional_humidity_sensor_info', 'pressure_sensor_manufacturer', 'pressure_sensor_model', 'pressure_sensor_accuracy',
                  'pressure_sensor_effective_dates', 'pressure_sensor_height_relative_to_VLBI_in_meters', 'pressure_sensor_additional_info',
                  'temperature_sensor_manufacturer', 'temperature_sensor_model', 'temperature_sensor_accuracy', 'temperature_sensor_effective_dates',
                  'temperature_sensor_additional_info']
        
class TimeAndFrequencyStandardsForm(forms.ModelForm):
     class Meta:
        model = ConfigurationInfo
        fields = ['standard_type', 'installed_dates_duration', 'manufacturer', 'model_number_or_ID', 'additional_info']
        
class AuxilliaryEquipmentForm(forms.ModelForm):
    class Meta:
        model = ConfigurationInfo
        fields = ['first_equipment_type', 'first_installed_dates', 'fisrt_manufacturer', 'fisrt_model_number_or_ID', 'first_additional_info',
                  'second_equipment_type', 'second_installed_dates', 'second_manufacturer', 'second_model_number_or_ID', 'second_additional_info'] 
        
class CoLocationsForm(forms.ModelForm):
    class Meta:
        model = ConfigurationInfo
        fields = ['instrument_type', 'instrument_name', 'status', 'effective_dates', 'included_in_local_survey', 'additional_info']
        
class FieldSystemComputerForm(forms.ModelForm):
    class Meta:
        model = ConfigurationInfo
        fields = ['computer_system_vendor', 'computer_CPU', 'computer_CPU_speed_in_MHz', 'computer_memory_in_Mbytes', 'computer_disk_in_Gbytes',
                  'computer_Linux_release', 'computer_internet_connection', 'antenna_interface_type', 'spare_FS_computer', 'known_RFI_sources']

class OnSiteContactForm(forms.ModelForm):
    class Meta:
        model = ConfigurationInfo
        fields = ['agency', 'shipping_address', 'postal_address', 'URL_of_site_web_page', 'on_site_friend_of_VLBI_name', 'primary_telephone_of_on_site_friend_of_VLBI',
                  'alternative_telephone_of_on_site_friend_of_VLBI', 'fax_of_on_site_friend_of_VLBI', 'email_of_on_site_friend_of_VLBI',
                  'primary_telephone_of_VLBI_operations_room', 'alternative_telephone_of_VLBI_operations_room', 'fax_of_VLBI_operations_room',
                  'email_of_VLBI_operations_room', 'name_of_other_on_site_contact', 'primary_telephone_of_other_on_site_contact',
                  'alternative_telephone_of_other_on_site_contact', 'fax_of_other_on_site_contact', 'email_of_other_on_site_contact', 'additional_info']

class ResponsibleAgencyForm(forms.ModelForm):
    class Meta:
        model = ConfigurationInfo
        fields = ['responsible_agency', 'shipping_address', 'postal_address', 'URL_of_agency_web_page', 'primary_administrative_agency_contact_person',
                  'primary_telephone_of_contact_person', 'alternative_telephone_of_contact_person', 'fax_of_contact_person',
                  'email_of_contact_person', 'alternative_agency_contact', 'alternative_agency_shipping_address', 'alternative_agency_postal_address',
                  'alternative_agency_URL_of_agency_web_page', 'primary_administrative_alternative_agency_contact_person',
                  'primary_telephone_of_alternative_agency_contact_person', 'alternative_contact_person', 'alternative_telephone',
                  'fax_of_alternative_contact_person', 'email_of_alternative_contact_person', 'additional_info', 'more_info']