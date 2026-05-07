from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', RedirectView.as_view(url='/jobs/', permanent=False)),

    path('auth/', include('ats_lite.auth_urls')),
    path('jobs/', include('jobs.urls')),
    path('candidates/', include('candidates.urls')),
    path('notifications/', include('notifications.urls')),

    # REST API (versioned)
    path('api/v1/', include('ats_lite.api_urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
