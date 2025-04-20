from django.http import HttpResponseForbidden
from django.shortcuts import redirect


def login_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if "user_id" not in request.session:
            return redirect("authorization")
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def role_required(*roles):
    def decorator(view_func):
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if request.session["user_role"] not in roles:
                return HttpResponseForbidden("Доступ запрещен")
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator
