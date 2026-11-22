from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.models import AuditLog
from .models import Injury
from .forms import InjuryForm
from django.contrib import messages
from accounts.decorators import role_required
from core.utils import log_action

@login_required
@role_required(['admin', 'director', 'coach'])
def injury_list(request):

    injuries = Injury.objects.all()

    return render(request, 'injuries/injury_list.html', {
        'injuries': injuries
    })


@login_required
@role_required(['admin', 'coach'])
def add_injury(request):

    if request.method == 'POST':

        form = InjuryForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(request,'Injuries record added successfully.')

            log_action(
            request.user,
            "INJURY_CREATED",
            "Injury record created"
            )

            return redirect('injury_list')

    else:
        form = InjuryForm()

    return render(request, 'injuries/add_injury.html', {
        'form': form
    })

@login_required
@role_required(['artist'])
def my_injuries(request):

    artist = getattr(request.user, 'artist', None)

    if not artist:
        return redirect('/dashboard/')

    injuries = Injury.objects.filter(
        artist=artist
    )

    return render(request,
        'injuries/my_injuries.html',
        {
            'injuries': injuries
        }
    )




@login_required
@role_required(['admin', 'coach'])
def edit_injury(request, injury_id):

    injury = get_object_or_404(
        Injury,
        id=injury_id
    )

    # RBAC protection
    if request.user.role not in ['admin', 'coach']:
        messages.error(
            request,
            "You do not have permission to edit injuries."
        )
        return redirect('/injuries/')

    if request.method == 'POST':

        form = InjuryForm(
            request.POST,
            request.FILES,
            instance=injury
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Injury updated successfully."
            )

            return redirect('/injuries/')

    else:

        form = InjuryForm(instance=injury)

    return render(
        request,
        'injuries/edit_injury.html',
        {
            'form': form,
            'injury': injury
        }
    )

@login_required
@role_required(['admin'])
def delete_injury(request, injury_id):

    injury = get_object_or_404(
        Injury,
        id=injury_id
    )

    # RBAC protection
    if request.user.role != 'admin':

        messages.error(
            request,
            "You do not have permission to delete injuries."
        )

        return redirect('/injuries/')

    injury.delete()

    messages.success(
        request,
        "Injury deleted successfully."
    )

    return redirect('injury_list')