from django.shortcuts import redirect
from django.contrib import messages
from django.conf import settings
import time
from django.http import HttpResponseForbidden
import re

class SessionTimeoutMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.user.is_authenticated:

            current_time = int(time.time())

            last_activity = request.session.get(
                'last_activity',
                current_time
            )

            timeout = settings.SESSION_COOKIE_AGE

            if current_time - last_activity > timeout:

                request.session.flush()

                messages.warning(
                    request,
                    'Your session expired due to inactivity. Please login again.'
                )

                return redirect('/login/')

            request.session['last_activity'] = current_time

        response = self.get_response(request)

        return response
    
# =========================================
# SQL INJECTION PROTECTION MIDDLEWARE
# =========================================

class SQLInjectionProtectionMiddleware:

    SQL_PATTERNS = [
        r"(\%27)|(\')|(\-\-)|(\%23)|(#)",
        r"(\bOR\b|\bAND\b).*=.*",
        r"UNION\s+SELECT",
        r"DROP\s+TABLE",
        r"INSERT\s+INTO",
        r"DELETE\s+FROM",
        r"UPDATE\s+.*SET",
        r"SELECT\s+\*",
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        data = ""
        # Check GET data
        for key, value in request.GET.items():
            data += f"{key} {value} "
        # Check POST data
        for key, value in request.POST.items():
            data += f"{key} {value} "
        # Detect SQL Injection
        for pattern in self.SQL_PATTERNS:

            if re.search(pattern, data, re.IGNORECASE):

                return HttpResponseForbidden(
                    "Potential SQL Injection attack detected."
                )
        response = self.get_response(request)
        return response