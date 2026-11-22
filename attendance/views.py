from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.models import AuditLog
from .models import Attendance
from .forms import AttendanceForm
from django.contrib import messages
from accounts.decorators import role_required
from django.db.models import Count
from django.utils.timezone import now
from core.utils import log_action

@login_required
@role_required(['admin', 'coach', 'director'])
def attendance_list(request):

    attendance_records = Attendance.objects.select_related(
        'artist',
        'training'
    ).order_by('-date')

    total_records = attendance_records.count()

    present_count = attendance_records.filter(
        status='present'
    ).count()

    absent_count = attendance_records.filter(
        status='absent'
    ).count()

    context = {

        'attendance_records': attendance_records,
        'total_records': total_records,
        'present_count': present_count,
        'absent_count': absent_count,

    }

    return render(
        request,
        'attendance/attendance_list.html',
        context
    )


@login_required
@role_required(['admin', 'coach'])
def add_attendance(request):

    if request.method == 'POST':

        form = AttendanceForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(request,'Attendance record added successfully.')

            log_action(
            request.user,
            "ATTENDANCE_CREATED",
            "Attendance record created"
            )

            return redirect('attendance_list')

    else:
        form = AttendanceForm()

    return render(request, 'attendance/add_attendance.html', {
        'form': form
    })

@login_required
@role_required(['artist'])
def my_attendance(request):

    artist = getattr(request.user, 'artist', None)

    if not artist:
        return redirect('/dashboard/')

    attendance_records = Attendance.objects.filter(
        artist=artist
    ).order_by('-date')

    # STATISTICS

    total_records = attendance_records.count()

    present_count = attendance_records.filter(
        status='present'
    ).count()

    absent_count = attendance_records.filter(
        status='absent'
    ).count()


    attendance_percentage = 0

    if total_records > 0:

        attendance_percentage = round(
            (present_count / total_records) * 100,
            1
        )

    # RECENT ATTENDANCE

    recent_attendance = attendance_records[:5]

    context = {

        'attendance_records': attendance_records,

        'recent_attendance': recent_attendance,

        'total_records': total_records,

        'present_count': present_count,

        'absent_count': absent_count,

        'attendance_percentage': attendance_percentage,
    }

    return render(
        request,
        'attendance/my_attendance.html',
        context
    )

@login_required
@role_required(['admin', 'coach'])
def edit_attendance(request, pk):

    attendance = Attendance.objects.get(id=pk)

    form = AttendanceForm(
        request.POST or None,
        instance=attendance
    )

    if form.is_valid():

        form.save()

        log_action(
        request.user,
        "ATTENDANCE_UPDATED",
        f"Attendance ID {attendance.id} updated"
        )

        messages.success(
            request,
            'Attendance updated successfully.'
        )

        return redirect('attendance_list')

    return render(

        request,

        'attendance/edit_attendance.html',

        {

            'form': form

        }

    )

@login_required
@role_required(['admin', 'coach'])
def delete_attendance(request, pk):

    attendance = get_object_or_404(Attendance, pk=pk)

    attendance.delete()

    messages.success(
        request,
        'Attendance record deleted successfully.'
    )

    return redirect('attendance_list')