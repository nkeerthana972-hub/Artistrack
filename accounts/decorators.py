from functools import wraps
from django.shortcuts import redirect
from django.http import HttpResponseForbidden


def role_required(allowed_roles=None):

    if allowed_roles is None:
        allowed_roles = []

    def decorator(view_func):

        @wraps(view_func)
        def wrapper_func(request, *args, **kwargs):

            if not request.user.is_authenticated:
                return redirect('/login/')

            # optional safety: superuser bypass
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            # handle missing role safely
            user_role = getattr(request.user, "role", None)

            if user_role in allowed_roles:
                return view_func(request, *args, **kwargs)

            return HttpResponseForbidden("You are not authorized to view this page.")

        return wrapper_func

    return decorator