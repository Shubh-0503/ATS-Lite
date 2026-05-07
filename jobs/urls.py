#Jobs HTML page URL patterns.
from django.urls import path
from . import template_views as views

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('<int:pk>/', views.job_detail, name='job_detail'),
    path('create/', views.job_create, name='job_create'),
    path('<int:pk>/edit/', views.job_edit, name='job_edit'),
    path('<int:pk>/delete/', views.job_delete, name='job_delete'),
]
