from datetime import timedelta

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from audit.services import record_event
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
            record_event('login_failure', actor=user, record_type='user', record_id=user.pk)
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
                        record_event('login_success', actor=locked_user, record_type='user', record_id=locked_user.pk)
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
                record_event('login_failure', actor=user, record_type='user' if user else 'authentication',
                             record_id=user.pk if user else '')
                error = 'Invalid username or password'
    return render(request, 'accounts/login.html', {'error': error})


@require_http_methods(['POST'])
@login_required
def sign_out(request):
    actor = request.user
    record_event('logout', actor=actor, record_type='user', record_id=actor.pk)
    logout(request)  # Django flushes the session and invalidates its key.
    return redirect('login')


@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html', {'role': request.user.get_role_display()})


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
            user = form.save()
            record_event('user_create', actor=request.user, record_type='user', record_id=user.pk)
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
                updated_user = form.save()
                record_event('user_update', actor=request.user, record_type='user',
                             record_id=updated_user.pk)
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
        record_event('user_deactivate', actor=request.user, record_type='user', record_id=target.pk)
    return redirect('user-management')
