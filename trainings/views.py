from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required

from django.contrib import messages

from django.db.models import Q

from accounts.decorators import role_required

from core.utils import log_action

from .models import Training

from .forms import TrainingForm


# =========================================
# TRAINING LIST
# =========================================

@login_required
@role_required(['admin', 'coach', 'director'])
def training_list(request):

    query = request.GET.get('q')

    trainings = Training.objects.all()

    if query:

        trainings = trainings.filter(

            Q(session_title__icontains=query) |
            Q(training_type__icontains=query) |
            Q(trainer_name__icontains=query) |
            Q(status__icontains=query)

        )

    trainings = trainings.order_by('-training_date')

    completed_count = trainings.filter(
        status='Completed'
    ).count()

    missed_count = trainings.filter(
        status='Missed'
    ).count()

    scheduled_count = trainings.filter(
        status='Scheduled'
    ).count()

    return render(
        request,
        'trainings/training_list.html',
        {
            'trainings': trainings,
            'query': query,
            'completed_count': completed_count,
            'missed_count': missed_count,
            'scheduled_count': scheduled_count,
        }
    )


# =========================================
# ADD TRAINING
# =========================================

@login_required
@role_required(['admin', 'coach'])
def add_training(request):

    if request.method == 'POST':

        form = TrainingForm(request.POST)

        if form.is_valid():

            training = form.save()

            log_action(
                request.user,
                "TRAINING_CREATED",
                f"Training created: {training.session_title}"
            )

            messages.success(
                request,
                'Training session added successfully.'
            )

            return redirect('training_list')

    else:

        form = TrainingForm()

    return render(
        request,
        'trainings/add_training.html',
        {
            'form': form
        }
    )


# =========================================
# EDIT TRAINING
# =========================================

@login_required
@role_required(['admin', 'coach'])
def edit_training(request, training_id):

    training = get_object_or_404(
        Training,
        id=training_id
    )

    if request.method == 'POST':

        form = TrainingForm(
            request.POST,
            instance=training
        )

        if form.is_valid():

            form.save()

            log_action(
                request.user,
                "TRAINING_UPDATED",
                f"Training updated: {training.session_title}"
            )

            messages.success(
                request,
                'Training updated successfully.'
            )

            return redirect('training_list')

    else:

        form = TrainingForm(instance=training)

    return render(
        request,
        'trainings/edit_training.html',
        {
            'form': form,
            'training': training
        }
    )


# =========================================
# DELETE TRAINING
# =========================================

@login_required
@role_required(['admin'])
def delete_training(request, training_id):

    training = get_object_or_404(
        Training,
        id=training_id
    )

    if request.method == 'POST':

        log_action(
            request.user,
            "TRAINING_DELETED",
            f"Training deleted: {training.session_title}"
        )

        training.delete()

        messages.success(
            request,
            'Training deleted successfully.'
        )

        return redirect('training_list')

    return render(
        request,
        'training_list',
        {
            'training': training
        }
    )


# =========================================
# ARTIST VIEW
# =========================================

@login_required
@role_required(['artist'])
def my_trainings(request):

    query = request.GET.get('q')

    trainings = Training.objects.all()

    if query:

        trainings = trainings.filter(

            Q(session_title__icontains=query) |
            Q(training_type__icontains=query) |
            Q(status__icontains=query)

        )

    trainings = trainings.order_by('-training_date')

    context = {

        'trainings': trainings,

        'total_trainings': trainings.count(),

        'completed_trainings': trainings.filter(
            status='Completed'
        ).count(),

        'missed_trainings': trainings.filter(
            status='Missed'
        ).count(),

        'upcoming_trainings': trainings.filter(
            status='Scheduled'
        ).count(),

        'query': query
    }

    return render(
        request,
        'trainings/my_trainings.html',
        context
    )