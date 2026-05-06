# accounts/decorators.py

from django.core.exceptions import PermissionDenied
from functools import wraps


def admin_required(view_func):
    """
    Decorator that only lets Admins through.
    If a Technician tries to access it → 403 Forbidden.

    Usage:
        @login_required
        @admin_required
        def my_admin_only_view(request):
            ...
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Check if user has a profile and if they're an admin
        if hasattr(request.user, 'profile') and request.user.profile.is_admin:
            return view_func(request, *args, **kwargs)
        # If not → raise 403 Forbidden
        raise PermissionDenied
    return wrapper


def technician_or_admin_required(view_func):
    """
    Decorator that lets both Technicians and Admins through.
    Blocks users with no profile (shouldn't happen, but safety first!).
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if hasattr(request.user, 'profile'):
            return view_func(request, *args, **kwargs)
        raise PermissionDenied
    return wrapper