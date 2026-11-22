from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from artists.models import Artist
from injuries.models import Injury
from attendance.models import Attendance
from performances.models import Performance
from django.http import HttpResponseForbidden
from accounts.models import AuditLog, CustomUser
from django.shortcuts import render
from accounts.decorators import role_required
from artists.models import Artist
from performances.models import Performance
from trainings.models import Training
from attendance.models import Attendance

from django.db.models import Count



from django.shortcuts import render

from artists.models import Artist
from attendance.models import Attendance
from performances.models import Performance
from injuries.models import Injury
from trainings.models import Training


def home(request):

    total_artists = Artist.objects.count()

    total_performances = Performance.objects.count()

    total_trainings = Training.objects.count()

    active_injuries = Injury.objects.filter(
        status='Active'
    ).count()

    recent_trainings = Training.objects.order_by(
        '-training_date'
    )[:4]

    context = {

        'total_artists': total_artists,

        'total_performances': total_performances,

        'total_trainings': total_trainings,

        'active_injuries': active_injuries,

        'recent_trainings': recent_trainings,
    }

    return render(
        request,
        'home.html',
        context
    )

@login_required
def dashboard(request):

    User = get_user_model()

    recent_users = User.objects.order_by('-date_joined')[:5]

    total_attendance = Attendance.objects.count()

    present_count = Attendance.objects.filter(
        status='present'
    ).count()

    absent_count = Attendance.objects.filter(
        status='absent'
    ).count()

    attendance_percentage = 0

    if total_attendance > 0:
        attendance_percentage = round(
            (present_count / total_attendance) * 100,
            1
        )

    context = {

        # Existing dashboard stats
        'artist_count': Artist.objects.count(),
        'injury_count': Injury.objects.count(),
        'attendance_count': total_attendance,
        'performance_count': Performance.objects.count(),
        'recent_users': recent_users,

        # Director statistics
        'total_trainings': Training.objects.count(),
        'present_count': present_count,
        'absent_count': absent_count,
        'attendance_percentage': attendance_percentage,
    }

    return render(
        request,
        'dashboard/dashboard.html',
        context
    )