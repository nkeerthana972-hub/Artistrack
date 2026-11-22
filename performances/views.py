from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.models import AuditLog
from .models import Performance
from .forms import PerformanceForm
from django.contrib import messages
from accounts.decorators import role_required
from django.db.models import Count
from core.utils import log_action
from django.utils.timezone import now

@login_required
@role_required(['admin', 'director', 'coach'])
def performance_list(request):

    performances = Performance.objects.all()

    return render(
        request,
        'performances/performance_list.html',
        {
            'performances': performances,
            'today': now().date()
        }
    )


@login_required
@role_required(['admin', 'coach'])
def add_performance(request):

    if request.method == 'POST':

        form = PerformanceForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(request,'Performance record added successfully.')

            log_action(
            request.user,
            "PERFORMANCE_CREATED",
            "Performance record created"
            )

            return redirect('performance_list')

    else:

        form = PerformanceForm()

    return render(
        request,
        'performances/add_performance.html',
        {
            'form': form
        }
    )


@login_required
@role_required(['artist'])
def my_performances(request):

    artist = getattr(request.user, 'artist', None)

    if not artist:
        return redirect('/dashboard/')

    performances = Performance.objects.filter(
        artist=artist
    ).order_by('-performance_date')

    # STATISTICS

    total_performances = performances.count()

    average_score = 0

    if total_performances > 0:

        total_score = sum(
            performance.score
            for performance in performances
        )

        average_score = round(
            total_score / total_performances,
            1
        )

    highest_score = 0

    if performances.exists():

        highest_score = max(
            performance.score
            for performance in performances
        )

    recent_performances = performances[:3]

    context = {

        'performances': performances,

        'recent_performances': recent_performances,

        'total_performances': total_performances,

        'average_score': average_score,

        'highest_score': highest_score,
    }

    return render(
        request,
        'performances/my_performances.html',
        context
    )

@login_required
def edit_performance(request, performance_id):

    performance = get_object_or_404(
        Performance,
        id=performance_id
    )

    if request.user.role not in ['admin', 'coach']:
        messages.error(request, 'Access denied.')
        return redirect('/performances/')

    form = PerformanceForm(
        request.POST or None,
        instance=performance
    )

    if form.is_valid():

        form.save()

        messages.success(
            request,
            'Performance updated successfully.'
        )

        return redirect('/performances/')

    return render(
        request,
        'performances/edit_performance.html',
        {'form': form}
    )

@login_required
def delete_performance(request, performance_id):

    performance = get_object_or_404(
        Performance,
        id=performance_id
    )

    if request.user.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('/performances/')

    if request.method == 'POST':

        performance.delete()

        messages.success(
            request,
            'Performance deleted successfully.'
        )

        return redirect('/performances/')

    return render(
        request,
        'performance_list',
        {'performance': performance}
        
    )
