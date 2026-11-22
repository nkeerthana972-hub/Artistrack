from django.urls import path

from . import views


urlpatterns = [

    path(
        'trainings/',
        views.training_list,
        name='training_list'
    ),

    path(
        'add-training/',
        views.add_training,
        name='add_training'
    ),

    path(
        'edit-training/<int:training_id>/',
        views.edit_training,
        name='edit_training'
    ),

    path(
        'delete-training/<int:training_id>/',
        views.delete_training,
        name='delete_training'
    ),

    path(
        'my-trainings/',
        views.my_trainings,
        name='my_trainings'
    ),

]