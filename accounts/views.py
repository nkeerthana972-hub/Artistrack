from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from accounts.models import AuditLog
from .forms import RegisterForm
from artists.models import Artist
from axes.models import AccessLog
from django.contrib.admin.views.decorators import staff_member_required
from core.utils import log_action
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.utils.timezone import now
from accounts.models import AuditLog, CustomUser
from accounts.decorators import role_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib import messages
from .forms import LoginForm
from django.core.mail import send_mail
from django.conf import settings
import random
from django.contrib.auth import update_session_auth_hash
from .forms import CustomPasswordChangeForm
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import (
    urlsafe_base64_encode,
    urlsafe_base64_decode
)
from django.utils.encoding import (
    force_bytes,
    force_str
)

from .forms import ForgotPasswordForm
from django.contrib.auth import (
    authenticate,
    login,
    logout
)

from .models import (
    CustomUser,
    AuditLog,
    AdminOTP
)

from .forms import (
    RegisterForm,
    LoginForm,
    OTPForm,
    StaffCreateForm
)

import random

from .models import AdminOTP

def register_view(request):

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)             
            user.role ='artist'
            user.save()
            Artist.objects.create(user=user,email=user.email)
            log_action(user,"REGISTER"," New artist registered ")

            messages.success(
                request,
                'Artist account created successfully.'
            )

            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('dashboard')

    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})



def login_view(request):

    if request.method == 'POST':

        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(
                request=request,
                username=username,
                password=password
            )

            if user is not None:

                # ADMIN 2FA CHECK
                if user.role == 'admin':
                    # GENERATE 6 DIGIT OTP
                    otp = str(random.randint(100000, 999999))

                    AdminOTP.objects.filter(
                    user=user
                    ).delete()

                    # SAVE OTP IN DATABASE
                    AdminOTP.objects.create(
                        user=user,
                        otp=otp
                    )
                    # SEND OTP EMAIL
                    send_mail(
                        subject='ArtisTrack — Admin Login OTP',
                        message=(
                            f"Hello {user.username},\n\n"
                            f"A login attempt was made to your ArtisTrack administrator account.\n\n"
                            f"Your One-Time Password (OTP) is:\n\n"
                            f"    {otp}\n\n"
                            f"This OTP is valid for 5 minutes. Do not share it with anyone.\n\n"
                            f"If you did not request this, please contact your system administrator immediately.\n\n"
                            f"Regards,\n"
                            f"ArtisTrack System"
                        ),
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[user.email],
                        fail_silently=False,
                    )

                    # SAVE USER ID IN SESSION
                    request.session['otp_user_id'] = user.id

                    messages.info(
                        request,
                        "OTP sent to your email."
                    )

                    return redirect('admin_otp_verify')

                # NORMAL LOGIN FOR OTHER USERS
                login(request, user)

                log_action(
                    user,
                    "LOGIN_SUCCESS",
                    "User logged in successfully"
                )

                return redirect('dashboard')

        # SHOW INVALID CREDENTIAL MESSAGE
        if form.errors.get('captcha'): 
            messages.error( request, "Invalid CAPTCHA." ) 
        else: 
            messages.error( request, "Invalid username or password." )

    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {
        'form': form
    })


def logout_view(request):
    if request.user.is_authenticated:
        log_action(request.user, "LOGOUT", "User logged out")
    logout(request)
    return redirect('login')


@login_required
@role_required(['admin'])
def admin_panel(request):

    total_users = CustomUser.objects.count()
    total_admins = CustomUser.objects.filter(role='admin').count()
    total_directors = CustomUser.objects.filter(role='director').count()
    total_coaches = CustomUser.objects.filter(role='coach').count()
    total_artists = CustomUser.objects.filter(role='artist').count()

    logs = AuditLog.objects.select_related('user').order_by('-timestamp')
    paginator = Paginator(logs, 5)
    page_obj = paginator.get_page(1)

    return render(request, 'admin_panel/admin_panel.html', {
        'logs': page_obj,
        'total_users': total_users,
        'total_admins': total_admins,
        'total_directors': total_directors,
        'total_coaches': total_coaches,
        'total_artists': total_artists,
    })


@login_required
@role_required(['admin'])
def filter_logs(request):

    q = request.GET.get('q', '')
    page = request.GET.get('page', 1)

    logs = AuditLog.objects.select_related('user').order_by('-timestamp')

    if q:
        logs = logs.filter(
            user__username__icontains=q
        ) | logs.filter(
            action__icontains=q
        )

    paginator = Paginator(logs, 5)
    page_obj = paginator.get_page(page)

    html = render_to_string('admin_panel/log_table.html', {
        'logs': page_obj
    })

    pagination_html = render_to_string('admin_panel/pagination.html', {
        'logs': page_obj
    })

    return JsonResponse({
        'html': html,
        'pagination': pagination_html
    })

def admin_otp_verify(request):

    user_id = request.session.get('otp_user_id')

    if not user_id:
        return redirect('login')

    user = CustomUser.objects.get(id=user_id)

    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():

            otp_entered = form.cleaned_data['otp']
            otp_record = AdminOTP.objects.filter(
                user=user
            ).last()

            if otp_record:

                if otp_record.is_expired():
                    messages.error(
                        request,
                        'OTP expired.'
                    )

                elif otp_record.otp == otp_entered:
                    AdminOTP.objects.filter(
                        user=user
                    ).delete()

                    login(
                    request,
                    user,
                    backend='django.contrib.auth.backends.ModelBackend'
                    )
                    del request.session['otp_user_id']
                    log_action(
                        user,
                        "ADMIN_LOGIN_SUCCESS",
                        "Admin logged in with OTP"
                    )

                    return redirect('dashboard')

                else:

                    messages.error(
                        request,
                        'Invalid OTP.'
                    )

    else:
        form = OTPForm()

    return render(
        request,
        'accounts/admin_otp_verify.html',
        {
            'form': form
        }
    )

@login_required
@role_required(['admin'])
def create_staff(request):

    if request.method == 'POST':

        form = StaffCreateForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            # EXTRA SECURITY
            if user.role == 'admin':

                messages.error(
                    request,
                    'Admin account creation is restricted.'
                )

                return redirect('create_staff')

            user.save()

            if user.role == 'coach':

                messages.success(
                    request,
                    'Coach account created successfully.'
                )

                log_action(
                request.user,
                "COACH_CREATED",
                f"{user.role} account created for {user.username}"
                )

            elif user.role == 'director':

                messages.success(
                    request,
                    'Director account created successfully.'
                )

                log_action(
                request.user,
                "DIRECTOR_CREATED",
                f"{user.role} account created for {user.username}"
            )



            return redirect('admin_panel')

    else:

        form = StaffCreateForm()

    return render(
        request,
        'accounts/create_staff.html',
        {
            'form': form
        }
    )

def resend_admin_otp(request):

    user_id = request.session.get(
        'otp_user_id'
    )

    if not user_id:

        messages.error(
            request,
            'Session expired. Please login again.')
        return redirect('login')

    user = CustomUser.objects.get(
        id=user_id
    )
    AdminOTP.objects.filter(
    user=user
    ).delete()

    otp = str(
        random.randint(100000, 999999)
    )
    AdminOTP.objects.create(
        user=user,
        otp=otp
    )
    send_mail(
        subject='ArtisTrack — Admin Login OTP',
        message=(
            f"Hello {user.username},\n\n"
            f"A login attempt was made to your ArtisTrack administrator account.\n\n"
            f"Your One-Time Password (OTP) is:\n\n"
            f"    {otp}\n\n"
            f"This OTP is valid for 5 minutes. Do not share it with anyone.\n\n"
            f"If you did not request this, please contact your system administrator immediately.\n\n"
            f"Regards,\n"
            f"ArtisTrack System"
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )

    messages.success(
        request,
        'A new OTP has been sent.'
    )

    return redirect('admin_otp_verify')

@login_required
def change_password(request):

    if request.method == 'POST':

        form = CustomPasswordChangeForm(
            request.user,
            request.POST
        )

        if form.is_valid():

            user = form.save()

            update_session_auth_hash(
                request,
                user
            )

            log_action(
                request.user,
                "PASSWORD_CHANGED",
                "User changed password"
            )

            messages.success(
                request,
                "Password updated successfully."
            )

            return redirect(
                'dashboard'
            )

    else:

        form = CustomPasswordChangeForm(
            request.user
        )

    return render(
        request,
        'accounts/change_password.html',
        {
            'form': form
        }
    )

def forgot_password(request):

    if request.method == 'POST':

        form = ForgotPasswordForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data['username']

            try:

                user = CustomUser.objects.get(
                    username=username
                )

                uid = urlsafe_base64_encode(
                    force_bytes(user.pk)
                )

                token = default_token_generator.make_token(
                    user
                )

                reset_link = request.build_absolute_uri(
                    f"/reset-password/{uid}/{token}/"
                )

                send_mail(
                    subject='ArtisTrack — Password Reset Request',
                    message=(
                        f"Hello {user.username},\n\n"
                        f"A password reset was requested for your ArtisTrack account.\n\n"
                        f"Click the link below to reset your password:\n\n"
                        f"    {reset_link}\n\n"
                        f"This link will expire shortly. If you did not request this, ignore this email.\n\n"
                        f"Regards,\n"
                        f"ArtisTrack System"
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],   # changed from [user.email]
                    fail_silently=False
                )

                log_action(
                    user,
                    "PASSWORD_RESET_REQUESTED",
                    f"Password reset requested for {user.username}"
                )

                messages.success(
                    request,
                    'Reset link sent.'
                )

                return redirect('login')

            except CustomUser.DoesNotExist:

                messages.error(
                    request,
                    'Username not found.'
                )

    else:

        form = ForgotPasswordForm()
        print(form.errors)

    return render(
        request,
        'accounts/forgot_password.html',
        {
            'form': form
        }
    )

def reset_password(
    request,
    uidb64,
    token
):

    try:

        uid = force_str(
            urlsafe_base64_decode(uidb64)
        )

        user = CustomUser.objects.get(pk=uid)

    except Exception:

        user = None

    if (
        user is None or
        not default_token_generator.check_token(
            user,
            token
        )
    ):
        

        messages.error(
            request,
            "Invalid reset link."
        )

        return redirect('login')

    if request.method == 'POST':

        form = SetPasswordForm(
            user,
            request.POST
        )

        if form.is_valid():

            form.save()

            log_action(
                user,
                "PASSWORD_RESET_COMPLETED",
                "Password reset completed"
            )

            messages.success(
                request,
                'Password updated successfully.'
            )

            return redirect('login')

    else:

        form = SetPasswordForm(user)

    return render(
        request,
        'accounts/reset_password.html',
        {
            'form': form
        }
    )