#Candidates HTML page URLs.

from django.urls import path
from . import template_views as views

urlpatterns = [
    path('apply/<int:job_id>/', views.apply_form, name='apply_form'),
    path('success/<int:app_id>/', views.application_success, name='application_success'),
    path('ranked/<int:job_id>/', views.candidate_list, name='candidate_list'),
]
