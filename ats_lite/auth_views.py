from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages


def login_view(request):
    # If already logged in, go straight to jobs
    if request.user.is_authenticated:
        return redirect('job_list')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Respect 'next' param (e.g., after being redirected from protected page)
            next_url = request.GET.get('next', 'job_list')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    return render(request, 'auth/login.html', {'form': form})


def register_view(request):
    #Handle new user registration
    if request.user.is_authenticated:
        return redirect('job_list')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Auto-login after registration
            login(request, user)
            messages.success(request, f'Welcome, {user.username}! Account created.')
            return redirect('job_list')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = UserCreationForm()

    return render(request, 'auth/register.html', {'form': form})
