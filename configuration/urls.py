from django.urls import path
from . import views

urlpatterns = [
    path('', views.configuration_view, name='configuration'),
    path('contact/', views.contact_view, name='contact'),
    path('site_identification/', views.site_identification_view, name='site_identification'),
    path('site_local_network_info/', views.site_local_network_info_view, name='site_local_network_info'),
    path('site_descriptive_info/', views.site_descriptive_info_view, name='site_descriptive_info'),
    path('antenna_details/', views.antenna_details_view, name='antenna_details'),
    path('receiver/', views.receiver_view, name='receiver'),
    path('cables_receiver_and_backend/', views.cables_receiver_and_backend_view, name='cables_receiver_and_backend'),
    path('data_acquisition_system/', views.data_acquisition_system_view, name='data_acquisition_system'),
    path('meteorological_instrumentation/', views.meteorological_instrumentation_view, name='meteorological_instrumentation'),
    path('time_and_frequency_standards/', views.time_and_frequency_standards_view, name='time_and_frequency_standards'),
    path('auxilliary_equipment/', views.auxilliary_equipment_view, name='auxilliary_equipment'),
    path('co_locations/', views.co_locations_view, name='co_locations'),
    path('field_system_computer/', views.field_system_computer_view, name='field_system_computer'),
    path('on_site_contact/', views.on_site_contact_view, name='on_site_contact'),
    path('responsible_agency/', views.responsible_agency_view, name='responsible_agency'),
    path('summary/', views.configuration_summary_view, name='configuration_summary'),
    path('success/', views.configuration_success_view, name='configuration_success'),
]