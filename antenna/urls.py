from django.urls import path
from . import views

urlpatterns = [
    path('', views.antenna_view, name='antenna'),
    path('request_form/', views.request_form_view, name='request_form'),
    path('site_description/', views.site_description_view, name='site_description'),
    path('domes_info/', views.domes_info_view, name='domes_info'),
    path('approximate_position/', views.approximate_position_view, name='approximate_position'),
    path('instrument/', views.instrument_view, name='instrument'),
    path('operation_contact/', views.operation_contact_view, name='operation_contact'),
    path('site_contact/', views.site_contact_view, name='site_contact'),
    path('summary/', views.antenna_summary_view, name='antenna_summary'),
    path('success/', views.antenna_success_view, name='antenna_success'),
]