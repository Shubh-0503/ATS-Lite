#Notifications HTML page URLs
from django.urls import path
from . import template_views as views

urlpatterns = [
    path('', views.notification_list, name='notification_list'),
    path('<int:pk>/toggle/', views.toggle_read, name='toggle_notification'),
    path('mark-all-read/', views.mark_all_read, name='mark_all_read'),
]
