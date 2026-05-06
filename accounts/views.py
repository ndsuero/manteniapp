# accounts/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from .forms import RegisterForm, ProfileEditForm
from .models import Profile
from .decorators import admin_required


def register(request):
    """Registration page — anyone can sign up."""
    if request.user.is_authenticated:
        return redirect('tickets:ticket_list')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log them in automatically after signup
            login(request, user)
            messages.success(
                request,
                f'🎉 Welcome to ManteniApp, {user.username}!'
            )
            return redirect('tickets:ticket_list')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile_view(request):
    """View your own profile."""
    return render(request, 'accounts/profile.html', {
        'profile': request.user.profile
    })


@login_required
def profile_edit(request):
    """Edit your own profile."""
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileEditForm(
            request.POST,
            instance=profile,
            user=request.user
        )
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        form = ProfileEditForm(instance=profile, user=request.user)

    return render(request, 'accounts/profile_edit.html', {'form': form})


@login_required
@admin_required
def user_list(request):
    """
    Admin only — manage all users.
    Technicians get a 403 error if they try to visit this.
    """
    users = User.objects.all().select_related('profile').order_by('username')
    return render(request, 'accounts/user_list.html', {'users': users})


@login_required
@admin_required
def promote_user(request, user_id):
    """Admin only — toggle a user between Admin and Technician role."""
    user = get_object_or_404(User, id=user_id)

    # Safety check — don't demote yourself!
    if user == request.user:
        messages.error(request, "❌ You can't change your own role!")
        return redirect('accounts:user_list')

    if request.method == 'POST':
        profile = user.profile
        if profile.is_admin:
            profile.role = Profile.Role.TECHNICIAN
            messages.success(
                request,
                f'🔧 {user.username} is now a Technician.'
            )
        else:
            profile.role = Profile.Role.ADMIN
            messages.success(
                request,
                f'⭐ {user.username} is now an Administrator.'
            )
        profile.save()

    return redirect('accounts:user_list')