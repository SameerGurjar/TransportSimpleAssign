from django.shortcuts import render, redirect
from django.conf import settings
from .forms import UserLoginForm, UserRegisterForm
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse
# Create your views here.

User = settings.AUTH_USER_MODEL


def login_user(request):
    if request.user.is_authenticated:
        return redirect(reverse('post:home'))

    if request.method == 'POST':
        form = UserLoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            login(request, user)

            redirect_url = request.GET.get('next')
            if redirect_url is not None:
                return redirect(redirect_url)
            return redirect(reverse('post:home'))
        else:
            context = {
                'form': form
            }
            return render(request, "accounts/login.html", context)
    else:
        form = UserLoginForm(request)
        redirect_url = request.GET.get('next')
        if redirect_url is not None:
            context = {
                'form': form,
                'info': "Action Requires Login"
            }
        else:
            context = {
                'form': form
            }
        return render(request, "accounts/login.html", context)


def register_user(request):
    if request.user.is_authenticated:
        return redirect(reverse('post:home'))

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            form.save()
            login(request, user)
            return redirect(reverse('post:home'))
        else:
            context = {
                'form': form
            }
            return render(request, 'accounts/register.html', context)
    else:
        form = UserRegisterForm()
        context = {
            'form': form
        }
        return render(request, 'accounts/register.html', context)


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect(reverse('post:home'))
