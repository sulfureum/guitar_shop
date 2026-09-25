from django.shortcuts import render, redirect
from . forms import LoginForm, RegistrationForm
from django.contrib.auth import login, logout

def user_logout(request):
    logout(request)
    return redirect('home')


def login_page(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()

    ctx = {
        'form': form
    }
    return render(request, 'users/login.html', ctx)

def registration_page(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:home')
    else:
        form = RegistrationForm()

    ctx = {
        'form': form
    }
    return render(request, 'users/registration.html', ctx)
