from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from antenna.models import AntennaInfo
from configuration.models import ConfigurationInfo
from logbook.models import LogbookInfo
from datetime import datetime, date
import json

class SummaryPageTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        
        # Create test data
        self.antenna_data = AntennaInfo.objects.create(
            user=self.user,
            full_name='John Doe',
            agency='Test Agency',
            email='john@example.com',
            date=date.today(),
            site_name='Test Site',
            city_or_town='Test City',
            country='Test Country',
            latitude_deg_min='50.0°N',
            longitude_deg_min='10.0°E',
            elevation_m=100.0,
            instrument='Test Instrument',
            date_of_installation=date.today(),
            operation_contact_name='John Contact',
            operation_agency='Test Agency',
            operation_email_one='contact@example.com',
            site_contact_name='Site Contact',
            site_agency='Site Agency',
            site_email='site@example.com'
        )
        
        self.config_data = ConfigurationInfo.objects.create(
            user=self.user,
            prepared_by_full_name='John Doe',
            email='john@example.com',
            site_name='Test Site',
            antenna_type='Test Antenna'
        )
        
        self.logbook_entry = LogbookInfo.objects.create(
            user=self.user,
            entry_time=datetime.now(),
            event_time=datetime.now(),
            technician_editor='John Doe',
            telescope='Test Telescope',
            component='Test Component',
            detailed_info='Test details'
        )
    
    def test_summary_page_loads_with_user_data(self):
        """Test that summary page loads and displays user's data correctly"""
        response = self.client.get(reverse('summary'))
        self.assertEqual(response.status_code, 200)
        
        # Check that all sections are present
        self.assertContains(response, 'Total Summary')
        self.assertContains(response, 'Antenna Information')
        self.assertContains(response, 'Configuration Information')
        self.assertContains(response, 'Logbook Entries')
        
        # Check that user data is displayed
        self.assertContains(response, 'John Doe')
        self.assertContains(response, 'Test Agency')
        self.assertContains(response, 'Test Site')
        self.assertContains(response, 'Test Antenna')
        self.assertContains(response, 'Test Telescope')
    
    def test_summary_page_with_no_data(self):
        """Test summary page when user has no data"""
        # Create a new user with no data
        new_user = User.objects.create_user(
            username='newuser',
            email='new@example.com',
            password='testpass123'
        )
        self.client.login(username='newuser', password='testpass123')
        
        response = self.client.get(reverse('summary'))
        self.assertEqual(response.status_code, 200)
        
        # Check that "No data" messages are displayed
        self.assertContains(response, 'No Antenna Data Available')
        self.assertContains(response, 'No Configuration Data Available')
        self.assertContains(response, 'No Logbook Entries Available')
    
    def test_summary_page_requires_authentication(self):
        """Test that summary page requires authentication"""
        self.client.logout()
        response = self.client.get(reverse('summary'))
        self.assertRedirects(response, '/login/?next=/summary/')
    
    def test_activity_log_page_loads(self):
        """Test that activity log page loads correctly"""
        response = self.client.get(reverse('user_logs'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Your Activity Logs')
        self.assertContains(response, 'All Activity')
    
    def test_activity_log_requires_authentication(self):
        """Test that activity log page requires authentication"""
        self.client.logout()
        response = self.client.get(reverse('user_logs'))
        self.assertRedirects(response, '/login/?next=/user-logs/')
    
    def test_summary_page_layout_elements(self):
        """Test that summary page has proper layout elements"""
        response = self.client.get(reverse('summary'))
        self.assertEqual(response.status_code, 200)
        
        # Check for Bootstrap classes used in two-column layout
        self.assertContains(response, 'col-md-6')
        self.assertContains(response, 'row')
        self.assertContains(response, 'card')
        self.assertContains(response, 'summary-container')
        
        # Check for View Activity Logs button
        self.assertContains(response, 'View Activity Logs')
        self.assertContains(response, 'fas fa-history')

class SummaryPageLayoutTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
    
    def test_summary_page_has_proper_margins(self):
        """Test that summary page has proper margins and spacing"""
        response = self.client.get(reverse('summary'))
        self.assertEqual(response.status_code, 200)
        
        # Check for custom CSS classes
        self.assertContains(response, 'summary-container')
        
        # Check that the page contains proper Bootstrap structure
        self.assertContains(response, 'container mt-4')
        self.assertContains(response, 'card mb-4')
    
    def test_two_column_layout_structure(self):
        """Test that summary page uses proper two-column layout structure"""
        response = self.client.get(reverse('summary'))
        self.assertEqual(response.status_code, 200)
        
        # Count the number of col-md-6 classes (should be even for two-column layout)
        content = response.content.decode('utf-8')
        col_count = content.count('col-md-6')
        self.assertGreater(col_count, 0)
        
        # Check for proper row structure
        self.assertContains(response, 'row')
        self.assertContains(response, 'col-md-6')
