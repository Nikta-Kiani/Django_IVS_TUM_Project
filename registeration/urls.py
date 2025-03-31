from django.urls import path
from . import views

urlpatterns = [
    path('registeration/', views.register_view, name='registeration'),
]