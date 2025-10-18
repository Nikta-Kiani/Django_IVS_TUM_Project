from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import LogbookInfo
from datetime import datetime, date
import json

class LogbookFormSubmissionTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
    
    def test_logbook_form_submission_redirects_to_success(self):
        """Test that logbook form submission redirects to success page"""
        # Submit logbook form data
        form_data = {
            'entry_time': '2024-01-15T10:30',
            'event_time': '2024-01-15T10:00',
            'technician_editor': 'John Doe',
            'participants': 'Jane Smith, Bob Johnson',
            'telescope': 'Test Telescope',
            'component': '1.1',  # Use a valid choice from COMPONENTS
            'detailed_info': 'Test detailed information',
            'attachment': ''  # Empty file field
        }
        
        # First submit the form (should redirect to summary)
        response = self.client.post(reverse('logbook_form'), form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('logbook_summary'))
        
        # Then submit the summary form (should redirect to success)
        summary_data = {
            'form_type': 'submit_form',
            **form_data
        }
        response = self.client.post(reverse('logbook_summary'), summary_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('logbook_success'))
        
        # Verify data was saved
        self.assertTrue(LogbookInfo.objects.filter(user=self.user).exists())
        logbook_entry = LogbookInfo.objects.get(user=self.user)
        self.assertEqual(logbook_entry.technician_editor, 'John Doe')
        self.assertEqual(logbook_entry.telescope, 'Test Telescope')
    
    def test_logbook_success_page_loads(self):
        """Test that logbook success page loads correctly"""
        response = self.client.get(reverse('logbook_success'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Success!')
        self.assertContains(response, 'logbook entry has been successfully saved')
    
    def test_logbook_form_requires_authentication(self):
        """Test that logbook form requires authentication"""
        self.client.logout()
        response = self.client.get(reverse('logbook_form'))
        self.assertRedirects(response, '/login/?next=/logbook/form/')
