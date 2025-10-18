from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import RequestForm, SiteDescriptionForm, DomesInfoForm, ApproximatePositionForm, InstrumentForm, OperationContactForm, SiteContactForm
from django.contrib.auth.decorators import login_required
from .models import AntennaInfo
from django.http import JsonResponse
import datetime
import logging
# Create your views here.
logger = logging.getLogger(__name__)

@login_required
def antenna_view(request):
    # Since @login_required ensures user is authenticated, redirect to request form
    return redirect('request_form')

@login_required
def request_form_view(request):
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            # Get cleaned data from the form
            request_data = form.cleaned_data

            if 'date' in request_data:
                request_data['date'] = request_data['date'].isoformat()

            # Save the cleaned and processed data in the session
            request.session['request_data'] = request_data
            return redirect('site_description')
    else:
        # Pre-fill form with existing user data if available
        if request.user.is_authenticated:
            try:
                instance = AntennaInfo.objects.get(user=request.user)
                form = RequestForm(instance=instance)
            except AntennaInfo.DoesNotExist:
                form = RequestForm()
        else:
            form = RequestForm()
    return render(request, 'antenna/request_form.html', {'form': form})

@login_required
def site_description_view(request):
    if request.method == 'POST':
        form = SiteDescriptionForm(request.POST)
        if form.is_valid():
            request.session['site_description_data'] = form.cleaned_data
            return redirect('domes_info')
    else:
        # Pre-fill form with existing user data if available
        if request.user.is_authenticated:
            try:
                instance = AntennaInfo.objects.get(user=request.user)
                form = SiteDescriptionForm(instance=instance)
            except AntennaInfo.DoesNotExist:
                form = SiteDescriptionForm()
        else:
            form = SiteDescriptionForm()
    return render(request, 'antenna/site_description.html', {'form': form})

@login_required
def domes_info_view(request):
    if request.method == 'POST':
        form = DomesInfoForm(request.POST)
        if form.is_valid():
            request.session['domes_info_data'] = form.cleaned_data
            # Continue with the next tab or the summary page
            return redirect('approximate_position')
    else:
        # Pre-fill form with existing user data if available
        if request.user.is_authenticated:
            try:
                instance = AntennaInfo.objects.get(user=request.user)
                form = DomesInfoForm(instance=instance)
            except AntennaInfo.DoesNotExist:
                form = DomesInfoForm()
        else:
            form = DomesInfoForm()
    return render(request, 'antenna/domes_info.html', {'form': form})

@login_required
def approximate_position_view(request):
    if request.method == 'POST':
        form = ApproximatePositionForm(request.POST)
        if form.is_valid():
            request.session['approximate_position_data'] = form.cleaned_data
            # Continue with the next tab or the summary page
            return redirect('instrument')
    else:
        # Pre-fill form with existing user data if available
        if request.user.is_authenticated:
            try:
                instance = AntennaInfo.objects.get(user=request.user)
                form = ApproximatePositionForm(instance=instance)
            except AntennaInfo.DoesNotExist:
                form = ApproximatePositionForm()
        else:
            form = ApproximatePositionForm()
    return render(request, 'antenna/approximate_position.html', {'form': form})

@login_required
def instrument_view(request):
    if request.method == 'POST':
        form = InstrumentForm(request.POST)
        if form.is_valid():
            # Get cleaned data from the form
            instrument_data = form.cleaned_data
            
            if 'date_of_installation' in instrument_data:
                instrument_data['date_of_installation'] = instrument_data['date_of_installation'].isoformat()
            
            # Save the cleaned and processed data in the session
            request.session['instrument_data'] = instrument_data
            # Continue with the next tab or the summary page
            return redirect('operation_contact')
    else:
        # Pre-fill form with existing user data if available
        if request.user.is_authenticated:
            try:
                instance = AntennaInfo.objects.get(user=request.user)
                form = InstrumentForm(instance=instance)
            except AntennaInfo.DoesNotExist:
                form = InstrumentForm()
        else:
            form = InstrumentForm()
    return render(request, 'antenna/instrument.html', {'form': form})

@login_required
def operation_contact_view(request):
    if request.method == 'POST':
        form = OperationContactForm(request.POST)
        if form.is_valid():
            request.session['operation_contact_data'] = form.cleaned_data
            # Continue with the next tab or the summary page
            return redirect('site_contact')
    else:
        # Pre-fill form with existing user data if available
        if request.user.is_authenticated:
            try:
                instance = AntennaInfo.objects.get(user=request.user)
                form = OperationContactForm(instance=instance)
            except AntennaInfo.DoesNotExist:
                form = OperationContactForm()
        else:
            form = OperationContactForm()
    return render(request, 'antenna/operation_contact.html', {'form': form})

@login_required
def site_contact_view(request):
    if request.method == 'POST':
        form = SiteContactForm(request.POST)
        if form.is_valid():
            request.session['site_contact_data'] = form.cleaned_data
            # Continue with the next tab or the summary page
            return redirect('antenna_summary')
    else:
        # Pre-fill form with existing user data if available
        if request.user.is_authenticated:
            try:
                instance = AntennaInfo.objects.get(user=request.user)
                form = SiteContactForm(instance=instance)
            except AntennaInfo.DoesNotExist:
                form = SiteContactForm()
        else:
            form = SiteContactForm()
    return render(request, 'antenna/site_contact.html', {'form': form})

@login_required
def antenna_summary_view(request):
    # Gather all the data from the session
    request_data = request.session.get('request_data', {})
    site_description_data = request.session.get('site_description_data', {})
    domes_info_data = request.session.get('domes_info_data', {})
    approximate_position_data = request.session.get('approximate_position_data', {})
    instrument_data = request.session.get('instrument_data', {})
    operation_contact_data = request.session.get('operation_contact_data', {})
    site_contact_data = request.session.get('site_contact_data', {})

    if request.method == 'POST' and request.POST.get("form_type") == "submit_form":
        # Validate that all required session data is present
        missing_fields = []
        
        # Check request form data
        if not request_data.get('full_name'):
            missing_fields.append('Full Name')
        if not request_data.get('agency'):
            missing_fields.append('Agency')
        if not request_data.get('email'):
            missing_fields.append('Email')
        if not request_data.get('date'):
            missing_fields.append('Date')
            
        # Check site description data
        if not site_description_data.get('site_name'):
            missing_fields.append('Site Name')
        if not site_description_data.get('city_or_town'):
            missing_fields.append('City or Town')
        if not site_description_data.get('state_or_province'):
            missing_fields.append('State or Province')
        if not site_description_data.get('country'):
            missing_fields.append('Country')
            
        # Check domes info data
        if not domes_info_data.get('domes_number'):
            missing_fields.append('DOMES Number')
        if not domes_info_data.get('local_number'):
            missing_fields.append('Local Number')
        if not domes_info_data.get('four_char_code'):
            missing_fields.append('4-Character Code')
            
        # Check approximate position data
        if approximate_position_data.get('latitude_deg_min') is None:
            missing_fields.append('Latitude')
        if approximate_position_data.get('longitude_deg_min') is None:
            missing_fields.append('Longitude')
        if approximate_position_data.get('elevation_m') is None:
            missing_fields.append('Elevation')
            
        # Check instrument data
        if not instrument_data.get('instrument'):
            missing_fields.append('Instrument')
        if not instrument_data.get('date_of_installation'):
            missing_fields.append('Installation Date')
            
        # Check operation contact data
        if not operation_contact_data.get('operation_contact_name'):
            missing_fields.append('Operation Contact Name')
        if not operation_contact_data.get('operation_agency'):
            missing_fields.append('Operation Agency')
        if not operation_contact_data.get('operation_email_one'):
            missing_fields.append('Operation Email')
            
        # Check site contact data
        if not site_contact_data.get('site_contact_name'):
            missing_fields.append('Site Contact Name')
        if not site_contact_data.get('site_agency'):
            missing_fields.append('Site Agency')
        if not site_contact_data.get('site_email'):
            missing_fields.append('Site Email')
        
        # If there are missing required fields, show error and redirect back
        if missing_fields:
            from django.contrib import messages
            messages.error(request, f'Please complete the following required fields: {", ".join(missing_fields)}. Please go back and fill them in.')
            return redirect('antenna_summary')
        
        # Check if entry exists, else create
        antenna_info, created = AntennaInfo.objects.get_or_create(user=request.user)
        if created:
            logger.info(f"Created new AntennaInfo for user {request.user}")
        else:
            logger.info(f"Retrieved existing AntennaInfo for user {request.user}")
        
        # If the form is submitted, save the data to the model
        antenna_info.full_name = request_data.get('full_name')
        antenna_info.agency = request_data.get('agency')
        antenna_info.email = request_data.get('email')
        
        # Handle date conversion from ISO format string back to date object
        date_value = request_data.get('date')
        if isinstance(date_value, str):
            try:
                antenna_info.date = datetime.datetime.fromisoformat(date_value).date()
            except (ValueError, TypeError):
                antenna_info.date = datetime.date.today()
        else:
            antenna_info.date = date_value or datetime.date.today()

        antenna_info.site_name = site_description_data.get('site_name')
        antenna_info.city_or_town = site_description_data.get('city_or_town')
        antenna_info.state_or_province = site_description_data.get('state_or_province')
        antenna_info.country = site_description_data.get('country')
        antenna_info.point_description = site_description_data.get('point_description')
        antenna_info.support_description = site_description_data.get('support_description')
        antenna_info.picture = site_description_data.get('picture')

        antenna_info.domes_number = domes_info_data.get('domes_number')
        antenna_info.local_number = domes_info_data.get('local_number')
        antenna_info.four_char_code = domes_info_data.get('four_char_code')

        antenna_info.x_coordinate_m = approximate_position_data.get('x_coordinate_m')
        antenna_info.y_coordinate_m = approximate_position_data.get('y_coordinate_m')
        antenna_info.z_coordinate_m = approximate_position_data.get('z_coordinate_m')
        antenna_info.latitude_deg_min = approximate_position_data.get('latitude_deg_min')
        antenna_info.longitude_deg_min = approximate_position_data.get('longitude_deg_min')
        antenna_info.elevation_m = approximate_position_data.get('elevation_m')
        antenna_info.tectonic_plate = approximate_position_data.get('tectonic_plate')

        antenna_info.instrument = instrument_data.get('instrument')
        
        # Handle date_of_installation conversion from ISO format string back to date object
        installation_date = instrument_data.get('date_of_installation')
        if isinstance(installation_date, str):
            try:
                antenna_info.date_of_installation = datetime.datetime.fromisoformat(installation_date).date()
            except (ValueError, TypeError):
                antenna_info.date_of_installation = datetime.date.today()
        else:
            antenna_info.date_of_installation = installation_date or datetime.date.today()

        antenna_info.operation_contact_name = operation_contact_data.get('operation_contact_name')
        antenna_info.operation_agency = operation_contact_data.get('operation_agency')
        antenna_info.operation_email_one = operation_contact_data.get('operation_email_one')
        antenna_info.operation_email_two = operation_contact_data.get('operation_email_two')

        antenna_info.site_contact_name = site_contact_data.get('site_contact_name')
        antenna_info.site_agency = site_contact_data.get('site_agency')
        antenna_info.site_email = site_contact_data.get('site_email')
        antenna_info.additional_info = site_contact_data.get('additional_info')
        
        try:
            # Save → triggers auditlog create/update
            antenna_info.save()
            # Clear only the antenna form data from session, not the entire session
            session_keys_to_clear = [
                'request_data', 'site_description_data', 'domes_info_data',
                'approximate_position_data', 'instrument_data', 'operation_contact_data',
                'site_contact_data'
            ]
            for key in session_keys_to_clear:
                if key in request.session:
                    del request.session[key]
            return redirect('antenna_success')  # Redirect to the antenna success page after saving
        except Exception as e:
            from django.contrib import messages
            logger.error(f"Error saving antenna info: {str(e)}")
            messages.error(request, f'Error saving data: {str(e)}. Please try again.')
            return redirect('antenna_summary')

    # Combine all the data into one context dictionary
    context = {
        'request_data': request_data,
        'site_description_data': site_description_data,
        'domes_info_data': domes_info_data,
        'approximate_position_data': approximate_position_data,
        'instrument_data': instrument_data,
        'operation_contact_data': operation_contact_data,
        'site_contact_data': site_contact_data,
    }

    return render(request, 'antenna/summary.html', context)

@login_required
def antenna_success_view(request):
    return render(request, 'antenna/success.html')

#@login_required
#def user_antenna_data(request):
#    user_antenna_data = AntennaInfo.objects.filter(user=request.user)
#   return render(request, 'antenna/user_data.html', {'antenna_data': user_antenna_data})
