from django.urls import path
from .views import register_view, login_view, logout_view,admin_otp_verify,create_staff,resend_admin_otp
from . import views
from accounts import views
from django.contrib.auth import views as auth_views
from .forms import CustomPasswordChangeForm
from .views import (forgot_password,reset_password)
urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('admin-panel/filter-logs/', views.filter_logs, name='filter_logs'),
    path('admin-otp-verify/',admin_otp_verify,name='admin_otp_verify'),
    path('create-staff/',create_staff,name='create_staff'),
    path('resend-admin-otp/',resend_admin_otp,name='resend_admin_otp'),
    # FORGOT PASSWORD


# CHANGE PASSWORD

path(
    'change-password/',
    views.change_password,
    name='change_password'
),

path(
    'forgot-password/',
    forgot_password,
    name='forgot_password'
),

path(
    'reset-password/<uidb64>/<token>/',
    reset_password,
    name='reset_password'
),


]