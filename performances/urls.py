from django.urls import path
from django.contrib.auth import views as auth_views

from .views import (
    performance_list,
    add_performance,
    my_performances,
    edit_performance,
    delete_performance
)

urlpatterns = [

    path(
        'performances/',
        performance_list,
        name='performance_list'
    ),

    path(
        'add-performance/',
        add_performance,
        name='add_performance'
    ),

    path(
        'my-performances/',
        my_performances,
        name='my_performances'
    ),

    path(

    'password-reset/',
    auth_views.PasswordResetView.as_view(
      template_name='accounts/password_reset.html'
    ),
    name='password_reset'
    ),

    path(
    'edit-performance/<int:performance_id>/',
    edit_performance,
    name='edit_performance'
),

path(
    'delete-performance/<int:performance_id>/',
    delete_performance,
    name='delete_performance'
),
]