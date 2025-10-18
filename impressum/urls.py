from django.urls import path
from . import views

urlpatterns = [
    path('imprint/', views.imprint_view, name='imprint'),
]