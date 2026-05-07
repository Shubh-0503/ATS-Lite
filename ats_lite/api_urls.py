from django.urls import path, include
from .token_auth import CustomAuthToken

urlpatterns = [
    # Get API token: POST with username + password
    path('auth/token/', CustomAuthToken.as_view(), name='api_token_auth'),

    # Job CRUD + search
    path('jobs/', include('jobs.api_urls')),

    # Candidate + application APIs
    path('candidates/', include('candidates.api_urls')),

    # Notification APIs
    path('notifications/', include('notifications.api_urls')),
]
