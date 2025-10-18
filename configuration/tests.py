from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import ConfigurationInfo
from datetime import datetime, date
import json

class ConfigurationFormSubmissionTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
    
    def test_configuration_form_submission_redirects_to_success(self):
        """Test that configuration form submission redirects to success page"""
        # Submit configuration summary form data
        form_data = {
            'form_type': 'submit_form',
            'prepared_by_full_name': 'John Doe',
            'email': 'john@example.com',
            'update_date': '2024-01-15',
            'report_type': 'Initial Report',
            'site_name': 'Test Site',
            'site_8_letter_code': 'TESTSITE',
            'site_2_letter_code': 'TS',
            'IERS_domes_number': '12345',
            'CDP_occupation_code': '1',
            'CDP_monument_number': '100',
            'IGS_station_code': 'TEST',
            'ILRS_station_name': 'Test Station',
            'survey_into_national_network': 'on',
            'start_date_of_operation': '2024-01-01',
            'additional_info': 'Test additional info',
            'antenna_type': 'Test Antenna',
            'diameter_m': '12.0',
            'axis_type': 'Alt-Az',
            'axis_offset_m': '0.5',
            'slew_rate_first_axis_deg_min': '10.0',
            'slew_rate_second_axis_deg_min': '15.0',
            'min_limit_first_axis_deg': '0.0',
            'max_limit_first_axis_deg': '360.0',
            'min_limit_second_axis_deg': '0.0',
            'max_limit_second_axis_deg': '90.0',
            'horizon_mask_data_azimuth_deg_coressponding_elevationmask_deg': '0,5;90,10',
            'start_date_of_occupation': '2024-01-01',
            'end_date_of_occupation': '2024-12-31',
            'additional_info': 'Test antenna info',
            'feed_location': 'Primary Focus',
            'feed_type': 'Dual Band',
            'x_first_stage_amplifier': 'Test X Amp',
            's_first_stage_amplifier': 'Test S Amp',
            'x_bandwidth_mhz': '500.0',
            's_bandwidth_mhz': '500.0',
            'x_tsys_at_zenith_k': '50.0',
            's_tsys_at_zenith_k': '60.0',
            'x_sefd_jy': '1000.0',
            's_sefd_jy': '1200.0',
            'x_aperture_efficiency': '0.6',
            's_aperture_efficiency': '0.7',
            'x_lo_frequencies_mhz': '8000.0',
            's_lo_frequencies_mhz': '2200.0',
            'phase_calibrator_type': 'Test Calibrator',
            'additional_info': 'Test receiver info'
        }
        
        response = self.client.post(reverse('configuration_summary'), form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('configuration_success'))
        
        # Verify data was saved (basic check)
        self.assertTrue(ConfigurationInfo.objects.filter(user=self.user).exists())
    
    def test_configuration_success_page_loads(self):
        """Test that configuration success page loads correctly"""
        response = self.client.get(reverse('configuration_success'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Success!')
        self.assertContains(response, 'configuration information has been successfully saved')
    
    def test_configuration_form_requires_authentication(self):
        """Test that configuration form requires authentication"""
        self.client.logout()
        response = self.client.get(reverse('configuration_summary'))
        self.assertRedirects(response, '/login/?next=/configuration/summary/')
