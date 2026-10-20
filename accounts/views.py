from datetime import timedelta

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from .forms import AccountCreationForm, AccountUpdateForm
from .models import User


LOCKOUT_ATTEMPTS = 5
LOCKOUT_DURATION = timedelta(minutes=15)


@require_http_methods(['GET', 'POST'])
def sign_in(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = User.objects.filter(username__iexact=username, is_active=True).first()
        if user and user.is_locked():
            error = 'Invalid username or password'
        else:
            authenticated = authenticate(request, username=username, password=password)
            if authenticated:
                with transaction.atomic():
                    locked_user = User.objects.select_for_update().get(pk=authenticated.pk)
                    if locked_user.is_locked():
                        error = 'Invalid username or password'
                    else:
                        locked_user.failed_attempts = 0
                        locked_user.locked_until = None
                        locked_user.save(update_fields=['failed_attempts', 'locked_until'])
                        login(request, locked_user)
                        return redirect('dashboard')
            else:
                if user:
                    with transaction.atomic():
                        locked_user = User.objects.select_for_update().get(pk=user.pk)
                        locked_user.failed_attempts += 1
                        if locked_user.failed_attempts >= LOCKOUT_ATTEMPTS:
                            locked_user.locked_until = timezone.now() + LOCKOUT_DURATION
                            locked_user.failed_attempts = 0
                        locked_user.save(update_fields=['failed_attempts', 'locked_until'])
                error = 'Invalid username or password'
    return render(request, 'accounts/login.html', {'error': error})


@require_http_methods(['POST'])
@login_required
def sign_out(request):
    logout(request)  # Django flushes the session and invalidates its key.
    return redirect('login')


@login_required
def dashboard(request):
    role_templates = {
        User.Role.ADMIN: 'accounts/dashboard_admin.html',
        User.Role.WARDEN: 'accounts/dashboard_warden.html',
        User.Role.STUDENT: 'accounts/dashboard_student.html',
    }
    template = role_templates.get(request.user.role, 'accounts/dashboard_student.html')
    return render(request, template, {'role': request.user.get_role_display()})


def admin_role_required(view):
    def wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(request.get_full_path())
        if request.user.role != User.Role.ADMIN:
            return HttpResponseForbidden('Access denied')
        return view(request, *args, **kwargs)
    wrapped.__name__ = view.__name__
    wrapped.__doc__ = view.__doc__
    return wrapped


@login_required
@admin_role_required
@require_http_methods(['GET', 'POST'])
def user_management(request):
    if request.method == 'POST':
        form = AccountCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user-management')
    else:
        form = AccountCreationForm()
    users = User.objects.order_by('username')
    return render(request, 'accounts/user_management.html', {'form': form, 'users': users})


@login_required
@admin_role_required
@require_http_methods(['GET', 'POST'])
def update_user(request, user_id):
    target = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = AccountUpdateForm(request.POST, instance=target)
        if form.is_valid():
            if form.has_changed():
                form.save()
            return redirect('user-management')
    else:
        form = AccountUpdateForm(instance=target)
    return render(request, 'accounts/user_update.html', {'form': form, 'account': target})


@login_required
@admin_role_required
@require_http_methods(['POST'])
def deactivate_user(request, user_id):
    target = User.objects.get(pk=user_id)
    if target.pk == request.user.pk:
        return HttpResponseForbidden('You cannot deactivate your own account')
    if target.is_active:
        target.is_active = False
        target.save(update_fields=['is_active'])
    return redirect('user-management')
