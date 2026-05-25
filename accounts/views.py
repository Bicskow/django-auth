from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpRequest
from django.contrib import messages

from .forms import RegisterForm

def login_view(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        user = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=user, password=password)

        if user != None:
            messages.success(
                request,
                "Successfully logged in!"
            )

            login(request, user)
            return redirect('home')
        else:
            messages.error(
                request,
                "Invalid username or password."
            )

    return render(request, "login.html")

@login_required
def home(request):
    return render(request, 'home.html')

@require_POST
@login_required
def logout_view(request):
    logout(request)

    messages.info(
        request,
        "You have been logged out."
    )
    return redirect('login')


def registration(request: HttpRequest):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request,user)

            messages.success(
                request,
                "Successful registration!"
            )
            messages.success(
                request,
                "Successfully logged in!"
            )

            return redirect('home')
        else:
            messages.error(
            request,
            form.errors
        )        
        
    else:
        form = RegisterForm()
        
        
    return render(request, 'registration.html', {"form": form})
