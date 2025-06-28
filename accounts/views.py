from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required
from .forms import AccountUpdateForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from checkout.models import CheckoutOrder

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('core:home')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('core:home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('core:home')

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')

@login_required
def order_history_view(request):
    orders = CheckoutOrder.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'accounts/order_history.html', {'orders': orders})

@login_required
def order_detail_view(request, order_id):
    try:
        order = CheckoutOrder.objects.get(id=order_id, user=request.user)
    except CheckoutOrder.DoesNotExist:
        raise Http404("Order not found.")

    return render(request, 'accounts/order_detail.html', {'order': order})

@login_required
def update_email_view(request):
    if request.method == 'POST':
        new_email = request.POST.get('email')
        if new_email:
            request.user.email = new_email
            request.user.save()
            messages.success(request, 'Email updated successfully.')
    return redirect('accounts:profile')


@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password was successfully updated.")
            return redirect('accounts:profile')
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'accounts/change_password.html', {'form': form})

@login_required
def account_detail_view(request):
    user = request.user
    profile_form = AccountUpdateForm(instance=user)
    password_form = PasswordChangeForm(user)
    
    if request.method == 'POST':
        if 'update_profile' in request.POST:
            profile_form = AccountUpdateForm(request.POST, instance=user)
            if profile_form.is_valid() and password_form.is_valid():
                profile_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your details were updated successfully.")
            return redirect('accounts:account_detail')
        elif 'change_password' in request.POST:
            password_form = PasswordChangeForm(user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Your password was successfully updated.")
                return redirect('accounts:account_detail')
            else:
                messages.error(request, "Password does not meet criteria, please try again.")
                return redirect('accounts:account_detail')

    return render(request, 'accounts/account_detail.html', {
        'profile_form': profile_form,
        'password_form': password_form
    })