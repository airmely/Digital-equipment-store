from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from .forms import LoginForm, RegisterForm, UserProfileForm


def sign_up(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'registration/registration.html',
                      {'form': form})

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'Вы успешно зарегистрировались')
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'registration/registration.html',
                          {'form': form})


def logout_user(request):
    logout(request)
    return redirect('login')


def login_user(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(
            request=request,
            template_name='registration/login.html',
            context={'form': form}
        )

    elif request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Привет {username.title()}, Добро пожаловать!')
                return redirect('home')

        messages.error(request, f'Неправильное имя пользователя или пароль')
        return render(request, 'registration/login.html', {'form': form})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'registration/profile.html', {'form': form})
