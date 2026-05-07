#Notifications REST API URLS
from django.urls import path
from . import views

urlpatterns = [
    path('', views.NotificationListView.as_view(), name='api_notifications'),
    path('<int:pk>/read/', views.mark_read, name='api_mark_read'),
    path('<int:pk>/unread/', views.mark_unread, name='api_mark_unread'),
    path('mark-all-read/', views.mark_all_read, name='api_mark_all_read'),
]
