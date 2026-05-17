from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpRequest

def login_view(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect("home")

    error = None

    if request.method == "POST":
        user = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=user, password=password)

        if user != None:
            login(request, user)
            return redirect('home')
        else:
            error = "Invalid username or password"

    return render(request, "login.html", {"error": error})

@login_required
def home(request):
    return render(request, 'home.html')

@require_POST
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
