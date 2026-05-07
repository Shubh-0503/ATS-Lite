from django.urls import path
from django.contrib.auth import views as auth_views
from ats_lite import auth_views as custom_auth_views

urlpatterns = [
    path('login/', custom_auth_views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', custom_auth_views.register_view, name='register'),
]
