from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from antenna.models import AntennaInfo
from configuration.models import ConfigurationInfo
from logbook.models import LogbookInfo
from auditlog.models import LogEntry

# Create your views here.
@login_required
def summary_view(request):
    # Fetch user's data from all models - get the most recent record for each
    try:
        antenna_data = AntennaInfo.objects.filter(user=request.user).order_by('-id').first()
    except AntennaInfo.DoesNotExist:
        antenna_data = None
    
    try:
        configuration_data = ConfigurationInfo.objects.filter(user=request.user).order_by('-id').first()
    except ConfigurationInfo.DoesNotExist:
        configuration_data = None
    
    # Get all logbook entries for the user
    logbook_entries = LogbookInfo.objects.filter(user=request.user).order_by('-entry_time')
    
    context = {
        'antenna_data': antenna_data,
        'configuration_data': configuration_data,
        'logbook_entries': logbook_entries,
    }
    
    return render(request, 'summary/summary.html', context)

@login_required
def user_logs_view(request):
    # Get audit log entries for the user's data
    antenna_logs = LogEntry.objects.filter(
        content_type__model='antennainfo',
        object_id__in=AntennaInfo.objects.filter(user=request.user).values_list('id', flat=True)
    ).order_by('-timestamp')
    
    configuration_logs = LogEntry.objects.filter(
        content_type__model='configurationinfo',
        object_id__in=ConfigurationInfo.objects.filter(user=request.user).values_list('id', flat=True)
    ).order_by('-timestamp')
    
    # Get logbook entries (these don't use auditlog, they are direct entries)
    logbook_entries = LogbookInfo.objects.filter(user=request.user).order_by('-entry_time')
    
    # Combine all logs and sort by timestamp
    all_logs = []
    
    # Helper function to convert action codes to readable text
    def get_action_text(action_code):
        action_map = {
            0: 'CREATE',
            1: 'UPDATE', 
            2: 'DELETE'
        }
        return action_map.get(action_code, f'UNKNOWN ({action_code})')
    
    # Add antenna logs
    for log in antenna_logs:
        # Get changes from the log entry
        changes = {}
        if hasattr(log, 'changes_display_dict') and log.changes_display_dict:
            changes = log.changes_display_dict
        elif hasattr(log, 'changes') and log.changes:
            # Parse changes if it's a string
            try:
                import json
                changes = json.loads(log.changes) if isinstance(log.changes, str) else log.changes
            except:
                changes = {'raw_changes': str(log.changes)}
        
        all_logs.append({
            'timestamp': log.timestamp,
            'action': get_action_text(log.action),
            'model': 'Antenna Information',
            'changes': changes,
            'user': log.actor,
            'object_repr': log.object_repr,
        })
    
    # Add configuration logs
    for log in configuration_logs:
        # Get changes from the log entry
        changes = {}
        if hasattr(log, 'changes_display_dict') and log.changes_display_dict:
            changes = log.changes_display_dict
        elif hasattr(log, 'changes') and log.changes:
            # Parse changes if it's a string
            try:
                import json
                changes = json.loads(log.changes) if isinstance(log.changes, str) else log.changes
            except:
                changes = {'raw_changes': str(log.changes)}
        
        all_logs.append({
            'timestamp': log.timestamp,
            'action': get_action_text(log.action),
            'model': 'Configuration Information',
            'changes': changes,
            'user': log.actor,
            'object_repr': log.object_repr,
        })
    
    # Add logbook entries
    for entry in logbook_entries:
        all_logs.append({
            'timestamp': entry.entry_time,
            'action': 'CREATE',
            'model': 'Logbook Entry',
            'changes': {
                'Event Time': str(entry.event_time),
                'Technician/Editor': entry.technician_editor or 'Not provided',
                'Telescope': entry.telescope,
                'Component': entry.get_component() or 'Not provided',
                'Details': entry.detailed_info or 'Not provided',
            },
            'user': request.user,
            'object_repr': f"Logbook entry for {entry.telescope}",
        })
    
    # Sort all logs by timestamp (most recent first)
    all_logs.sort(key=lambda x: x['timestamp'], reverse=True)
    
    context = {
        'all_logs': all_logs,
        'antenna_logs': antenna_logs,
        'configuration_logs': configuration_logs,
        'logbook_entries': logbook_entries,
    }
    
    return render(request, 'summary/user_logs.html', context)
