from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages

from .forms import EmailLoginForm, RegisterForm

def login_view(request):
    if request.method == "POST":
        form = EmailLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            next_url = request.POST.get("next", "")

            try:
                user = User.objects.get(Q(email=email))
            except User.DoesNotExist:
                messages.error(request, "No existe un usuario con ese email.")
                return render(request, "login.html", {"form": form})

            user_auth = authenticate(username=user.username, password=password)
            if user_auth:
                login(request, user_auth)
                messages.success(request, "Inicio de sesión exitoso.")
                return redirect(next_url or "core:job_list")
            else:
                messages.error(request, "Contraseña incorrecta.")
    else:
        form = EmailLoginForm()

    next_url = request.GET.get("next", "")
    return render(request, "login.html", {"form": form, "next": next_url})

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            login(request, user)
            return redirect("core:job_list")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Sesión cerrada correctamente.")
    return redirect("core:job_list")
