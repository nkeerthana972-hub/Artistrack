from django.urls import path

from .views import (
    injury_list,
    add_injury,
    my_injuries,
    edit_injury,
    delete_injury
)

urlpatterns = [

    path(
        'injuries/',
        injury_list,
        name='injury_list'
    ),

    path(
        'add-injury/',
        add_injury,
        name='add_injury'
    ),

    path(
    'my-injuries/',
    my_injuries,
    name='my_injuries'
),

    path(
        'edit-injury/<int:injury_id>/',
        edit_injury,
        name='edit_injury'
    ),

    path(
        'delete-injury/<int:injury_id>/',
        delete_injury,
        name='delete_injury'
    ),
]
