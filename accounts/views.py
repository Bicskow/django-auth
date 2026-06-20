from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpRequest
from django.contrib import messages

from allauth.account.models import EmailAddress
from allauth.account.utils import setup_user_email
from allauth.account.internal.flows.email_verification import send_verification_email_for_user

from .forms import RegisterForm

def login_view(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            email_verified = EmailAddress.objects.filter(
                user=user, verified=True
            ).exists()

            if email_verified:
                messages.success(request, "Successfully logged in!")
                login(request, user)
                return redirect('home')
            else:
                messages.error(
                    request,
                    "Please verify your email address before logging in."
                )
                return redirect('login')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "login.html")

@login_required
def home(request):
    return render(request, 'home.html')

@require_POST
@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')


def registration(request: HttpRequest):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            setup_user_email(request, user, [])
            send_verification_email_for_user(request, user)

            messages.success(
                request,
                "Registration successful! Please check your email to verify your account."
            )
            return redirect('email-verification-sent')
        else:
            messages.error(request, 'Please correct the errors below.')

    else:
        form = RegisterForm()

    return render(request, 'registration.html', {"form": form})


def email_verification_sent(request: HttpRequest):
    return render(request, "verification_sent.html")
