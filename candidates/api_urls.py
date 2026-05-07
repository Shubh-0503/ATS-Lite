
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('', views.CandidateViewSet, basename='candidate')

urlpatterns = [
    path('apply/<int:job_id>/', views.apply_to_job, name='api_apply_job'),

    path('ranked/<int:job_id>/', views.ranked_candidates, name='api_ranked_candidates'),

    # Update application status
    path('application/<int:application_id>/status/', views.update_application_status, name='api_update_status'),

    # CRUD for candidates (read-only)
    path('', include(router.urls)),
]
