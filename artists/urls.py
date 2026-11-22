from django.urls import path

from .views import (
    artist_list,
    add_artist,
    edit_artist,
    delete_artist,
    my_profile,
    edit_my_profile
)

urlpatterns = [

    path('artists/', artist_list, name='artist_list'),

    path('add-artist/', add_artist, name='add_artist'),

    path('edit-artist/<int:pk>/', edit_artist, name='edit_artist'),

    path('delete-artist/<int:pk>/', delete_artist, name='delete_artist'),

    path('my-profile/', my_profile, name='my_profile'),

    path('edit-my-profile/',edit_my_profile,name='edit_my_profile'),
]