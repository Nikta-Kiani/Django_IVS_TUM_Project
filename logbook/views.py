from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import LogbookInfoForm
from django.contrib.auth.decorators import login_required
from .models import LogbookInfo
from django.http import JsonResponse
import datetime

# Create your views here.
#@login_required
def logbook_view(request):
    
     # If the user is authenticated, show a personalized logbook welcome page
    if request.user.is_authenticated:
        return redirect('logbook_form')
    # Render the welcome page with the registration and login forms
    return render(request, 'logbook/logbook.html',{
        'is_authenticated': False,})
    
#@login_required    
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
                
            if form.cleaned_data['new_component']:
                logbook_data.component = form.cleaned_data['new_component']

            # Save the cleaned and processed data in the session
            request.session['logbook_data'] = logbook_data
            return redirect('logbook_summary')
    else:
        form = LogbookInfoForm()
    return render(request, 'logbook/form.html', {'form': form})

#@login_required
def logbook_summary_view(request):
    # Gather all the data from the session
    logbook_data = request.session.get('logbook_data', {})
    
    if request.method == 'POST'and request.POST.get("form_type") == "submit_form":
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
             # If the form is submitted, save the data to the model
        logbook_info = LogbookInfo(
            user=request.user,
            entry_time=logbook_data.get('entry_time'),
            event_time=logbook_data.get('event_time'),
            technician_editor=logbook_data.get('technician_editor'),
            participants=logbook_data.get('participants'),
            telescope=logbook_data.get('telescope'),
            component=logbook_data.get('component'),
            detailed_info=logbook_data.get('detailed_info'),
            attachment=logbook_data.get('attachment'),
        )
        logbook_info.save()
        # Clear session after saving
        request.session.flush()

        return redirect('summary')  # Redirect to the summary page after saving
     # Combine all the data into one context dictionary
    context = {
        'logbook_data': logbook_data,
    }

    return render(request, 'logbook/summary.html', context)