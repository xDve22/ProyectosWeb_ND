import base64
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages
from datetime import date
from django.conf import settings
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions

from .models import Profile

from .forms import EmailLoginForm, RegisterForm, ProfileForm

logger = logging.getLogger(__name__)

MAX_FILE_SIZE = 1 * 1024 * 1024  # 1MB
ALLOWED_TYPES = ["image/jpeg", "image/png"]

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
                return redirect(next_url or "jobs:job_list")
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
            return redirect("jobs:job_list")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    if field == "__all__":
                        messages.error(request, error)
                    else:
                        messages.error(request, f"{form.fields[field].label}: {error}")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Sesión cerrada correctamente.")
    return redirect("jobs:job_list")

@login_required
def profile_detail(request):
    profile = get_object_or_404(Profile, user=request.user)
    
    profile_fields = [
        {'label': 'Birth Date', 'value': profile.birth_date, 'format': 'date'},
        {'label': 'Phone', 'value': profile.phone, 'format': 'text'},
        {'label': 'Address', 'value': profile.address, 'format': 'text'},
        {'label': 'Country', 'value': profile.country, 'format': 'text'},
        {'label': 'City', 'value': profile.city, 'format': 'text'},
    ]
    
    return render(request, "profile/detail.html", {
        "profile": profile,
        "profile_fields": profile_fields
    })

@login_required
def profile_edit(request):
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            avatar = request.FILES.get("avatar")

            if avatar:
                if avatar.content_type not in ALLOWED_TYPES:
                    messages.error(request, "Only JPG and PNG images are allowed.")
                    return render(request, "profile/edit.html", {"form": form})

                if avatar.size > MAX_FILE_SIZE:
                    messages.error(request, "The image must be less than 1MB.")
                    return render(request, "profile/edit.html", {"form": form})

                logger.info(f"FILES: {request.FILES}")

                try:
                    avatar.seek(0)
                    file_content = avatar.read()
                    file_base64 = base64.b64encode(file_content).decode("utf-8")

                    upload = settings.IMAGEKIT.upload_file(
                        file=file_base64,
                        file_name=avatar.name,
                        options=UploadFileRequestOptions(
                            folder="/devjobs/profile/",
                            is_private_file=False,
                            use_unique_file_name=True,
                        ),
                    )

                    if hasattr(upload, "response_metadata"):
                        image_url = upload.response_metadata.raw.get("url")
                    elif hasattr(upload, "url"):
                        image_url = upload.url
                    else:
                        image_url = upload.get("url")

                    if not image_url:
                        messages.error(request, "Error uploading image.")
                        return render(request, "profile/edit.html", {"form": form})

                    profile.avatar = image_url

                except Exception as e:
                    messages.error(request, f"Image upload failed: {str(e)}")
                    logger.exception(f"Error uploading avatar: {str(e)}")
                    return render(request, "profile/edit.html", {"form": form})

            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("accounts:profile_detail")

        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileForm(instance=profile)

    return render(request, "profile/edit.html", {"form": form})
