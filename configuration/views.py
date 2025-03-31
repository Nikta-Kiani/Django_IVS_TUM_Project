from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import ContactForm, SiteIdentificationForm, SiteLocalNetworkInfoForm, SiteDescriptiveInfoForm, AntennaDetailsForm, ReceiverForm, CablesReceiverAndBackendForm, DataAcquisitionSystemForm, MeteorologicalInstrumentationForm, TimeAndFrequencyStandardsForm, AuxilliaryEquipmentForm, CoLocationsForm, FieldSystemComputerForm, OnSiteContactForm, ResponsibleAgencyForm
from django.contrib.auth.decorators import login_required
from .models import ConfigurationInfo
from django.http import JsonResponse
import datetime
from django.contrib import messages
from django.http import HttpResponseForbidden

# Create your views here.
#@login_required
def configuration_view(request):
    
     # If the user is authenticated, show a personalized configuration welcome page
    if request.user.is_authenticated:
        return redirect('contact')
    # Render the welcome page with the registration and login forms
    return render(request, 'configuration/configuration.html',{
        'is_authenticated': False,})

#@login_required
def contact_view(request):

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Get cleaned data from the form
            contact_data = form.cleaned_data

            if 'update_date' in contact_data:
                contact_data['update_date'] = contact_data['update_date'].isoformat()

            # Save the cleaned and processed data in the session
            request.session['contact_data'] = contact_data
            return redirect('site_identification')
    else:
        form = ContactForm()
    return render(request, 'configuration/contact.html', {'form': form})

#@login_required
def site_identification_view(request):
    if request.method == 'POST':
        form = SiteIdentificationForm(request.POST)
        if form.is_valid():
            # Get cleaned data from the form
            site_identification_data = form.cleaned_data

            if 'start_date_of_operation' in site_identification_data:
                site_identification_data['start_date_of_operation'] = site_identification_data['start_date_of_operation'].isoformat()

            # Save the cleaned and processed data in the session
            request.session['site_identification_data'] = site_identification_data
            return redirect('site_local_network_info')
    else:
        form = SiteIdentificationForm()
    return render(request, 'configuration/site_identification.html', {'form': form})

#@login_required
def site_local_network_info_view(request):
    if request.method == 'POST':
        form = SiteLocalNetworkInfoForm(request.POST)
        if form.is_valid():
             # Get cleaned data from the form
            site_local_network_info_data = form.cleaned_data

            if 'most_recent_survey_date' in site_local_network_info_data:
                site_local_network_info_data['most_recent_survey_date'] = site_local_network_info_data['most_recent_survey_date'].isoformat()

            # Save the cleaned and processed data in the session
            request.session['site_local_network_info'] = 'site_local_network_info'
            return redirect('site_descriptive_info')
    else:
        form = SiteLocalNetworkInfoForm()
    return render(request, 'configuration/site_local_network_info.html', {'form': form})

#@login_required
def site_descriptive_info_view(request):
    if request.method == 'POST':
        form = SiteDescriptiveInfoForm(request.POST)
        if form.is_valid():
            request.session['site_descriptive_info_data'] = form.cleaned_data
            # Continue with the next tab or the summary page
            return redirect('antenna_details')
    else:
        form = SiteDescriptiveInfoForm()
    return render(request, 'configuration/site_descriptive_info.html', {'form': form})

#@login_required
def antenna_details_view(request):
    if request.method == 'POST':
        form = AntennaDetailsForm(request.POST)
        if form.is_valid():
            # Get cleaned data from the form
           antenna_details_data = form.cleaned_data
            
           if 'start_date_of_occupation' in antenna_details_data:
               antenna_details_data['start_date_of_occupation'] = antenna_details_data['start_date_of_occupation'].isoformat()
           if 'end_date_of_occupation' in antenna_details_data:
               antenna_details_data['end_date_of_occupation'] = antenna_details_data['end_date_of_occupation'].isoformat()
               
            # Save the cleaned and processed data in the session
           request.session['antenna_details_data'] = antenna_details_data
            # Continue with the next tab or the summary page
           return redirect('receiver')
    else:
        form = AntennaDetailsForm()
    return render(request, 'configuration/antenna_details.html', {'form': form})


#@login_required
def receiver_view(request):
    if request.method == 'POST':
        form = ReceiverForm(request.POST)
        if form.is_valid():
            request.session['receiver_data'] = form.cleaned_data
            # Continue with the next tab or the summary page
            return redirect('cables_receiver_and_backend')
    else:
        form = ReceiverForm()
    return render(request, 'configuration/receiver.html', {'form': form})

#@login_required
def cables_receiver_and_backend_view(request):
    if request.method == 'POST':
        form = CablesReceiverAndBackendForm(request.POST)
        if form.is_valid():
            request.session['cables_receiver_and_backend_data'] = form.cleaned_data
            # Continue with the next tab or the summary page
            return redirect('data_acquisition_system')
    else:
        form = CablesReceiverAndBackendForm()
    return render(request, 'configuration/cables_receiver_and_backend.html', {'form': form})

#@login_required
def data_acquisition_system_view(request):
    if request.method == 'POST':
        form = DataAcquisitionSystemForm(request.POST)
        if form.is_valid():
            request.session['data_acquisition_system'] = form.cleaned_data
            # Continue with the next tab or the summary page
            return redirect('meteorological_instrumentation')
    else:
        form = DataAcquisitionSystemForm()
    return render(request, 'configuration/data_acquisition_system.html', {'form': form})

#@login_required
def meteorological_instrumentation_view(request):
    if request.method == 'POST':
        form = MeteorologicalInstrumentationForm(request.POST)
        if form.is_valid():
            request.session['meteorological_instrumentation'] = form.cleaned_data
            # Continue with the next tab or the summary page
            return redirect('time_and_frequency_standards')
    else:
        form = MeteorologicalInstrumentationForm()
    return render(request, 'configuration/meteorological_instrumentation.html', {'form': form})

#@login_required
def time_and_frequency_standards_view(request):
    if request.method == 'POST':
        form = TimeAndFrequencyStandardsForm(request.POST)
        if form.is_valid():
            request.session['time_and_frequency_standards'] = form.cleaned_data
            # Continue with the next tab or the summary page
            return redirect('auxilliary_equipment')
    else:
        form = TimeAndFrequencyStandardsForm()
    return render(request, 'configuration/time_and_frequency_standards.html', {'form': form})

#@login_required
def auxilliary_equipment_view(request):
    if request.method == 'POST':
        form = AuxilliaryEquipmentForm(request.POST)
        if form.is_valid():
            request.session['auxilliary_equipment'] = form.cleaned_data
            # Continue with the next tab or the summary page
            return redirect('co_locations')
    else:
        form = AuxilliaryEquipmentForm()
    return render(request, 'configuration/auxilliary_equipment.html', {'form': form})

#@login_required
def co_locations_view(request):
    if request.method == 'POST':
        form = CoLocationsForm(request.POST)
        if form.is_valid():
            request.session['co_locations'] = form.cleaned_data
            # Continue with the next tab or the summary page
            return redirect('field_system_computer')
    else:
        form = CoLocationsForm()
    return render(request, 'configuration/co_locations.html', {'form': form})

#@login_required
def field_system_computer_view(request):
    if request.method == 'POST':
        form = FieldSystemComputerForm(request.POST)
        if form.is_valid():
            request.session['field_system_computer'] = form.cleaned_data
            # Continue with the next tab or the summary page
            return redirect('on_site_contact')
    else:
        form = FieldSystemComputerForm()
    return render(request, 'configuration/field_system_computer.html', {'form': form})

#@login_required
def on_site_contact_view(request):
    if request.method == 'POST':
        form = OnSiteContactForm(request.POST)
        if form.is_valid():
            request.session['on_site_contact'] = form.cleaned_data
            # Continue with the next tab or the summary page
            return redirect('responsible_agency')
    else:
        form = OnSiteContactForm()
    return render(request, 'configuration/on_site_contact.html', {'form': form})

#@login_required
def responsible_agency_view(request):
    if request.method == 'POST':
        form = ResponsibleAgencyForm(request.POST)
        if form.is_valid():
            request.session['responsible_agency'] = form.cleaned_data
            # Continue with the next tab or the summary page
            return redirect('configuration_summary')
    else:
        form = ResponsibleAgencyForm()
    return render(request, 'configuration/responsible_agency.html', {'form': form})

#@login_required
def configuration_summary_view(request):
    # Gather all the data from the session
    contact_data = request.session.get('contact_data', {})
    site_identification_data = request.session.get('site_identification_data', {})
    site_local_network_info_data = request.session.get('site_local_network_info_data', {})
    site_descriptive_info_data = request.session.get('site_descriptive_info_data', {})
    antenna_details_data = request.session.get('antenna_details_data', {})
    receiver_data = request.session.get('receiver_contact_data', {})
    cables_receiver_and_backend_data = request.session.get('cables_receiver_and_backend_data', {})
    data_acquisition_system_data = request.session.get('data_acquisition_system_data', {})
    meteorological_instrumentation_data = request.session.get('meteorological_instrumentation_data', {})
    time_and_frequency_standards_data = request.session.get('time_and_frequency_standards_data', {})
    auxilliary_equipment_data = request.session.get('auxilliary_equipment_data', {})
    co_locations_data = request.session.get('co_locations_data', {})
    field_system_computer_data = request.session.get('field_system_computer_data', {})
    on_site_contact_data = request.session.get('on_site_contact_data', {})
    responsible_agency_data = request.session.get('responsible_agency_data', {})


    if request.method == 'POST'and request.POST.get("form_type") == "submit_form":
        # Ensure session data is present
        if not contact_data:
            contact_data = {
                'prepared_by_full_name': request.POST.get('prepared_by_full_name'),
                'email': request.POST.get('email'),
                'update_date': request.POST.get('update_date'),
                'report_type': request.POST.get('report_type')
            }

        if not site_identification_data:
            site_identification_data = {
                'site_name': request.POST.get('site_name'),
                'site_8_letter_code': request.POST.get('site_8_letter_code'),
                'site_2_letter_code': request.POST.get('site_2_letter_code'),
                'IERS_domes_number': request.POST.get('IERS_domes_number'),
                'CDP_occupation_code': request.FILES.get('CDP_occupation_code'),
                'CDP_monument_number': request.POST.get('CDP_monument_number'),
                'IGS_station_code': request.POST.get('IGS_station_code'),
                'ILRS_station_name': request.POST.get('ILRS_station_name'),
                'survey_into_national_network': request.POST.get('survey_into_national_network'),
                'start_date_of_operation': request.POST.get('start_date_of_operation'),
                'additional_info': request.POST.get('additional_info')
            }

        if not site_local_network_info_data:
            site_local_network_info_data = {
                'type_of_marker': request.POST.get('type_of_marker'),
                'frequency_of_surveying': request.POST.get('frequency_of_surveying'),
                'surveying_method': request.POST.get('surveying_method'),
                'survey_instruments_used': request.POST.get('survey_instruments_used'),
                'accuracy': request.POST.get('accuracy'),
                'survey_performed_by': request.POST.get('survey_performed_by'),
                'survay_documentation': request.POST.get('survay_documentation'),
                'responsible_person': request.POST.get('responsible_person'),
                'most_recent_survey_date': request.POST.get('most_recent_survey_date'),
                'results_provided_to_IERS': request.POST.get('results_provided_to_IERS'),
                'results_provided_to_CDDIS': request.POST.get('results_provided_to_CDDIS'),
                'number_of_reference_markers': request.POST.get('number_of_reference_markers'),
                'additional_info': request.POST.get('additional_info')
            }

        if not site_descriptive_info_data:
            site_descriptive_info_data = {
                'site_map': request.POST.get('site_map'),
                'site_map_url': request.POST.get('site_map_url'),
                'site_diagram': request.POST.get('site_diagram'),
                'site_diagram_url': request.POST.get('site_diagram_url'),
                'horizon_mask': request.POST.get('horizon_mask'),
                'horizon_mask_url': request.POST.get('horizon_mask_url'),
                'monument_description': request.POST.get('monument_description'),
                'monument_description_url': request.POST.get('monument_description_url'),
                'site_photographs': request.POST.get('site_photographs'),
                'site_photographs_url': request.POST.get('site_photographs_url')
            }

        if not antenna_details_data:
            antenna_details_data = {
                'antenna_type': request.POST.get('antenna_type'),
                'diameter_m': request.POST.get('diameter_m'),
                'axis_type': request.POST.get('axis_type'),
                'axis_offset_m': request.POST.get('axis_offset_m'),
                'slew_rate_first_axis_deg_min': request.POST.get('slew_rate_first_axis_deg_min'),
                'slew_rate_second_axis_deg_min': request.POST.get('slew_rate_second_axis_deg_min'),
                'min_limit_first_axis_deg': request.POST.get('min_limit_first_axis_deg'),
                'max_limit_first_axis_deg': request.POST.get('max_limit_first_axis_deg'),
                'min_limit_second_axis_deg': request.POST.get('min_limit_second_axis_deg'),
                'max_limit_second_axis_deg': request.POST.get('max_limit_second_axis_deg'),
                'horizon_mask_data_azimuth_deg_coressponding_elevationmask_deg': request.POST.get('horizon_mask_data_azimuth_deg_coressponding_elevationmask_deg'),
                'start_date_of_occupation': request.POST.get('start_date_of_occupation'),
                'end_date_of_occupation': request.POST.get('end_date_of_occupation'),
                'additional_info': request.POST.get('additional_info')
            }

        if not receiver_data:
            receiver_data = {
                'feed_location': request.POST.get('feed_location'),
                'feed_type': request.POST.get('feed_type'),
                'x_first_stage_amplifier': request.POST.get('x_first_stage_amplifier'),
                's_first_stage_amplifier': request.POST.get('s_first_stage_amplifier'),
                'x_bandwidth_mhz': request.POST.get('x_bandwidth_mhz'),
                's_bandwidth_mhz': request.POST.get('s_bandwidth_mhz'),
                'x_tsys_at_zenith_k': request.POST.get('x_tsys_at_zenith_k'),
                's_tsys_at_zenith_k': request.POST.get('s_tsys_at_zenith_k'),
                'x_sefd_jy': request.POST.get('x_sefd_jy'),
                's_sefd_jy': request.POST.get('s_sefd_jy'),
                'x_aperture_efficiency': request.POST.get('x_aperture_efficiency'),
                's_aperture_efficiency': request.POST.get('s_aperture_efficiency'),
                'x_lo_frequencies_mhz': request.POST.get('x_lo_frequencies_mhz'),
                's_lo_frequencies_mhz': request.POST.get('s_lo_frequencies_mhz'),
                'phase_calibrator_type': request.POST.get('phase_calibrator_type'),
                'additional_info': request.POST.get('additional_info')
            }

        if not cables_receiver_and_backend_data:
            cables_receiver_and_backend_data = {
                'length_of_cable_run_m': request.POST.get('length_of_cable_run_m'),
                'x_band_cable_type': request.POST.get('x_band_cable_type'),
                'x_band_freq_bandpass_mhz': request.POST.get('x_band_freq_bandpass_mhz'),
                's_band_cable_type': request.POST.get('s_band_cable_type'),
                's_band_freq_bandpass_mhz': request.POST.get('s_band_freq_bandpass_mhz'),
                'lo_ref_signal_cable_type': request.POST.get('lo_ref_signal_cable_type'),
                'lo_ref_signal_freq_mhz': request.POST.get('lo_ref_signal_freq_mhz'),
                'phase_cal_ref_signal_cable_type': request.POST.get('phase_cal_ref_signal_cable_type'),
                'phase_cal_ref_signal_freq_mhz': request.POST.get('phase_cal_ref_signal_freq_mhz'),
                'cable_measure_system_type': request.POST.get('cable_measure_system_type'),
                'additional_info': request.POST.get('additional_info')
            }
            
        if not data_acquisition_system_data:
            data_acquisition_system_data = {
                'type_of_video_converter': request.POST.get('type_of_video_converter'),
                'number_of_mixers': request.POST.get('number_of_mixers'),
                'sidebands_available': request.POST.get('sidebands_available'),
                'number_of_mixers_with_2mhz_filter': request.POST.get('number_of_mixers_with_2mhz_filter'),
                'number_of_mixers_with_4mhz_filter': request.POST.get('number_of_mixers_with_4mhz_filter'),
                'number_of_mixers_with_8mhz_filter': request.POST.get('number_of_mixers_with_8mhz_filter'),
                'number_of_mixers_with_16mhz_filter': request.POST.get('number_of_mixers_with_16mhz_filter'),
                'number_of_mixers_with_32mhz_filter': request.POST.get('number_of_mixers_with_32mhz_filter'),
                'additional_video_converter': request.POST.get('additional_video_converter'),
                'formatter_type': request.POST.get('formatter_type'),
                'serial_number_or_rack_id': request.POST.get('serial_number_or_rack_id'),
                'additional_formattter': request.POST.get('additional_formattter'),
                'decode_type': request.POST.get('decode_type'),
                'additional_decoder': request.POST.get('additional_decoder'),
                'IF_distributor_type': request.POST.get('IF_distributor_type'),
                'additional_IF_distributor': request.POST.get('additional_IF_distributor'),
                'X_down_converter_freq': request.POST.get('X_down_converter_freq'),
                'S_up_down_converter_freq': request.POST.get('S_up_down_converter_freq'),
                'additional_converter': request.POST.get('additional_converter'),
                'other_rack_equipment': request.POST.get('other_rack_equipment'),
                'additional_rack_equipment': request.POST.get('additional_rack_equipment'),
                'recorder_type': request.POST.get('recorder_type'),
                'number_of_recorders': request.POST.get('number_of_recorders'),
                'tape_type': request.POST.get('tape_type'),
                'additional_info': request.POST.get('additional_info'),
                'additional_recorder_type': request.POST.get('additional_recorder_type'),
                'configuration_types_supported': request.POST.get('configuration_types_supported'),
                'additional_configuration_info': request.POST.get('additional_configuration_info')
            }  
        
        if not  meteorological_instrumentation_data:
            meteorological_instrumentation_data = {
                'humidity_sensor_manufacturer': request.POST.get('humidity_sensor_manufacturer'),
                'humidity_sensor_model': request.POST.get('humidity_sensor_model'),
                'humidity_sensor_accuracy': request.POST.get('humidity_sensor_accuracy'),
                'humidity_sensor_effective_dates': request.POST.get('humidity_sensor_effective_dates'),
                'addtional_humidity_sensor_info': request.POST.get('addtional_humidity_sensor_info'),
                'pressure_sensor_manufacturer': request.POST.get('tpressure_sensor_manufacturer'),
                'pressure_sensor_model': request.POST.get('pressure_sensor_model'),
                'pressure_sensor_accuracy': request.POST.get('pressure_sensor_accuracy'),
                'pressure_sensor_effective_dates': request.POST.get('pressure_sensor_effective_dates'),
                'pressure_sensor_height_relative_to_VLBI_in_meters': request.POST.get('pressure_sensor_height_relative_to_VLBI_in_meters'),
                'pressure_sensor_additional_info': request.POST.get('pressure_sensor_additional_info'),
                'temperature_sensor_manufacturer': request.POST.get('temperature_sensor_manufacturer'),
                'temperature_sensor_model': request.POST.get('temperature_sensor_model'),
                'temperature_sensor_accuracy': request.POST.get('temperature_sensor_accuracy'),
                'temperature_sensor_effective_dates': request.POST.get('temperature_sensor_effective_dates'),
                'temperature_sensor_additional_info': request.POST.get('temperature_sensor_additional_info')
            }
        
        if not time_and_frequency_standards_data:
            time_and_frequency_standards_data = {
                'standard_type': request.POST.get('standard_type'),
                'installed_dates_duration': request.POST.get('installed_dates_duration'),
                'manufacturer': request.POST.get('manufacturer'),
                'model_number_or_ID': request.POST.get('model_number_or_ID'),
                'additional_info': request.POST.get('additional_info')
            }
            
        if not auxilliary_equipment_data:
            auxilliary_equipment_data = {
                'first_equipment_type': request.POST.get('first_equipment_type'),
                'first_installed_dates': request.POST.get('first_installed_dates'),
                'fisrt_manufacturer': request.POST.get('afisrt_manufacturer'),
                'fisrt_model_number_or_ID': request.POST.get('fisrt_model_number_or_ID'),
                'first_additional_info': request.POST.get('first_additional_info'),
                'second_equipment_type': request.POST.get('second_equipment_type'),
                'second_installed_dates': request.POST.get('second_installed_dates'),
                'second_manufacturer': request.POST.get('second_manufacturer'),
                'second_model_number_or_ID': request.POST.get('second_model_number_or_ID'),
                'second_additional_info': request.POST.get('second_additional_info')
            }
        
        if not co_locations_data:
            co_locations_data = {
                'instrument_type': request.POST.get('instrument_type'),
                'instrument_name': request.POST.get('instrument_name'),
                'status': request.POST.get('status'),
                'effective_dates': request.POST.get('effective_dates'),
                'included_in_local_survey': request.POST.get('included_in_local_survey'),
                'additional_info': request.POST.get('additional_info')
            }
        if not field_system_computer_data:
            field_system_computer_data = {
                'computer_system_vendor': request.POST.get('computer_system_vendor'),
                'computer_CPU': request.POST.get('computer_CPU'),
                'computer_CPU_speed_in_MHz': request.POST.get('computer_CPU_speed_in_MHz'),
                'computer_memory_in_Mbytes': request.POST.get('computer_memory_in_Mbytes'),
                'computer_disk_in_Gbytes': request.POST.get('computer_disk_in_Gbytes'),
                'computer_Linux_release': request.POST.get('computer_Linux_release'),
                'computer_internet_connection': request.POST.get('computer_internet_connection'),
                'antenna_interface_type': request.POST.get('antenna_interface_type'),
                'spare_FS_computer': request.POST.get('spare_FS_computer'),
                'known_RFI_sources': request.POST.get('known_RFI_sources')
            }
        if not on_site_contact_data:
            on_site_contact_data = {
                'agency': request.POST.get('agency'),
                'shipping_address': request.POST.get('shipping_address'),
                'postal_address': request.POST.get('postal_address'),
                'URL_of_site_web_page': request.POST.get('URL_of_site_web_page'),
                'on_site_friend_of_VLBI_name': request.POST.get('on_site_friend_of_VLBI_name'),
                'primary_telephone_of_on_site_friend_of_VLBI': request.POST.get('primary_telephone_of_on_site_friend_of_VLBI'),
                'alternative_telephone_of_on_site_friend_of_VLBI': request.POST.get('alternative_telephone_of_on_site_friend_of_VLBI'),
                'fax_of_on_site_friend_of_VLBI': request.POST.get('fax_of_on_site_friend_of_VLBI'),
                'email_of_on_site_friend_of_VLBI': request.POST.get('email_of_on_site_friend_of_VLBI'),
                'primary_telephone_of_VLBI_operations_room': request.POST.get('primary_telephone_of_VLBI_operations_room'),
                'alternative_telephone_of_VLBI_operations_room': request.POST.get('alternative_telephone_of_VLBI_operations_room'),
                'fax_of_VLBI_operations_room': request.POST.get('fax_of_VLBI_operations_room'),
                'email_of_VLBI_operations_room': request.POST.get('email_of_VLBI_operations_room'),
                'name_of_other_on_site_contact': request.POST.get('name_of_other_on_site_contact'),
                'primary_telephone_of_other_on_site_contact': request.POST.get('primary_telephone_of_other_on_site_contact'),
                'alternative_telephone_of_other_on_site_contact': request.POST.get('alternative_telephone_of_other_on_site_contact'),
                'fax_of_other_on_site_contact': request.POST.get('fax_of_other_on_site_contact'),
                'email_of_other_on_site_contact': request.POST.get('email_of_other_on_site_contact'),
                'additional_info': request.POST.get('additional_info')
            }

        if not responsible_agency_data:
            responsible_agency_data = {
                'responsible_agency': request.POST.get('responsible_agency'),
                'shipping_address': request.POST.get('shipping_address'),
                'postal_address': request.POST.get('postal_address'),
                'URL_of_agency_web_page': request.POST.get('URL_of_agency_web_page'),
                'primary_administrative_agency_contact_person': request.POST.get('primary_administrative_agency_contact_person'),
                'primary_telephone_of_contact_person': request.POST.get('primary_telephone_of_contact_person'),
                'alternative_telephone_of_contact_person': request.POST.get('alternative_telephone_of_contact_person'),
                'fax_of_contact_person': request.POST.get('fax_of_contact_person'),
                'email_of_contact_person': request.POST.get('email_of_contact_person'),
                'alternative_agency_contact': request.POST.get('alternative_agency_contact'),
                'alternative_agency_shipping_address': request.POST.get('alternative_agency_shipping_address'),
                'alternative_agency_postal_address': request.POST.get('alternative_agency_postal_address'),
                'alternative_agency_URL_of_agency_web_page': request.POST.get('alternative_agency_URL_of_agency_web_page'),
                'primary_administrative_alternative_agency_contact_person': request.POST.get('primary_administrative_alternative_agency_contact_person'),
                'primary_telephone_of_alternative_agency_contact_person': request.POST.get('primary_telephone_of_alternative_agency_contact_person'),
                'alternative_contact_person': request.POST.get('alternative_contact_person'),
                'alternative_telephone': request.POST.get('alternative_telephone'),
                'fax_of_alternative_contact_person': request.POST.get('fax_of_alternative_contact_person'),
                'email_of_alternative_contact_person': request.POST.get('email_of_alternative_contact_person'),
                'additional_info': request.POST.get('additional_info'),
                'more_info': request.POST.get('more_info'),
            }

    # Check if the user is authenticated
        if request.user.is_authenticated:
        # If the form is submitted, save the data to the model
            configuration_info = ConfigurationInfo(
            user=request.user,
            prepared_by_full_name=contact_data.get('prepared_by_full_name'),
            email=contact_data.get('email'),
            update_date=contact_data.get('update_date'),
            report_type=contact_data.get('report_type'),

            site_name=site_identification_data.get('site_name'),
            site_8_letter_code=site_identification_data.get('site_8_letter_code'),
            site_2_letter_code=site_identification_data.get('site_2_letter_code'),
            IERS_domes_number=site_identification_data.get('IERS_domes_number'),
            CDP_occupation_code=site_identification_data.get('CDP_occupation_code'),
            CDP_monument_number=site_identification_data.get('CDP_monument_number'),
            IGS_station_code=site_identification_data.get('IGS_station_code'),
            ILRS_station_name=site_identification_data.get('ILRS_station_name'),
            survey_info_national_network=site_identification_data.get('survey_info_national_network'),
            start_date_of_operation=site_identification_data.get('start_date_of_operation'),
            additional_info=site_identification_data.get('additional_info'),
            
            type_of_marker=site_local_network_info_data.get('type_of_marker'),
            frequency_of_surveying=site_local_network_info_data.get('frequency_of_surveying'),
            surveying_method=site_local_network_info_data.get('surveying_method'),
            survey_instruments_used=site_local_network_info_data.get('survey_instruments_used'),
            accuracy=site_local_network_info_data.get('accuracy'),
            survey_performed_by=site_local_network_info_data.get('survey_performed_by'),
            survay_documentation=site_local_network_info_data.get('survay_documentation'),
            responsible_person=site_local_network_info_data.get('responsible_person'),
            most_recent_survey_date=site_local_network_info_data.get('most_recent_survey_date'),
            results_provided_to_IERS=site_local_network_info_data.get('results_provided_to_IERS'),
            results_provided_to_CDDIS=site_local_network_info_data.get('results_provided_to_CDDIS'),
            number_of_reference_markers=site_local_network_info_data.get('number_of_reference_markers'),
            local_additional_info=site_local_network_info_data.get('additional_info'),

            site_map=site_descriptive_info_data.get('site_map'),
            site_map_url=site_descriptive_info_data.get('site_map_url'),
            site_diagram=site_descriptive_info_data.get('site_diagram'),
            site_diagram_url=site_descriptive_info_data.get('site_diagram_url'),
            horizon_mask=site_descriptive_info_data.get('horizon_mask'),
            horizon_mask_url=site_descriptive_info_data.get('horizon_mask_url'),
            monument_description=site_descriptive_info_data.get('monument_description'),
            monument_description_url=site_descriptive_info_data.get('monument_description_url'),
            site_photographs=site_descriptive_info_data.get('site_photographs'),
            site_photographs_url=site_descriptive_info_data.get('site_photographs_url'),

            antenna_type=antenna_details_data.get('antenna_type'),
            diameter_m=antenna_details_data.get('diameter_m'),
            axis_type=antenna_details_data.get('axis_type'),
            axis_offset_m=antenna_details_data.get('axis_offset_m'),
            slew_rate_first_axis_deg_min=antenna_details_data.get('slew_rate_first_axis_deg_min'),
            slew_rate_second_axis_deg_min=antenna_details_data.get('slew_rate_second_axis_deg_min'),
            min_limit_first_axis_deg=antenna_details_data.get('min_limit_first_axis_deg'),
            max_limit_first_axis_deg=antenna_details_data.get('max_limit_first_axis_deg'),
            min_limit_second_axis_deg=antenna_details_data.get('min_limit_second_axis_deg'),
            max_limit_second_axis_deg=antenna_details_data.get('max_limit_second_axis_deg'),
            horizon_mask_data_azimuth_deg_coressponding_elevationmask_deg=antenna_details_data.get('horizon_mask_data_azimuth_deg_coressponding_elevationmask_deg'),
            start_date_of_occupation=antenna_details_data.get('start_date_of_occupation'),
            end_date_of_occupation=antenna_details_data.get('end_date_of_occupation'),
            antenna_additional_info=antenna_details_data.get('additional_info'),

            feed_location=receiver_data.get('feed_location'),
            feed_type=receiver_data.get('feed_type'),
            x_first_stage_amplifier=receiver_data.get('x_first_stage_amplifier'),
            s_first_stage_amplifier=receiver_data.get('s_first_stage_amplifier'),
            x_bandwidth_mhz=receiver_data.get('x_bandwidth_mhz'),
            s_bandwidth_mhz=receiver_data.get('s_bandwidth_mhz'),
            x_tsys_at_zenith_k=receiver_data.get('x_tsys_at_zenith_k'),
            s_tsys_at_zenith_k=receiver_data.get('s_tsys_at_zenith_k'),
            x_sefd_jy=receiver_data.get('x_sefd_jy'),
            s_sefd_jy=receiver_data.get('s_sefd_jy'),
            x_aperture_efficiency=receiver_data.get('x_aperture_efficiency'),
            s_aperture_efficiency=receiver_data.get('s_first_stage_amplifier'),
            x_lo_frequencies_mhz=receiver_data.get('x_lo_frequencies_mhz'),
            s_lo_frequencies_mhz=receiver_data.get('s_lo_frequencies_mhz'),
            phase_calibrator_type=receiver_data.get('phase_calibrator_type'),
            receiver_additional_info=receiver_data.get('additional_info'),

            length_of_cable_run_m=cables_receiver_and_backend_data.get('length_of_cable_run_m'),
            x_band_cable_type=cables_receiver_and_backend_data.get('x_band_cable_type'),
            x_band_freq_bandpass_mhz=cables_receiver_and_backend_data.get('x_band_freq_bandpass_mhz'),
            s_band_cable_type=cables_receiver_and_backend_data.get('s_band_cable_type'),
            s_band_freq_bandpass_mhz=cables_receiver_and_backend_data.get('s_band_freq_bandpass_mhz'),
            lo_ref_signal_cable_type=cables_receiver_and_backend_data.get('lo_ref_signal_cable_type'),
            lo_ref_signal_freq_mhz=cables_receiver_and_backend_data.get('lo_ref_signal_freq_mhz'),
            phase_cal_ref_signal_cable_type=cables_receiver_and_backend_data.get('phase_cal_ref_signal_cable_type'),
            phase_cal_ref_signal_freq_mhz=cables_receiver_and_backend_data.get('phase_cal_ref_signal_freq_mhz'),
            cable_measure_system_type=cables_receiver_and_backend_data.get('cable_measure_system_type'),
            cables_additional_info=cables_receiver_and_backend_data.get('additional_info'),
            
            type_of_video_converter=data_acquisition_system_data.get('type_of_video_converter'),
            number_of_mixers=data_acquisition_system_data.get('number_of_mixers'),
            sidebands_available=data_acquisition_system_data.get('sidebands_available'),
            number_of_mixers_with_2mhz_filter=data_acquisition_system_data.get('number_of_mixers_with_2mhz_filter'),
            number_of_mixers_with_4mhz_filter=data_acquisition_system_data.get('number_of_mixers_with_4mhz_filter'),
            number_of_mixers_with_8mhz_filter=data_acquisition_system_data.get('number_of_mixers_with_8mhz_filter'),
            number_of_mixers_with_16mhz_filter=data_acquisition_system_data.get('number_of_mixers_with_16mhz_filter'),
            number_of_mixers_with_32mhz_filter=data_acquisition_system_data.get('number_of_mixers_with_32mhz_filter'),
            additional_video_converter=data_acquisition_system_data.get('additional_video_converter'),
            formatter_type=data_acquisition_system_data.get('formatter_type'),
            serial_number_or_rack_id=data_acquisition_system_data.get('serial_number_or_rack_id'),
            additional_formattter=data_acquisition_system_data.get('additional_formattter'),
            decode_type=data_acquisition_system_data.get('decode_type'),
            additional_decoder=data_acquisition_system_data.get('additional_decoder'),
            IF_distributor_type=data_acquisition_system_data.get('IF_distributor_type'),
            additional_IF_distributor=data_acquisition_system_data.get('additional_IF_distributor'),
            X_down_converter_freq=data_acquisition_system_data.get('X_down_converter_freq'),
            S_up_down_converter_freq=data_acquisition_system_data.get('S_up_down_converter_freq'),
            additional_converter=data_acquisition_system_data.get('additional_converter'),
            other_rack_equipment=data_acquisition_system_data.get('other_rack_equipment'),
            additional_rack_equipment=data_acquisition_system_data.get('additional_rack_equipment'),
            recorder_type=data_acquisition_system_data.get('recorder_type'),
            number_of_recorders=data_acquisition_system_data.get('number_of_recorders'),
            tape_type=data_acquisition_system_data.get('tape_type'),
            data_additional_info=data_acquisition_system_data.get('additional_info'),
            additional_recorder_type=data_acquisition_system_data.get('additional_recorder_type'),
            configuration_types_supported=data_acquisition_system_data.get('configuration_types_supported'),
            additional_configuration_info=data_acquisition_system_data.get('additional_configuration_info'),
            
            humidity_sensor_manufacturer=meteorological_instrumentation_data.get('humidity_sensor_manufacturer'),
            humidity_sensor_model=meteorological_instrumentation_data.get('humidity_sensor_model'),
            humidity_sensor_accuracy=meteorological_instrumentation_data.get('humidity_sensor_accuracy'),
            humidity_sensor_effective_dates=meteorological_instrumentation_data.get('humidity_sensor_effective_dates'),
            addtional_humidity_sensor_info=meteorological_instrumentation_data.get('addtional_humidity_sensor_info'),
            pressure_sensor_manufacturer=meteorological_instrumentation_data.get('pressure_sensor_manufacturer'),
            pressure_sensor_model=meteorological_instrumentation_data.get('pressure_sensor_model'),
            pressure_sensor_accuracy=meteorological_instrumentation_data.get('pressure_sensor_accuracy'),
            pressure_sensor_effective_dates=meteorological_instrumentation_data.get('pressure_sensor_effective_dates'),
            pressure_sensor_height_relative_to_VLBI_in_meters=meteorological_instrumentation_data.get('pressure_sensor_height_relative_to_VLBI_in_meters'),
            pressure_sensor_additional_info=meteorological_instrumentation_data.get('pressure_sensor_additional_info'),
            temperature_sensor_manufacturer=meteorological_instrumentation_data.get('temperature_sensor_manufacturer'),
            temperature_sensor_model=meteorological_instrumentation_data.get('temperature_sensor_model'),
            temperature_sensor_accuracy=meteorological_instrumentation_data.get('temperature_sensor_accuracy'),
            temperature_sensor_effective_dates=meteorological_instrumentation_data.get('temperature_sensor_effective_dates'),
            temperature_sensor_additional_info=meteorological_instrumentation_data.get('temperature_sensor_additional_info'),
            
            standard_type=time_and_frequency_standards_data.get('standard_type'),
            installed_dates_duration=time_and_frequency_standards_data.get('installed_dates_duration'),
            manufacturer=time_and_frequency_standards_data.get('manufacturer'),
            model_number_or_ID=time_and_frequency_standards_data.get('model_number_or_ID'),
            time_and_frequency_additional_info=time_and_frequency_standards_data.get('additional_info'),

            first_equipment_type=auxilliary_equipment_data.get('first_equipment_type'),
            first_installed_dates=auxilliary_equipment_data.get('first_installed_dates'),
            fisrt_manufacturer=auxilliary_equipment_data.get('fisrt_manufacturer'),
            fisrt_model_number_or_ID=auxilliary_equipment_data.get('fisrt_model_number_or_ID'),
            first_additional_info=auxilliary_equipment_data.get('first_additional_info'),
            second_equipment_type=auxilliary_equipment_data.get('second_equipment_type'),
            second_installed_dates=auxilliary_equipment_data.get('second_installed_dates'),
            second_manufacturer=auxilliary_equipment_data.get('second_manufacturer'),
            second_additional_info=auxilliary_equipment_data.get('second_additional_info'),
            
            instrument_type=co_locations_data.get('instrument_type'),
            instrument_name=co_locations_data.get('instrument_name'),
            status=co_locations_data.get('status'),
            effective_dates=co_locations_data.get('effective_dates'),
            included_in_local_survey=co_locations_data.get('included_in_local_survey'),
            co_locations_additional_info=co_locations_data.get('additional_info'),
            
            computer_system_vendor=field_system_computer_data.get('computer_system_vendor'),
            computer_CPU=field_system_computer_data.get('computer_CPU'),
            computer_CPU_speed_in_MHz=field_system_computer_data.get('computer_CPU_speed_in_MHz'),
            computer_memory_in_Mbytes=field_system_computer_data.get('computer_memory_in_Mbytes'),
            computer_disk_in_Gbytes=field_system_computer_data.get('computer_disk_in_Gbytes'),
            computer_Linux_release=field_system_computer_data.get('computer_Linux_release'),
            computer_internet_connection=field_system_computer_data.get('computer_internet_connection'),
            antenna_interface_type=field_system_computer_data.get('antenna_interface_type'),
            spare_FS_computer=field_system_computer_data.get('spare_FS_computer'),
            known_RFI_sources=field_system_computer_data.get('known_RFI_sources'),
            
            agency=on_site_contact_data.get('agency'),
            agency_shipping_address=on_site_contact_data.get('shipping_address'),
            agency_postal_address=on_site_contact_data.get('postal_address'),
            agency_URL_of_site_web_page=on_site_contact_data.get('URL_of_site_web_page'),
            on_site_friend_of_VLBI_name=on_site_contact_data.get('on_site_friend_of_VLBI_name'),
            primary_telephone_of_on_site_friend_of_VLBI=on_site_contact_data.get('primary_telephone_of_on_site_friend_of_VLBI'),
            alternative_telephone_of_on_site_friend_of_VLBI=on_site_contact_data.get('alternative_telephone_of_on_site_friend_of_VLBI'),
            fax_of_on_site_friend_of_VLBI=on_site_contact_data.get('fax_of_on_site_friend_of_VLBI'),
            email_of_on_site_friend_of_VLBI=on_site_contact_data.get('email_of_on_site_friend_of_VLBI'),
            primary_telephone_of_VLBI_operations_room=on_site_contact_data.get('primary_telephone_of_VLBI_operations_room'),
            alternative_telephone_of_VLBI_operations_room=on_site_contact_data.get('alternative_telephone_of_VLBI_operations_room'),
            fax_of_VLBI_operations_room=on_site_contact_data.get('fax_of_VLBI_operations_room'),
            email_of_VLBI_operations_room=on_site_contact_data.get('email_of_VLBI_operations_room'),
            name_of_other_on_site_contact=on_site_contact_data.get('name_of_other_on_site_contact'),
            primary_telephone_of_other_on_site_contact=on_site_contact_data.get('primary_telephone_of_other_on_site_contact'),
            alternative_telephone_of_other_on_site_contact=on_site_contact_data.get('alternative_telephone_of_other_on_site_contact'),
            fax_of_other_on_site_contact=on_site_contact_data.get('fax_of_other_on_site_contact'),
            email_of_other_on_site_contact=on_site_contact_data.get('email_of_other_on_site_contact'),
            on_site_additional_info=on_site_contact_data.get('additional_info'),
            
            responsible_agency=responsible_agency_data.get('responsible_agency'),
            shipping_address=responsible_agency_data.get('shipping_address'),
            postal_address=responsible_agency_data.get('postal_address'),
            URL_of_agency_web_page=responsible_agency_data.get('URL_of_agency_web_page'),
            primary_administrative_agency_contact_person=responsible_agency_data.get('primary_administrative_agency_contact_person'),
            primary_telephone_of_contact_person=responsible_agency_data.get('primary_telephone_of_contact_person'),
            alternative_telephone_of_contact_person=responsible_agency_data.get('alternative_telephone_of_contact_person'),
            fax_of_contact_person=responsible_agency_data.get('fax_of_contact_person'),
            email_of_contact_person=responsible_agency_data.get('email_of_contact_person'),
            alternative_agency_contact=responsible_agency_data.get('alternative_agency_contact'),
            alternative_agency_shipping_address=responsible_agency_data.get('alternative_agency_shipping_address'),
            alternative_agency_postal_address=responsible_agency_data.get('alternative_agency_postal_address'),
            alternative_agency_URL_of_agency_web_page=responsible_agency_data.get('alternative_agency_URL_of_agency_web_page'),
            primary_administrative_alternative_agency_contact_person=responsible_agency_data.get('primary_administrative_alternative_agency_contact_person'),
            primary_telephone_of_alternative_agency_contact_person=responsible_agency_data.get('primary_telephone_of_alternative_agency_contact_person'),
            alternative_contact_person=responsible_agency_data.get('alternative_contact_person'),
            alternative_telephone=responsible_agency_data.get('alternative_telephone'),
            fax_of_alternative_contact_person=responsible_agency_data.get('fax_of_alternative_contact_person'),
            email_of_alternative_contact_person=responsible_agency_data.get('email_of_alternative_contact_person'),
            reponsible_agency_additional_info=responsible_agency_data.get('additional_info'),
            more_info=responsible_agency_data.get('more_info'),
        )  
          
            configuration_info.save()
                # Clear session after saving
            request.session.flush()

            return redirect('logbook')  # Redirect to the logbook page after saving
        else:
        # Handle the case where the user is not authenticated
            messages.error(request, 'You must be logged in to submit the configuration.')
            return redirect('login')  # Redirect to the login page
     # Combine all the data into one context dictionary
    context = {
        'contact_data': contact_data,
        'site_identification_data': site_identification_data,
        'site_local_network_info_data': site_local_network_info_data,
        'site_descriptive_info_data': site_descriptive_info_data,
        'antenna_details_data': antenna_details_data,
        'receiver_data': receiver_data,
        'cables_receiver_and_backend_data': cables_receiver_and_backend_data,
        'data_acquisition_system_data': data_acquisition_system_data,
        'meteorological_instrumentation_data': meteorological_instrumentation_data,
        'time_and_frequency_standards_data': time_and_frequency_standards_data,
        'auxilliary_equipment_data': auxilliary_equipment_data,
        'co_locations_data': co_locations_data,
        'field_system_computer_data': field_system_computer_data,
        'on_site_contact_data': on_site_contact_data,
        'responsible_agency_data': responsible_agency_data
    }

    return render(request, 'configuration/summary.html', context)

#@login_required
#def user_antenna_data(request):
#    user_antenna_data = AntennaInfo.objects.filter(user=request.user)
#   return render(request, 'antenna/user_data.html', {'antenna_data': user_antenna_data})