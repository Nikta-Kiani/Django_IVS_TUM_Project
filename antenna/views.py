from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import RequestForm, SiteDescriptionForm, DomesInfoForm, ApproximatePositionForm, InstrumentForm, OperationContactForm, SiteContactForm
from django.contrib.auth.decorators import login_required
from .models import AntennaInfo
from django.http import JsonResponse
import datetime
# Create your views here.

@login_required
def antenna_view(request):
    
    return render(request, 'antenna/antenna.html')
     # If the user is authenticated, show a personalized antenna welcome page
    #if request.user.is_authenticated:
     #   return redirect('request_form')
    # Render the welcome page with the registration and login forms
    #return render(request, 'antenna/antenna.html',{
     #  'is_authenticated': False,})

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


    if request.method == 'POST'and request.POST.get("form_type") == "submit_form":
        # Ensure session data is present
        if not request_data:
            request_data = {
                'full_name': request.POST.get('full_name'),
                'agency': request.POST.get('agency'),
                'email': request.POST.get('email'),
                'date': request.POST.get('date'),
            }

        if not site_description_data:
            site_description_data = {
                'site_name': request.POST.get('site_name'),
                'city_or_town': request.POST.get('city_or_town'),
                'state_or_province': request.POST.get('state_or_province'),
                'country': request.POST.get('country'),
                'point_description': request.POST.get('point_description'),
                'support_description': request.POST.get('support_description'),
                'picture': request.FILES.get('picture'),  # Ensure file upload works
            }

        if not domes_info_data:
            domes_info_data = {
                'domes_number': request.POST.get('domes_number'),
                'local_number': request.POST.get('local_number'),
                'four_char_code': request.POST.get('four_char_code'),
            }

        if not approximate_position_data:
            approximate_position_data = {
                'x_coordinate_m': request.POST.get('x_coordinate_m'),
                'y_coordinate_m': request.POST.get('y_coordinate_m'),
                'z_coordinate_m': request.POST.get('z_coordinate_m'),
                'latitude_deg_min': request.POST.get('latitude_deg_min'),
                'longitude_deg_min': request.POST.get('longitude_deg_min'),
                'elevation_m': request.POST.get('elevation_m'),
                'tectonic_plate': request.POST.get('tectonic_plate'),
            }

        if not instrument_data:
            instrument_data = {
                'instrument': request.POST.get('instrument'),
                'date_of_installation': request.POST.get('date_of_installation'),
            }

        if not operation_contact_data:
            operation_contact_data = {
                'operation_contact_name': request.POST.get('operation_contact_name'),
                'operation_agency': request.POST.get('operation_agency'),
                'operation_email_one': request.POST.get('operation_email_one'),
                'operation_email_two': request.POST.get('operation_email_two'),
            }

        if not site_contact_data:
            site_contact_data = {
                'site_contact_name': request.POST.get('site_contact_name'),
                'site_agency': request.POST.get('site_agency'),
                'site_email': request.POST.get('site_email'),
                'additional_info': request.POST.get('additional_info'),
            }
        # If the form is submitted, save the data to the model
        antenna_info = AntennaInfo(
            user=request.user,
            full_name=request_data.get('full_name'),
            agency=request_data.get('agency'),
            email=request_data.get('email'),
            date=request_data.get('date'),

            site_name=site_description_data.get('site_name'),
            city_or_town=site_description_data.get('city_or_town'),
            state_or_province=site_description_data.get('state_or_province'),
            country=site_description_data.get('country'),
            point_description=site_description_data.get('point_description'),
            support_description=site_description_data.get('support_description'),
            picture=site_description_data.get('picture'),
            
            domes_number=domes_info_data.get('domes_number'),
            local_number=domes_info_data.get('local_number'),
            four_char_code=domes_info_data.get('four_char_code'),

            x_coordinate_m=approximate_position_data.get('x_coordinate_m'),
            y_coordinate_m=approximate_position_data.get('y_coordinate_m'),
            z_coordinate_m=approximate_position_data.get('z_coordinate_m'),
            latitude_deg_min=approximate_position_data.get('latitude_deg_min'),
            longitude_deg_min=approximate_position_data.get('longitude_deg_min'),
            elevation_m=approximate_position_data.get('elevation_m'),
            tectonic_plate=approximate_position_data.get('tectonic_plate'),

            instrument=instrument_data.get('instrument'),
            date_of_installation=instrument_data.get('date_of_installation'),

            operation_contact_name=operation_contact_data.get('operation_contact_name'),
            operation_agency=operation_contact_data.get('operation_agency'),
            operation_email_one=operation_contact_data.get('operation_email_one'),
            operation_email_two=operation_contact_data.get('operation_email_two'),

            site_contact_name=site_contact_data.get('site_contact_name'),
            site_agency=site_contact_data.get('site_agency'),
            site_email=site_contact_data.get('site_email'),
            additional_info=site_contact_data.get('additional_info'),
        )
        antenna_info.save()
                # Clear session after saving
        request.session.flush()

        return redirect('configuration')  # Redirect to the configuration page after saving
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

#@login_required
#def user_antenna_data(request):
#    user_antenna_data = AntennaInfo.objects.filter(user=request.user)
 #   return render(request, 'antenna/user_data.html', {'antenna_data': user_antenna_data})
