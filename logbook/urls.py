from django.urls import path
from . import views

urlpatterns = [
    path('', views.logbook_view, name='logbook'),
    path('form/', views.logbook_form_view, name='logbook_form'),
    path('summary/', views.logbook_summary_view, name='logbook_summary'),
    path('success/', views.logbook_success_view, name='logbook_success'),
]