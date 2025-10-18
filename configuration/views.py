from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import ContactForm, SiteIdentificationForm, SiteLocalNetworkInfoForm, SiteDescriptiveInfoForm, AntennaDetailsForm, ReceiverForm, CablesReceiverAndBackendForm, DataAcquisitionSystemForm, MeteorologicalInstrumentationForm, TimeAndFrequencyStandardsForm, AuxilliaryEquipmentForm, CoLocationsForm, FieldSystemComputerForm, OnSiteContactForm, ResponsibleAgencyForm
from django.contrib.auth.decorators import login_required
from .models import ConfigurationInfo
from django.http import JsonResponse
import datetime
from django.contrib import messages
from django.http import HttpResponseForbidden
from auditlog.registry import auditlog

def get_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default

def get_float(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default

def get_bool(value, default=False):
    # Accepts 'on', 'true', '1', True as True
    if isinstance(value, bool):
        return value
    if value in ['on', 'true', 'True', '1', 1]:
        return True
    return default

def get_date(value, default=None):
    if not value:
        return default or datetime.date.today()
    if isinstance(value, datetime.date):
        return value
    try:
        return datetime.date.fromisoformat(value)
    except Exception:
        return default or datetime.date.today()

# Create your views here.
@login_required
def configuration_view(request):
    # Since @login_required ensures user is authenticated, redirect to contact form
    return redirect('contact')

@login_required
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
        if request.user.is_authenticated:
            try:
                instance = ConfigurationInfo.objects.get(user=request.user)
                form = ContactForm(instance=instance)
            except ConfigurationInfo.DoesNotExist:
                form = ContactForm()
        else:
            form = ContactForm()
    return render(request, 'configuration/contact.html', {'form': form})

@login_required
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
        if request.user.is_authenticated:
            try:
                instance = ConfigurationInfo.objects.get(user=request.user)
                form = SiteIdentificationForm(instance=instance)
            except ConfigurationInfo.DoesNotExist:
                form = SiteIdentificationForm()
        else:
            form = SiteIdentificationForm()
    return render(request, 'configuration/site_identification.html', {'form': form})

@login_required
def site_local_network_info_view(request):
    if request.method == 'POST':
        form = SiteLocalNetworkInfoForm(request.POST)
        if form.is_valid():
             # Get cleaned data from the form
            site_local_network_info_data = form.cleaned_data

            if 'most_recent_survey_date' in site_local_network_info_data:
                site_local_network_info_data['most_recent_survey_date'] = site_local_network_info_data['most_recent_survey_date'].isoformat()

            # Save the cleaned and processed data in the session
            request.session['site_local_network_info_data'] = site_local_network_info_data
            return redirect('site_descriptive_info')
    else:
        if request.user.is_authenticated:
            try:
                instance = ConfigurationInfo.objects.get(user=request.user)
                form = SiteLocalNetworkInfoForm(instance=instance)
            except ConfigurationInfo.DoesNotExist:
                form = SiteLocalNetworkInfoForm()
        else:
            form = SiteLocalNetworkInfoForm()
    return render(request, 'configuration/site_local_network_info.html', {'form': form})

@login_required
def site_descriptive_info_view(request):
    if request.method == 'POST':
        form = SiteDescriptiveInfoForm(request.POST)
        if form.is_valid():
            request.session['site_descriptive_info_data'] = form.cleaned_data
            # Continue with the next tab or the summary page
            return redirect('antenna_details')
    else:
        if request.user.is_authenticated:
            try:
                instance = ConfigurationInfo.objects.get(user=request.user)
                form = SiteDescriptiveInfoForm(instance=instance)
            except ConfigurationInfo.DoesNotExist:
                form = SiteDescriptiveInfoForm()
        else:
            form = SiteDescriptiveInfoForm()
    return render(request, 'configuration/site_descriptive_info.html', {'form': form})

@login_required
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
        if request.user.is_authenticated:
            try:
                instance = ConfigurationInfo.objects.get(user=request.user)
                form = AntennaDetailsForm(instance=instance)
            except ConfigurationInfo.DoesNotExist:
                form = AntennaDetailsForm()
        else:
            form = AntennaDetailsForm()
    return render(request, 'configuration/antenna_details.html', {'form': form})


@login_required
def receiver_view(request):
    if request.method == 'POST':
        form = ReceiverForm(request.POST)
        if form.is_valid():
            request.session['receiver_data'] = form.cleaned_data
            # Continue with the next tab or the summary page
            return redirect('cables_receiver_and_backend')
    else:
        if request.user.is_authenticated:
            try:
                instance = ConfigurationInfo.objects.get(user=request.user)
                form = ReceiverForm(instance=instance)
            except ConfigurationInfo.DoesNotExist:
                form = ReceiverForm()
        else:
            form = ReceiverForm()
    return render(request, 'configuration/receiver.html', {'form': form})

@login_required
def cables_receiver_and_backend_view(request):
    if request.method == 'POST':
        form = CablesReceiverAndBackendForm(request.POST)
        if form.is_valid():
            request.session['cables_receiver_and_backend_data'] = form.cleaned_data
            # Continue with the next tab or the summary page
            return redirect('data_acquisition_system')
    else:
        if request.user.is_authenticated:
            try:
                instance = ConfigurationInfo.objects.get(user=request.user)
                form = CablesReceiverAndBackendForm(instance=instance)
            except ConfigurationInfo.DoesNotExist:
                form = CablesReceiverAndBackendForm()
        else:
            form = CablesReceiverAndBackendForm()
    return render(request, 'configuration/cables_receiver_and_backend.html', {'form': form})

@login_required
def data_acquisition_system_view(request):
    if request.method == 'POST':
        form = DataAcquisitionSystemForm(request.POST)
        if form.is_valid():
            request.session['data_acquisition_system'] = form.cleaned_data
            # Continue with the next tab or the summary page
            return redirect('meteorological_instrumentation')
    else:
        if request.user.is_authenticated:
            try:
                instance = ConfigurationInfo.objects.get(user=request.user)
                form = DataAcquisitionSystemForm(instance=instance)
            except ConfigurationInfo.DoesNotExist:
                form = DataAcquisitionSystemForm()
        else:
            form = DataAcquisitionSystemForm()
    return render(request, 'configuration/data_acquisition_system.html', {'form': form})

@login_required
def meteorological_instrumentation_view(request):
    if request.method == 'POST':
        form = MeteorologicalInstrumentationForm(request.POST)
        if form.is_valid():
            request.session['meteorological_instrumentation'] = form.cleaned_data
            # Continue with the next tab or the summary page
            return redirect('time_and_frequency_standards')
    else:
        if request.user.is_authenticated:
            try:
                instance = ConfigurationInfo.objects.get(user=request.user)
                form = MeteorologicalInstrumentationForm(instance=instance)
            except ConfigurationInfo.DoesNotExist:
                form = MeteorologicalInstrumentationForm()
        else:
            form = MeteorologicalInstrumentationForm()
    return render(request, 'configuration/meteorological_instrumentation.html', {'form': form})

@login_required
def time_and_frequency_standards_view(request):
    if request.method == 'POST':
        form = TimeAndFrequencyStandardsForm(request.POST)
        if form.is_valid():
            request.session['time_and_frequency_standards'] = form.cleaned_data
            # Continue with the next tab or the summary page
            return redirect('auxilliary_equipment')
    else:
        if request.user.is_authenticated:
            try:
                instance = ConfigurationInfo.objects.get(user=request.user)
                form = TimeAndFrequencyStandardsForm(instance=instance)
            except ConfigurationInfo.DoesNotExist:
                form = TimeAndFrequencyStandardsForm()
        else:
            form = TimeAndFrequencyStandardsForm()
    return render(request, 'configuration/time_and_frequency_standards.html', {'form': form})

@login_required
def auxilliary_equipment_view(request):
    if request.method == 'POST':
        form = AuxilliaryEquipmentForm(request.POST)
        if form.is_valid():
            request.session['auxilliary_equipment'] = form.cleaned_data
            # Continue with the next tab or the summary page
            return redirect('co_locations')
    else:
        if request.user.is_authenticated:
            try:
                instance = ConfigurationInfo.objects.get(user=request.user)
                form = AuxilliaryEquipmentForm(instance=instance)
            except ConfigurationInfo.DoesNotExist:
                form = AuxilliaryEquipmentForm()
        else:
            form = AuxilliaryEquipmentForm()
    return render(request, 'configuration/auxilliary_equipment.html', {'form': form})

@login_required
def co_locations_view(request):
    if request.method == 'POST':
        form = CoLocationsForm(request.POST)
        if form.is_valid():
            request.session['co_locations'] = form.cleaned_data
            # Continue with the next tab or the summary page
            return redirect('field_system_computer')
    else:
        if request.user.is_authenticated:
            try:
                instance = ConfigurationInfo.objects.get(user=request.user)
                form = CoLocationsForm(instance=instance)
            except ConfigurationInfo.DoesNotExist:
                form = CoLocationsForm()
        else:
            form = CoLocationsForm()
    return render(request, 'configuration/co_locations.html', {'form': form})

@login_required
def field_system_computer_view(request):
    if request.method == 'POST':
        form = FieldSystemComputerForm(request.POST)
        if form.is_valid():
            request.session['field_system_computer'] = form.cleaned_data
            # Continue with the next tab or the summary page
            return redirect('on_site_contact')
    else:
        if request.user.is_authenticated:
            try:
                instance = ConfigurationInfo.objects.get(user=request.user)
                form = FieldSystemComputerForm(instance=instance)
            except ConfigurationInfo.DoesNotExist:
                form = FieldSystemComputerForm()
        else:
            form = FieldSystemComputerForm()
    return render(request, 'configuration/field_system_computer.html', {'form': form})

@login_required
def on_site_contact_view(request):
    if request.method == 'POST':
        form = OnSiteContactForm(request.POST)
        if form.is_valid():
            request.session['on_site_contact'] = form.cleaned_data
            # Continue with the next tab or the summary page
            return redirect('responsible_agency')
    else:
        if request.user.is_authenticated:
            try:
                instance = ConfigurationInfo.objects.get(user=request.user)
                form = OnSiteContactForm(instance=instance)
            except ConfigurationInfo.DoesNotExist:
                form = OnSiteContactForm()
        else:
            form = OnSiteContactForm()
    return render(request, 'configuration/on_site_contact.html', {'form': form})

@login_required
def responsible_agency_view(request):
    if request.method == 'POST':
        form = ResponsibleAgencyForm(request.POST)
        if form.is_valid():
            request.session['responsible_agency'] = form.cleaned_data
            # Continue with the next tab or the summary page
            return redirect('configuration_summary')
    else:
        if request.user.is_authenticated:
            try:
                instance = ConfigurationInfo.objects.get(user=request.user)
                form = ResponsibleAgencyForm(instance=instance)
            except ConfigurationInfo.DoesNotExist:
                form = ResponsibleAgencyForm()
        else:
            form = ResponsibleAgencyForm()
    return render(request, 'configuration/responsible_agency.html', {'form': form})

@login_required
def configuration_summary_view(request):
    # Gather all the data from the session
    contact_data = request.session.get('contact_data', {})
    site_identification_data = request.session.get('site_identification_data', {})
    site_local_network_info_data = request.session.get('site_local_network_info_data', {})
    site_descriptive_info_data = request.session.get('site_descriptive_info_data', {})
    antenna_details_data = request.session.get('antenna_details_data', {})
    receiver_data = request.session.get('receiver_data', {})
    cables_receiver_and_backend_data = request.session.get('cables_receiver_and_backend_data', {})
    data_acquisition_system_data = request.session.get('data_acquisition_system', {})
    meteorological_instrumentation_data = request.session.get('meteorological_instrumentation', {})
    time_and_frequency_standards_data = request.session.get('time_and_frequency_standards', {})
    auxilliary_equipment_data = request.session.get('auxilliary_equipment', {})
    co_locations_data = request.session.get('co_locations', {})
    field_system_computer_data = request.session.get('field_system_computer', {})
    on_site_contact_data = request.session.get('on_site_contact', {})
    responsible_agency_data = request.session.get('responsible_agency', {})

    # Ensure update_date is set and is a date object
    update_date = contact_data.get('update_date')
    if not update_date:
        update_date = datetime.date.today()
        contact_data['update_date'] = update_date
    elif isinstance(update_date, str):
        try:
            update_date = datetime.date.fromisoformat(update_date)
            contact_data['update_date'] = update_date
        except Exception:
            update_date = datetime.date.today()
            contact_data['update_date'] = update_date

    if request.method == 'POST' and request.POST.get("form_type") == "submit_form":
        # Validate that all required session data is present
        missing_fields = []
        
        # Check contact data
        if not contact_data.get('prepared_by_full_name'):
            missing_fields.append('Prepared by Full Name')
        if not contact_data.get('email'):
            missing_fields.append('Email')
        if not contact_data.get('report_type'):
            missing_fields.append('Report Type')
            
        # Check site identification data
        if not site_identification_data.get('site_name'):
            missing_fields.append('Site Name')
        if not site_identification_data.get('site_8_letter_code'):
            missing_fields.append('Site 8 Letter Code')
        if not site_identification_data.get('site_2_letter_code'):
            missing_fields.append('Site 2 Letter Code')
        if not site_identification_data.get('IERS_domes_number'):
            missing_fields.append('IERS DOMES Number')
        if not site_identification_data.get('IGS_station_code'):
            missing_fields.append('IGS Station Code')
        if not site_identification_data.get('ILRS_station_name'):
            missing_fields.append('ILRS Station Name')
            
        # If there are missing required fields, show error and redirect back
        if missing_fields:
            messages.error(request, f'Please complete the following required fields: {", ".join(missing_fields)}. Please go back and fill them in.')
            return redirect('configuration_summary')
        
        # Ensure session data is present
        if not contact_data:
            contact_data = {
                'prepared_by_full_name': request.POST.get('prepared_by_full_name'),
                'email': request.POST.get('email'),
                'update_date': update_date,
                'report_type': request.POST.get('report_type')
            }

        if not site_identification_data:
            site_identification_data = {
                'site_name': request.POST.get('site_name') or '',
                'site_8_letter_code': request.POST.get('site_8_letter_code') or '',
                'site_2_letter_code': request.POST.get('site_2_letter_code') or '',
                'IERS_domes_number': request.POST.get('IERS_domes_number') or '',
                'CDP_occupation_code': get_int(request.POST.get('CDP_occupation_code'), 0),
                'CDP_monument_number': get_int(request.POST.get('CDP_monument_number'), 0),
                'IGS_station_code': request.POST.get('IGS_station_code') or '',
                'ILRS_station_name': request.POST.get('ILRS_station_name') or '',
                'survey_into_national_network': get_bool(request.POST.get('survey_into_national_network'), False),
                'start_date_of_operation': get_date(request.POST.get('start_date_of_operation')),
                'additional_info': request.POST.get('additional_info') or '',
            }

        if not site_local_network_info_data:
            site_local_network_info_data = {
                'type_of_marker': request.POST.get('type_of_marker') or '',
                'frequency_of_surveying': request.POST.get('frequency_of_surveying') or '',
                'surveying_method': request.POST.get('surveying_method') or '',
                'survey_instruments_used': request.POST.get('survey_instruments_used') or '',
                'accuracy': request.POST.get('accuracy') or '',
                'survey_performed_by': request.POST.get('survey_performed_by') or '',
                'survay_documentation': request.POST.get('survay_documentation') or '',
                'responsible_person': request.POST.get('responsible_person') or '',
                'most_recent_survey_date': get_date(request.POST.get('most_recent_survey_date')),
                'results_provided_to_IERS': get_bool(request.POST.get('results_provided_to_IERS'), False),
                'results_provided_to_CDDIS': get_bool(request.POST.get('results_provided_to_CDDIS'), False),
                'number_of_reference_markers': request.POST.get('number_of_reference_markers') or '',
                'additional_info': request.POST.get('additional_info') or '',
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
                'antenna_type': request.POST.get('antenna_type') or '',
                'diameter_m': get_float(request.POST.get('diameter_m'), 0.0),
                'axis_type': request.POST.get('axis_type') or '',
                'axis_offset_m': get_float(request.POST.get('axis_offset_m'), 0.0),
                'slew_rate_first_axis_deg_min': get_float(request.POST.get('slew_rate_first_axis_deg_min'), 0.0),
                'slew_rate_second_axis_deg_min': get_float(request.POST.get('slew_rate_second_axis_deg_min'), 0.0),
                'min_limit_first_axis_deg': get_float(request.POST.get('min_limit_first_axis_deg'), 0.0),
                'max_limit_first_axis_deg': get_float(request.POST.get('max_limit_first_axis_deg'), 0.0),
                'min_limit_second_axis_deg': get_float(request.POST.get('min_limit_second_axis_deg'), 0.0),
                'max_limit_second_axis_deg': get_float(request.POST.get('max_limit_second_axis_deg'), 0.0),
                'horizon_mask_data_azimuth_deg_coressponding_elevationmask_deg': request.POST.get('horizon_mask_data_azimuth_deg_coressponding_elevationmask_deg') or '',
                'start_date_of_occupation': get_date(request.POST.get('start_date_of_occupation')),
                'end_date_of_occupation': get_date(request.POST.get('end_date_of_occupation')),
                'additional_info': request.POST.get('additional_info') or '',
            }

        if not receiver_data:
            receiver_data = {
                'feed_location': request.POST.get('feed_location') or '',
                'feed_type': request.POST.get('feed_type') or '',
                'x_first_stage_amplifier': request.POST.get('x_first_stage_amplifier') or '',
                's_first_stage_amplifier': request.POST.get('s_first_stage_amplifier') or '',
                'x_bandwidth_mhz': get_float(request.POST.get('x_bandwidth_mhz'), 0.0),
                's_bandwidth_mhz': get_float(request.POST.get('s_bandwidth_mhz'), 0.0),
                'x_tsys_at_zenith_k': get_float(request.POST.get('x_tsys_at_zenith_k'), 0.0),
                's_tsys_at_zenith_k': get_float(request.POST.get('s_tsys_at_zenith_k'), 0.0),
                'x_sefd_jy': get_float(request.POST.get('x_sefd_jy'), 0.0),
                's_sefd_jy': get_float(request.POST.get('s_sefd_jy'), 0.0),
                'x_aperture_efficiency': request.POST.get('x_aperture_efficiency') or '',
                's_aperture_efficiency': request.POST.get('s_aperture_efficiency') or '',
                'x_lo_frequencies_mhz': get_float(request.POST.get('x_lo_frequencies_mhz'), 0.0),
                's_lo_frequencies_mhz': get_float(request.POST.get('s_lo_frequencies_mhz'), 0.0),
                'phase_calibrator_type': request.POST.get('phase_calibrator_type') or '',
                'additional_info': request.POST.get('additional_info') or '',
            }

        if not cables_receiver_and_backend_data:
            cables_receiver_and_backend_data = {
                'length_of_cable_run_m': get_float(request.POST.get('length_of_cable_run_m'), 0.0),
                'x_band_cable_type': request.POST.get('x_band_cable_type') or '',
                'x_band_freq_bandpass_mhz': request.POST.get('x_band_freq_bandpass_mhz') or '',
                's_band_cable_type': request.POST.get('s_band_cable_type') or '',
                's_band_freq_bandpass_mhz': request.POST.get('s_band_freq_bandpass_mhz') or '',
                'lo_ref_signal_cable_type': request.POST.get('lo_ref_signal_cable_type') or '',
                'lo_ref_signal_freq_mhz': request.POST.get('lo_ref_signal_freq_mhz') or '',
                'phase_cal_ref_signal_cable_type': request.POST.get('phase_cal_ref_signal_cable_type') or '',
                'phase_cal_ref_signal_freq_mhz': get_float(request.POST.get('phase_cal_ref_signal_freq_mhz'), 0.0),
                'cable_measure_system_type': request.POST.get('cable_measure_system_type') or '',
                'additional_info': request.POST.get('additional_info') or '',
            }
            
        if not data_acquisition_system_data:
            data_acquisition_system_data = {
                'type_of_video_converter': request.POST.get('type_of_video_converter') or '',
                'number_of_mixers': get_int(request.POST.get('number_of_mixers'), 0),
                'sidebands_available': request.POST.get('sidebands_available') or '',
                'number_of_mixers_with_2mhz_filter': get_int(request.POST.get('number_of_mixers_with_2mhz_filter'), 0),
                'number_of_mixers_with_4mhz_filter': get_int(request.POST.get('number_of_mixers_with_4mhz_filter'), 0),
                'number_of_mixers_with_8mhz_filter': get_int(request.POST.get('number_of_mixers_with_8mhz_filter'), 0),
                'number_of_mixers_with_16mhz_filter': get_int(request.POST.get('number_of_mixers_with_16mhz_filter'), 0),
                'number_of_mixers_with_32mhz_filter': get_int(request.POST.get('number_of_mixers_with_32mhz_filter'), 0),
                'additional_video_converter': request.POST.get('additional_video_converter') or '',
                'formatter_type': request.POST.get('formatter_type') or '',
                'serial_number_or_rack_id': request.POST.get('serial_number_or_rack_id') or '',
                'additional_formattter': request.POST.get('additional_formattter') or '',
                'decode_type': request.POST.get('decode_type') or '',
                'additional_decoder': request.POST.get('additional_decoder') or '',
                'IF_distributor_type': request.POST.get('IF_distributor_type') or '',
                'additional_IF_distributor': request.POST.get('additional_IF_distributor') or '',
                'X_down_converter_freq': get_float(request.POST.get('X_down_converter_freq'), 0.0),
                'S_up_down_converter_freq': request.POST.get('S_up_down_converter_freq') or '',
                'additional_converter': request.POST.get('additional_converter') or '',
                'other_rack_equipment': request.POST.get('other_rack_equipment') or '',
                'additional_rack_equipment': request.POST.get('additional_rack_equipment') or '',
                'recorder_type': request.POST.get('recorder_type') or '',
                'number_of_recorders': get_int(request.POST.get('number_of_recorders'), 0),
                'tape_type': request.POST.get('tape_type') or '',
                'additional_info': request.POST.get('additional_info') or '',
                'additional_recorder_type': request.POST.get('additional_recorder_type') or '',
                'configuration_types_supported': request.POST.get('configuration_types_supported') or '',
                'additional_configuration_info': request.POST.get('additional_configuration_info') or '',
            }  
        
        if not  meteorological_instrumentation_data:
            meteorological_instrumentation_data = {
                'humidity_sensor_manufacturer': request.POST.get('humidity_sensor_manufacturer') or '',
                'humidity_sensor_model': request.POST.get('humidity_sensor_model') or '',
                'humidity_sensor_accuracy': request.POST.get('humidity_sensor_accuracy') or '',
                'humidity_sensor_effective_dates': request.POST.get('humidity_sensor_effective_dates') or '',
                'addtional_humidity_sensor_info': request.POST.get('addtional_humidity_sensor_info') or '',
                'pressure_sensor_manufacturer': request.POST.get('pressure_sensor_manufacturer') or '',
                'pressure_sensor_model': request.POST.get('pressure_sensor_model') or '',
                'pressure_sensor_accuracy': request.POST.get('pressure_sensor_accuracy') or '',
                'pressure_sensor_effective_dates': request.POST.get('pressure_sensor_effective_dates') or '',
                'pressure_sensor_height_relative_to_VLBI_in_meters': get_float(request.POST.get('pressure_sensor_height_relative_to_VLBI_in_meters'), 0.0),
                'pressure_sensor_additional_info': request.POST.get('pressure_sensor_additional_info') or '',
                'temperature_sensor_manufacturer': request.POST.get('temperature_sensor_manufacturer') or '',
                'temperature_sensor_model': request.POST.get('temperature_sensor_model') or '',
                'temperature_sensor_accuracy': request.POST.get('temperature_sensor_accuracy') or '',
                'temperature_sensor_effective_dates': request.POST.get('temperature_sensor_effective_dates') or '',
                'temperature_sensor_additional_info': request.POST.get('temperature_sensor_additional_info') or '',
            }
        
        if not time_and_frequency_standards_data:
            time_and_frequency_standards_data = {
                'standard_type': request.POST.get('standard_type') or '',
                'installed_dates_duration': request.POST.get('installed_dates_duration') or '',
                'manufacturer': request.POST.get('manufacturer') or '',
                'model_number_or_ID': request.POST.get('model_number_or_ID') or '',
                'additional_info': request.POST.get('additional_info') or '',
            }
            
        if not auxilliary_equipment_data:
            auxilliary_equipment_data = {
                'first_equipment_type': request.POST.get('first_equipment_type') or '',
                'first_installed_dates': request.POST.get('first_installed_dates') or '',
                'fisrt_manufacturer': request.POST.get('fisrt_manufacturer') or '',
                'fisrt_model_number_or_ID': request.POST.get('fisrt_model_number_or_ID') or '',
                'first_additional_info': request.POST.get('first_additional_info') or '',
                'second_equipment_type': request.POST.get('second_equipment_type') or '',
                'second_installed_dates': request.POST.get('second_installed_dates') or '',
                'second_manufacturer': request.POST.get('second_manufacturer') or '',
                'second_model_number_or_ID': request.POST.get('second_model_number_or_ID') or '',
                'second_additional_info': request.POST.get('second_additional_info') or '',
            }
        
        if not co_locations_data:
            co_locations_data = {
                'instrument_type': request.POST.get('instrument_type') or '',
                'instrument_name': request.POST.get('instrument_name') or '',
                'status': request.POST.get('status') or '',
                'effective_dates': request.POST.get('effective_dates') or '',
                'included_in_local_survey': request.POST.get('included_in_local_survey') or '',
                'additional_info': request.POST.get('additional_info') or '',
            }
        if not field_system_computer_data:
            field_system_computer_data = {
                'computer_system_vendor': request.POST.get('computer_system_vendor') or '',
                'computer_CPU': request.POST.get('computer_CPU') or '',
                'computer_CPU_speed_in_MHz': get_float(request.POST.get('computer_CPU_speed_in_MHz'), 0.0),
                'computer_memory_in_Mbytes': get_float(request.POST.get('computer_memory_in_Mbytes'), 0.0),
                'computer_disk_in_Gbytes': get_float(request.POST.get('computer_disk_in_Gbytes'), 0.0),
                'computer_Linux_release': request.POST.get('computer_Linux_release') or '',
                'computer_internet_connection': request.POST.get('computer_internet_connection') or '',
                'antenna_interface_type': request.POST.get('antenna_interface_type') or '',
                'spare_FS_computer': get_bool(request.POST.get('spare_FS_computer'), False),
                'known_RFI_sources': request.POST.get('known_RFI_sources') or '',
            }
        if not on_site_contact_data:
            on_site_contact_data = {
                'agency': request.POST.get('agency') or '',
                'shipping_address': request.POST.get('shipping_address') or '',
                'postal_address': request.POST.get('postal_address') or '',
                'URL_of_site_web_page': request.POST.get('URL_of_site_web_page') or '',
                'on_site_friend_of_VLBI_name': request.POST.get('on_site_friend_of_VLBI_name') or '',
                'primary_telephone_of_on_site_friend_of_VLBI': request.POST.get('primary_telephone_of_on_site_friend_of_VLBI') or '',
                'alternative_telephone_of_on_site_friend_of_VLBI': request.POST.get('alternative_telephone_of_on_site_friend_of_VLBI') or '',
                'fax_of_on_site_friend_of_VLBI': request.POST.get('fax_of_on_site_friend_of_VLBI') or '',
                'email_of_on_site_friend_of_VLBI': request.POST.get('email_of_on_site_friend_of_VLBI') or '',
                'primary_telephone_of_VLBI_operations_room': request.POST.get('primary_telephone_of_VLBI_operations_room') or '',
                'alternative_telephone_of_VLBI_operations_room': request.POST.get('alternative_telephone_of_VLBI_operations_room') or '',
                'fax_of_VLBI_operations_room': request.POST.get('fax_of_VLBI_operations_room') or '',
                'email_of_VLBI_operations_room': request.POST.get('email_of_VLBI_operations_room') or '',
                'name_of_other_on_site_contact': request.POST.get('name_of_other_on_site_contact') or '',
                'primary_telephone_of_other_on_site_contact': request.POST.get('primary_telephone_of_other_on_site_contact') or '',
                'alternative_telephone_of_other_on_site_contact': request.POST.get('alternative_telephone_of_other_on_site_contact') or '',
                'fax_of_other_on_site_contact': request.POST.get('fax_of_other_on_site_contact') or '',
                'email_of_other_on_site_contact': request.POST.get('email_of_other_on_site_contact') or '',
                'additional_info': request.POST.get('additional_info') or '',
            }

        if not responsible_agency_data:
            responsible_agency_data = {
                'responsible_agency': request.POST.get('responsible_agency') or '',
                'shipping_address': request.POST.get('shipping_address') or '',
                'postal_address': request.POST.get('postal_address') or '',
                'URL_of_agency_web_page': request.POST.get('URL_of_agency_web_page') or '',
                'primary_administrative_agency_contact_person': request.POST.get('primary_administrative_agency_contact_person') or '',
                'primary_telephone_of_contact_person': request.POST.get('primary_telephone_of_contact_person') or '',
                'alternative_telephone_of_contact_person': request.POST.get('alternative_telephone_of_contact_person') or '',
                'fax_of_contact_person': request.POST.get('fax_of_contact_person') or '',
                'email_of_contact_person': request.POST.get('email_of_contact_person') or '',
                'alternative_agency_contact': request.POST.get('alternative_agency_contact') or '',
                'alternative_agency_shipping_address': request.POST.get('alternative_agency_shipping_address') or '',
                'alternative_agency_postal_address': request.POST.get('alternative_agency_postal_address') or '',
                'alternative_agency_URL_of_agency_web_page': request.POST.get('alternative_agency_URL_of_agency_web_page') or '',
                'primary_administrative_alternative_agency_contact_person': request.POST.get('primary_administrative_alternative_agency_contact_person') or '',
                'primary_telephone_of_alternative_agency_contact_person': request.POST.get('primary_telephone_of_alternative_agency_contact_person') or '',
                'alternative_contact_person': request.POST.get('alternative_contact_person') or '',
                'alternative_telephone': request.POST.get('alternative_telephone') or '',
                'fax_of_alternative_contact_person': request.POST.get('fax_of_alternative_contact_person') or '',
                'email_of_alternative_contact_person': request.POST.get('email_of_alternative_contact_person') or '',
                'additional_info': request.POST.get('additional_info') or '',
                'more_info': request.POST.get('more_info') or '',
            }

        if request.user.is_authenticated:
            configuration_info, created = ConfigurationInfo.objects.get_or_create(user=request.user)
            configuration_info.prepared_by_full_name = contact_data.get('prepared_by_full_name', '')
            configuration_info.email = contact_data.get('email', '')
            configuration_info.update_date = update_date
            configuration_info.report_type = contact_data.get('report_type', '')

            configuration_info.site_name = site_identification_data.get('site_name', '')
            configuration_info.site_8_letter_code = site_identification_data.get('site_8_letter_code', '')
            configuration_info.site_2_letter_code = site_identification_data.get('site_2_letter_code', '')
            configuration_info.IERS_domes_number = site_identification_data.get('IERS_domes_number', '')
            configuration_info.CDP_occupation_code = site_identification_data.get('CDP_occupation_code', 0)
            configuration_info.CDP_monument_number = site_identification_data.get('CDP_monument_number', 0)
            configuration_info.IGS_station_code = site_identification_data.get('IGS_station_code', '')
            configuration_info.ILRS_station_name = site_identification_data.get('ILRS_station_name', '')
            configuration_info.survey_into_national_network = site_identification_data.get('survey_into_national_network', False)
            configuration_info.start_date_of_operation = site_identification_data.get('start_date_of_operation', datetime.date.today())
            configuration_info.additional_info = site_identification_data.get('additional_info', '')
            
            configuration_info.type_of_marker = site_local_network_info_data.get('type_of_marker')
            configuration_info.frequency_of_surveying = site_local_network_info_data.get('frequency_of_surveying')
            configuration_info.surveying_method = site_local_network_info_data.get('surveying_method')
            configuration_info.survey_instruments_used = site_local_network_info_data.get('survey_instruments_used')
            configuration_info.accuracy = site_local_network_info_data.get('accuracy')
            configuration_info.survey_performed_by = site_local_network_info_data.get('survey_performed_by')
            configuration_info.survay_documentation = site_local_network_info_data.get('survay_documentation')
            configuration_info.responsible_person = site_local_network_info_data.get('responsible_person')
            configuration_info.most_recent_survey_date = site_local_network_info_data.get('most_recent_survey_date')
            configuration_info.results_provided_to_IERS = site_local_network_info_data.get('results_provided_to_IERS')
            configuration_info.results_provided_to_CDDIS = site_local_network_info_data.get('results_provided_to_CDDIS')
            configuration_info.number_of_reference_markers = site_local_network_info_data.get('number_of_reference_markers')
            configuration_info.additional_info = site_local_network_info_data.get('additional_info')

            configuration_info.site_map = site_descriptive_info_data.get('site_map')
            configuration_info.site_map_url = site_descriptive_info_data.get('site_map_url')
            configuration_info.site_diagram = site_descriptive_info_data.get('site_diagram')
            configuration_info.site_diagram_url = site_descriptive_info_data.get('site_diagram_url')
            configuration_info.horizon_mask = site_descriptive_info_data.get('horizon_mask')
            configuration_info.horizon_mask_url = site_descriptive_info_data.get('horizon_mask_url')
            configuration_info.monument_description = site_descriptive_info_data.get('monument_description')
            configuration_info.monument_description_url = site_descriptive_info_data.get('monument_description_url')
            configuration_info.site_photographs = site_descriptive_info_data.get('site_photographs')
            configuration_info.site_photographs_url = site_descriptive_info_data.get('site_photographs_url')

            configuration_info.antenna_type = antenna_details_data.get('antenna_type')
            configuration_info.diameter_m = antenna_details_data.get('diameter_m')
            configuration_info.axis_type = antenna_details_data.get('axis_type')
            configuration_info.axis_offset_m = antenna_details_data.get('axis_offset_m')
            configuration_info.slew_rate_first_axis_deg_min = antenna_details_data.get('slew_rate_first_axis_deg_min')
            configuration_info.slew_rate_second_axis_deg_min = antenna_details_data.get('slew_rate_second_axis_deg_min')
            configuration_info.min_limit_first_axis_deg = antenna_details_data.get('min_limit_first_axis_deg')
            configuration_info.max_limit_first_axis_deg = antenna_details_data.get('max_limit_first_axis_deg')
            configuration_info.min_limit_second_axis_deg = antenna_details_data.get('min_limit_second_axis_deg')
            configuration_info.max_limit_second_axis_deg = antenna_details_data.get('max_limit_second_axis_deg')
            configuration_info.horizon_mask_data_azimuth_deg_coressponding_elevationmask_deg = antenna_details_data.get('horizon_mask_data_azimuth_deg_coressponding_elevationmask_deg')
            configuration_info.start_date_of_occupation = antenna_details_data.get('start_date_of_occupation')
            configuration_info.end_date_of_occupation = antenna_details_data.get('end_date_of_occupation')
            configuration_info.additional_info = antenna_details_data.get('additional_info')

            configuration_info.feed_location = receiver_data.get('feed_location')
            configuration_info.feed_type = receiver_data.get('feed_type')
            configuration_info.x_first_stage_amplifier = receiver_data.get('x_first_stage_amplifier')
            configuration_info.s_first_stage_amplifier = receiver_data.get('s_first_stage_amplifier')
            configuration_info.x_bandwidth_mhz = receiver_data.get('x_bandwidth_mhz')
            configuration_info.s_bandwidth_mhz = receiver_data.get('s_bandwidth_mhz')
            configuration_info.x_tsys_at_zenith_k = receiver_data.get('x_tsys_at_zenith_k')
            configuration_info.s_tsys_at_zenith_k = receiver_data.get('s_tsys_at_zenith_k')
            configuration_info.x_sefd_jy = receiver_data.get('x_sefd_jy')
            configuration_info.s_sefd_jy = receiver_data.get('s_sefd_jy')
            configuration_info.x_aperture_efficiency = receiver_data.get('x_aperture_efficiency')
            configuration_info.s_aperture_efficiency = receiver_data.get('s_first_stage_amplifier')
            configuration_info.x_lo_frequencies_mhz = receiver_data.get('x_lo_frequencies_mhz')
            configuration_info.s_lo_frequencies_mhz = receiver_data.get('s_lo_frequencies_mhz')
            configuration_info.phase_calibrator_type = receiver_data.get('phase_calibrator_type')
            configuration_info.additional_info = receiver_data.get('additional_info')

            configuration_info.length_of_cable_run_m = cables_receiver_and_backend_data.get('length_of_cable_run_m')
            configuration_info.x_band_cable_type = cables_receiver_and_backend_data.get('x_band_cable_type')
            configuration_info.x_band_freq_bandpass_mhz = cables_receiver_and_backend_data.get('x_band_freq_bandpass_mhz')
            configuration_info.s_band_cable_type = cables_receiver_and_backend_data.get('s_band_cable_type')
            configuration_info.s_band_freq_bandpass_mhz = cables_receiver_and_backend_data.get('s_band_freq_bandpass_mhz')
            configuration_info.lo_ref_signal_cable_type = cables_receiver_and_backend_data.get('lo_ref_signal_cable_type')
            configuration_info.lo_ref_signal_freq_mhz = cables_receiver_and_backend_data.get('lo_ref_signal_freq_mhz')
            configuration_info.phase_cal_ref_signal_cable_type = cables_receiver_and_backend_data.get('phase_cal_ref_signal_cable_type')
            configuration_info.phase_cal_ref_signal_freq_mhz = cables_receiver_and_backend_data.get('phase_cal_ref_signal_freq_mhz')
            configuration_info.cable_measure_system_type = cables_receiver_and_backend_data.get('cable_measure_system_type')
            configuration_info.additional_info = cables_receiver_and_backend_data.get('additional_info')
            
            configuration_info.type_of_video_converter = data_acquisition_system_data.get('type_of_video_converter')
            configuration_info.number_of_mixers = data_acquisition_system_data.get('number_of_mixers')
            configuration_info.sidebands_available = data_acquisition_system_data.get('sidebands_available')
            configuration_info.number_of_mixers_with_2mhz_filter = data_acquisition_system_data.get('number_of_mixers_with_2mhz_filter')
            configuration_info.number_of_mixers_with_4mhz_filter = data_acquisition_system_data.get('number_of_mixers_with_4mhz_filter')
            configuration_info.number_of_mixers_with_8mhz_filter = data_acquisition_system_data.get('number_of_mixers_with_8mhz_filter')
            configuration_info.number_of_mixers_with_16mhz_filter = data_acquisition_system_data.get('number_of_mixers_with_16mhz_filter')
            configuration_info.number_of_mixers_with_32mhz_filter = data_acquisition_system_data.get('number_of_mixers_with_32mhz_filter')
            configuration_info.additional_video_converter = data_acquisition_system_data.get('additional_video_converter')
            configuration_info.formatter_type = data_acquisition_system_data.get('formatter_type')
            configuration_info.serial_number_or_rack_id = data_acquisition_system_data.get('serial_number_or_rack_id')
            configuration_info.additional_formattter = data_acquisition_system_data.get('additional_formattter')
            configuration_info.decode_type = data_acquisition_system_data.get('decode_type')
            configuration_info.additional_decoder = data_acquisition_system_data.get('additional_decoder')
            configuration_info.IF_distributor_type = data_acquisition_system_data.get('IF_distributor_type')
            configuration_info.additional_IF_distributor = data_acquisition_system_data.get('additional_IF_distributor')
            configuration_info.X_down_converter_freq = data_acquisition_system_data.get('X_down_converter_freq')
            configuration_info.S_up_down_converter_freq = data_acquisition_system_data.get('S_up_down_converter_freq')
            configuration_info.additional_converter = data_acquisition_system_data.get('additional_converter')
            configuration_info.other_rack_equipment = data_acquisition_system_data.get('other_rack_equipment')
            configuration_info.additional_rack_equipment = data_acquisition_system_data.get('additional_rack_equipment')
            configuration_info.recorder_type = data_acquisition_system_data.get('recorder_type')
            configuration_info.number_of_recorders = data_acquisition_system_data.get('number_of_recorders')
            configuration_info.tape_type = data_acquisition_system_data.get('tape_type')
            configuration_info.additional_info = data_acquisition_system_data.get('additional_info')
            configuration_info.additional_recorder_type = data_acquisition_system_data.get('additional_recorder_type')
            configuration_info.configuration_types_supported = data_acquisition_system_data.get('configuration_types_supported')
            configuration_info.additional_configuration_info = data_acquisition_system_data.get('additional_configuration_info')
            
            configuration_info.humidity_sensor_manufacturer = meteorological_instrumentation_data.get('humidity_sensor_manufacturer')
            configuration_info.humidity_sensor_model = meteorological_instrumentation_data.get('humidity_sensor_model')
            configuration_info.humidity_sensor_accuracy = meteorological_instrumentation_data.get('humidity_sensor_accuracy')
            configuration_info.humidity_sensor_effective_dates = meteorological_instrumentation_data.get('humidity_sensor_effective_dates')
            configuration_info.addtional_humidity_sensor_info = meteorological_instrumentation_data.get('addtional_humidity_sensor_info')
            configuration_info.pressure_sensor_manufacturer = meteorological_instrumentation_data.get('pressure_sensor_manufacturer')
            configuration_info.pressure_sensor_model = meteorological_instrumentation_data.get('pressure_sensor_model')
            configuration_info.pressure_sensor_accuracy = meteorological_instrumentation_data.get('pressure_sensor_accuracy')
            configuration_info.pressure_sensor_effective_dates = meteorological_instrumentation_data.get('pressure_sensor_effective_dates')
            configuration_info.pressure_sensor_height_relative_to_VLBI_in_meters = meteorological_instrumentation_data.get('pressure_sensor_height_relative_to_VLBI_in_meters')
            configuration_info.pressure_sensor_additional_info = meteorological_instrumentation_data.get('pressure_sensor_additional_info')
            configuration_info.temperature_sensor_manufacturer = meteorological_instrumentation_data.get('temperature_sensor_manufacturer')
            configuration_info.temperature_sensor_model = meteorological_instrumentation_data.get('temperature_sensor_model')
            configuration_info.temperature_sensor_accuracy = meteorological_instrumentation_data.get('temperature_sensor_accuracy')
            configuration_info.temperature_sensor_effective_dates = meteorological_instrumentation_data.get('temperature_sensor_effective_dates')
            configuration_info.temperature_sensor_additional_info = meteorological_instrumentation_data.get('temperature_sensor_additional_info')
            
            configuration_info.standard_type = time_and_frequency_standards_data.get('standard_type')
            configuration_info.installed_dates_duration = time_and_frequency_standards_data.get('installed_dates_duration')
            configuration_info.manufacturer = time_and_frequency_standards_data.get('manufacturer')
            configuration_info.model_number_or_ID = time_and_frequency_standards_data.get('model_number_or_ID')
            configuration_info.additional_info = time_and_frequency_standards_data.get('additional_info')

            configuration_info.first_equipment_type = auxilliary_equipment_data.get('first_equipment_type')
            configuration_info.first_installed_dates = auxilliary_equipment_data.get('first_installed_dates')
            configuration_info.fisrt_manufacturer = auxilliary_equipment_data.get('fisrt_manufacturer')
            configuration_info.fisrt_model_number_or_ID = auxilliary_equipment_data.get('fisrt_model_number_or_ID')
            configuration_info.first_additional_info = auxilliary_equipment_data.get('first_additional_info')
            configuration_info.second_equipment_type = auxilliary_equipment_data.get('second_equipment_type')
            configuration_info.second_installed_dates = auxilliary_equipment_data.get('second_installed_dates')
            configuration_info.second_manufacturer = auxilliary_equipment_data.get('second_manufacturer')
            configuration_info.second_model_number_or_ID = auxilliary_equipment_data.get('second_model_number_or_ID')
            configuration_info.second_additional_info = auxilliary_equipment_data.get('second_additional_info')
            
            configuration_info.instrument_type = co_locations_data.get('instrument_type')
            configuration_info.instrument_name = co_locations_data.get('instrument_name')
            configuration_info.status = co_locations_data.get('status')
            configuration_info.effective_dates = co_locations_data.get('effective_dates')
            configuration_info.included_in_local_survey = co_locations_data.get('included_in_local_survey')
            configuration_info.additional_info = co_locations_data.get('additional_info')
            
            configuration_info.computer_system_vendor = field_system_computer_data.get('computer_system_vendor')
            configuration_info.computer_CPU = field_system_computer_data.get('computer_CPU')
            configuration_info.computer_CPU_speed_in_MHz = field_system_computer_data.get('computer_CPU_speed_in_MHz')
            configuration_info.computer_memory_in_Mbytes = field_system_computer_data.get('computer_memory_in_Mbytes')
            configuration_info.computer_disk_in_Gbytes = field_system_computer_data.get('computer_disk_in_Gbytes')
            configuration_info.computer_Linux_release = field_system_computer_data.get('computer_Linux_release')
            configuration_info.computer_internet_connection = field_system_computer_data.get('computer_internet_connection')
            configuration_info.antenna_interface_type = field_system_computer_data.get('antenna_interface_type')
            configuration_info.spare_FS_computer = field_system_computer_data.get('spare_FS_computer')
            configuration_info.known_RFI_sources = field_system_computer_data.get('known_RFI_sources')
            
            configuration_info.agency = on_site_contact_data.get('agency')
            configuration_info.shipping_address = on_site_contact_data.get('shipping_address')
            configuration_info.postal_address = on_site_contact_data.get('postal_address')
            configuration_info.agency_URL_of_site_web_page = on_site_contact_data.get('URL_of_site_web_page')
            configuration_info.on_site_friend_of_VLBI_name = on_site_contact_data.get('on_site_friend_of_VLBI_name')
            configuration_info.primary_telephone_of_on_site_friend_of_VLBI = on_site_contact_data.get('primary_telephone_of_on_site_friend_of_VLBI')
            configuration_info.alternative_telephone_of_on_site_friend_of_VLBI = on_site_contact_data.get('alternative_telephone_of_on_site_friend_of_VLBI')
            configuration_info.fax_of_on_site_friend_of_VLBI = on_site_contact_data.get('fax_of_on_site_friend_of_VLBI')
            configuration_info.email_of_on_site_friend_of_VLBI = on_site_contact_data.get('email_of_on_site_friend_of_VLBI')
            configuration_info.primary_telephone_of_VLBI_operations_room = on_site_contact_data.get('primary_telephone_of_VLBI_operations_room')
            configuration_info.alternative_telephone_of_VLBI_operations_room = on_site_contact_data.get('alternative_telephone_of_VLBI_operations_room')
            configuration_info.fax_of_VLBI_operations_room = on_site_contact_data.get('fax_of_VLBI_operations_room')
            configuration_info.email_of_VLBI_operations_room = on_site_contact_data.get('email_of_VLBI_operations_room')
            configuration_info.name_of_other_on_site_contact = on_site_contact_data.get('name_of_other_on_site_contact')
            configuration_info.primary_telephone_of_other_on_site_contact = on_site_contact_data.get('primary_telephone_of_other_on_site_contact')
            configuration_info.alternative_telephone_of_other_on_site_contact = on_site_contact_data.get('alternative_telephone_of_other_on_site_contact')
            configuration_info.fax_of_other_on_site_contact = on_site_contact_data.get('fax_of_other_on_site_contact')
            configuration_info.email_of_other_on_site_contact = on_site_contact_data.get('email_of_other_on_site_contact')
            configuration_info.additional_info = on_site_contact_data.get('additional_info')
            
            configuration_info.responsible_agency = responsible_agency_data.get('responsible_agency')
            configuration_info.responsible_agency_shipping_address = responsible_agency_data.get('shipping_address')
            configuration_info.responsible_agency_postal_address = responsible_agency_data.get('postal_address')
            configuration_info.URL_of_agency_web_page = responsible_agency_data.get('URL_of_agency_web_page')
            configuration_info.primary_administrative_agency_contact_person = responsible_agency_data.get('primary_administrative_agency_contact_person')
            configuration_info.primary_telephone_of_contact_person = responsible_agency_data.get('primary_telephone_of_contact_person')
            configuration_info.alternative_telephone_of_contact_person = responsible_agency_data.get('alternative_telephone_of_contact_person')
            configuration_info.fax_of_contact_person = responsible_agency_data.get('fax_of_contact_person')
            configuration_info.email_of_contact_person = responsible_agency_data.get('email_of_contact_person')
            configuration_info.alternative_agency_contact = responsible_agency_data.get('alternative_agency_contact')
            configuration_info.alternative_agency_shipping_address = responsible_agency_data.get('alternative_agency_shipping_address')
            configuration_info.alternative_agency_postal_address = responsible_agency_data.get('alternative_agency_postal_address')
            configuration_info.alternative_agency_URL_of_agency_web_page = responsible_agency_data.get('alternative_agency_URL_of_agency_web_page')
            configuration_info.primary_administrative_alternative_agency_contact_person = responsible_agency_data.get('primary_administrative_alternative_agency_contact_person')
            configuration_info.primary_telephone_of_alternative_agency_contact_person = responsible_agency_data.get('primary_telephone_of_alternative_agency_contact_person')
            configuration_info.alternative_contact_person = responsible_agency_data.get('alternative_contact_person')
            configuration_info.alternative_telephone = responsible_agency_data.get('alternative_telephone')
            configuration_info.fax_of_alternative_contact_person = responsible_agency_data.get('fax_of_alternative_contact_person')
            configuration_info.email_of_alternative_contact_person = responsible_agency_data.get('email_of_alternative_contact_person')
            configuration_info.additional_info = responsible_agency_data.get('additional_info')
            configuration_info.more_info = responsible_agency_data.get('more_info')

            try:
                configuration_info.save()
                # Clear only the configuration data from session, not the entire session
                session_keys_to_clear = [
                    'contact_data', 'site_identification_data', 'site_local_network_info_data',
                    'site_descriptive_info_data', 'antenna_details_data', 'receiver_data',
                    'cables_receiver_and_backend_data', 'data_acquisition_system',
                    'meteorological_instrumentation', 'time_and_frequency_standards',
                    'auxilliary_equipment', 'co_locations', 'field_system_computer',
                    'on_site_contact', 'responsible_agency'
                ]
                for key in session_keys_to_clear:
                    if key in request.session:
                        del request.session[key]

                return redirect('configuration_success')
            except Exception as e:
                messages.error(request, f'Error saving configuration: {str(e)}. Please try again.')
                return redirect('configuration_summary')
        else:
            messages.error(request, 'You must be logged in to submit the configuration.')
            return redirect('login')

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

@login_required
def configuration_success_view(request):
    return render(request, 'configuration/success.html')

# @login_required
#def user_antenna_data(request):
#    user_antenna_data = AntennaInfo.objects.filter(user=request.user)
#   return render(request, 'antenna/user_data.html', {'antenna_data': user_antenna_data})