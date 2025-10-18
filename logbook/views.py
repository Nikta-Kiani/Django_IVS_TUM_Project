from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import LogbookInfoForm
from django.contrib.auth.decorators import login_required
from .models import LogbookInfo
from django.http import JsonResponse
import datetime

# Create your views here.
@login_required
def logbook_view(request):
    # Since @login_required ensures user is authenticated, redirect to logbook form
    return redirect('logbook_form')
    
@login_required    
def logbook_form_view(request):
    if request.method == 'POST':
        form = LogbookInfoForm(request.POST)
        if form.is_valid():
            # Get cleaned data from the form
            logbook_data = form.cleaned_data

            if 'entry_time' in logbook_data:
                logbook_data['entry_time'] = logbook_data['entry_time'].isoformat()
            
            if 'event_time' in logbook_data:
                logbook_data['event_time'] = logbook_data['event_time'].isoformat()
                
            if form.cleaned_data.get('new_component'):
                logbook_data['component'] = form.cleaned_data['new_component']

            # Save the cleaned and processed data in the session
            request.session['logbook_data'] = logbook_data
            return redirect('logbook_summary')
    else:
        form = LogbookInfoForm()
    return render(request, 'logbook/form.html', {'form': form})

@login_required
def logbook_summary_view(request):
    # Gather all the data from the session
    logbook_data = request.session.get('logbook_data', {})
    
    if request.method == 'POST'and request.POST.get("form_type") == "submit_form":
        # Validate that all required session data is present
        missing_fields = []
        
        # Check logbook data
        if not logbook_data.get('event_time'):
            missing_fields.append('Event Time')
        if not logbook_data.get('technician_editor'):
            missing_fields.append('Technician/Editor')
        if not logbook_data.get('telescope'):
            missing_fields.append('Telescope')
        if not logbook_data.get('component'):
            missing_fields.append('Component')
        if not logbook_data.get('detailed_info'):
            missing_fields.append('Detailed Information')
            
        # If there are missing required fields, show error and redirect back
        if missing_fields:
            from django.contrib import messages
            messages.error(request, f'Please complete the following required fields: {", ".join(missing_fields)}. Please go back and fill them in.')
            return redirect('logbook_summary')
        
        # Ensure session data is present
        if not logbook_data:
            logbook_data = {
                'entry_time': request.POST.get('entry_time'),
                'event_time': request.POST.get('event_time'),
                'technician_editor': request.POST.get('technician_editor'),
                'participants': request.POST.get('participants'),
                'telescope': request.POST.get('telescope'),
                'component': request.POST.get('component'),
                'detailed_info': request.POST.get('detailed_info'),
                'attachment': request.POST.get('attachment'),
            }
        
        try:
            # Handle datetime conversion from ISO format string back to datetime object
            entry_time = logbook_data.get('entry_time')
            if isinstance(entry_time, str):
                try:
                    entry_time = datetime.datetime.fromisoformat(entry_time)
                except (ValueError, TypeError):
                    entry_time = datetime.datetime.now()
            else:
                entry_time = entry_time or datetime.datetime.now()
                
            event_time = logbook_data.get('event_time')
            if isinstance(event_time, str):
                try:
                    event_time = datetime.datetime.fromisoformat(event_time)
                except (ValueError, TypeError):
                    event_time = datetime.datetime.now()
            else:
                event_time = event_time or datetime.datetime.now()
            
            # If the form is submitted, save the data to the model
            logbook_info = LogbookInfo(
                user=request.user,
                entry_time=entry_time,
                event_time=event_time,
                technician_editor=logbook_data.get('technician_editor'),
                participants=logbook_data.get('participants'),
                telescope=logbook_data.get('telescope'),
                component=logbook_data.get('component'),
                detailed_info=logbook_data.get('detailed_info'),
                attachment=logbook_data.get('attachment'),
            )
            logbook_info.save()
            # Clear only the logbook data from session, not the entire session
            if 'logbook_data' in request.session:
                del request.session['logbook_data']

            return redirect('logbook_success')  # Redirect to the success page after saving
        except Exception as e:
            from django.contrib import messages
            messages.error(request, f'Error saving logbook entry: {str(e)}. Please try again.')
            return redirect('logbook_summary')
     # Combine all the data into one context dictionary
    context = {
        'logbook_data': logbook_data,
    }

    return render(request, 'logbook/summary.html', context)

@login_required
def logbook_success_view(request):
    return render(request, 'logbook/success.html')