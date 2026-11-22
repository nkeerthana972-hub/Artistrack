from django.urls import path

from .views import (
    attendance_list,
    add_attendance,
    my_attendance,
    edit_attendance,
    delete_attendance
)

urlpatterns = [

    path(
        'attendance/',
        attendance_list,
        name='attendance_list'
    ),

    path(
        'add-attendance/',
        add_attendance,
        name='add_attendance'
    ),

    path(
    'my-attendance/',
    my_attendance,
    name='my_attendance'
    ),

    path(
    'edit-attendance/<int:pk>/',
    edit_attendance,
    name='edit_attendance'
    ),

    path(
    'delete-attendance/<int:pk>/',
    delete_attendance,
    name='delete_attendance'
),
]