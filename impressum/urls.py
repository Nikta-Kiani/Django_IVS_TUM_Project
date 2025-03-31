from django.urls import path
from . import views

urlpatterns = [
    path('impressum/', views.impressum_view, name='impressum'),
]