from django.urls import path
from . import views

urlpatterns = [
    path('summary/', views.summary_view, name='summary'),
    path('user-logs/', views.user_logs_view, name='user_logs'),
]