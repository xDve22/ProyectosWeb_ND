from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from django.conf import settings
from django.contrib import messages
from .models import JobOffer
from .forms import JobOfferForm, JobFilterForm
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
import logging
import base64

logger = logging.getLogger(__name__)

MAX_FILE_SIZE = 1 * 1024 * 1024  # 1MB
ALLOWED_TYPES = ["image/jpeg", "image/png"]


@user_passes_test(lambda u: u.is_staff)
def job_create(request):
    if request.method == "POST":
        form = JobOfferForm(request.POST, request.FILES)
        if form.is_valid():
            job = form.save(commit=False)
            job.save()

            logo = request.FILES.get("logo")
            logger.info("================================")
            logger.info(f"Logo recibido: {logo}")
            logger.info("================================")

            if logo:
                if logo.content_type not in ALLOWED_TYPES:
                    messages.error(request, "Only JPG and PNG images are allowed.")
                    logger.info("================================")
                    logger.error(f"Tipo de archivo no permitido: {logo.content_type}")
                    logger.info("================================")
                    return render(request, "job_create.html", {"form": form})

                if logo.size > MAX_FILE_SIZE:
                    messages.error(request, "The image must be less than 1MB.")
                    logger.info("================================")
                    logger.error(f"Archivo muy grande: {logo.size} bytes")
                    logger.info("================================")
                    return render(request, "job_create.html", {"form": form})

                try:
                    logo.seek(0)
                    file_content = logo.read()
                    file_base64 = base64.b64encode(file_content).decode('utf-8')
                    
                    upload = settings.IMAGEKIT.upload_file(
                        file=file_base64,
                        file_name=logo.name,
                        options=UploadFileRequestOptions(
                            folder="/devjobs/media/",
                            is_private_file=False,
                            use_unique_file_name=True,
                        ),
                    )

                    if hasattr(upload, 'response_metadata'):
                        image_url = upload.response_metadata.raw.get('url')
                    elif hasattr(upload, 'url'):
                        image_url = upload.url
                    else:
                        image_url = upload.get('url')

                    if not image_url:
                        messages.error(request, "Error uploading image.")
                        logger.info("================================")
                        logger.error("No se pudo obtener la URL de la imagen")
                        logger.info("================================")
                        return render(request, "job_create.html", {"form": form})

                    job.company.logo = image_url
                    job.company.save()

                except Exception as e:
                    messages.error(request, f"Image upload failed: {str(e)}")
                    logger.info("================================")
                    logger.exception(f"Error al subir imagen: {str(e)}")
                    logger.info("================================")
                    return render(request, "job_create.html", {"form": form})

            messages.success(request, "Job created successfully.")
            return redirect("job_list")
        else:
            logger.info("================================")
            logger.error(f"Errores del formulario: {form.errors}")
            logger.info("================================")
    else:
        form = JobOfferForm()

    return render(request, "job_create.html", {"form": form})

@user_passes_test(lambda u: u.is_staff)
def job_edit(request, pk):
    job = get_object_or_404(JobOffer, pk=pk)
    company = job.company

    if request.method == "POST":
        form = JobOfferForm(request.POST, request.FILES, instance=job)
        if form.is_valid():
            form.save()

            if "logo" in request.FILES:
                logo = request.FILES["logo"]

                if logo.content_type not in ALLOWED_TYPES:
                    messages.error(request, "Only JPG and PNG images are allowed.")
                    logger.error(f"Tipo de archivo no permitido: {logo.content_type}")
                    return render(request, "job_edit.html", {"form": form, "job": job})

                if logo.size > MAX_FILE_SIZE:
                    messages.error(request, "The image must be less than 1MB.")
                    logger.error(f"Archivo muy grande: {logo.size} bytes")
                    return render(request, "job_edit.html", {"form": form, "job": job})

                try:
                    logo.seek(0)
                    file_content = logo.read()
                    file_base64 = base64.b64encode(file_content).decode('utf-8')

                    upload = settings.IMAGEKIT.upload_file(
                        file=file_base64,
                        file_name=logo.name,
                        options=UploadFileRequestOptions(
                            folder="/devjobs/media/",
                            is_private_file=False,
                            use_unique_file_name=True,
                        ),
                    )

                    if hasattr(upload, 'response_metadata'):
                        image_url = upload.response_metadata.raw.get('url')
                    elif hasattr(upload, 'url'):
                        image_url = upload.url
                    else:
                        image_url = upload.get('url')

                    if not image_url:
                        messages.error(request, "Error uploading image.")
                        logger.error("No se pudo obtener la URL de la imagen")
                        return render(request, "job_edit.html", {"form": form, "job": job})

                    company.logo = image_url
                    company.save()

                except Exception as e:
                    messages.error(request, f"Image upload failed: {str(e)}")
                    logger.exception(f"Error al actualizar imagen: {str(e)}")
                    return render(request, "job_edit.html", {"form": form, "job": job})

            messages.success(request, "Job updated successfully.")
            return redirect("job_detail", pk=job.pk)
        else:
            logger.error(f"Errores del formulario: {form.errors}")
    else:
        form = JobOfferForm(instance=job)

    return render(request, "job_edit.html", {"form": form, "job": job})

@user_passes_test(lambda u: u.is_staff)
def job_delete(request, pk):
    job = get_object_or_404(JobOffer, pk=pk)
    job.delete()
    return redirect("job_list")

def job_list(request):
    jobs = JobOffer.objects.select_related("company").order_by("-created_at")
    form = JobFilterForm(request.GET or None)

    if form.is_valid():
        title_or_company = form.cleaned_data.get("title_or_company")
        location = form.cleaned_data.get("location")
        full_time_only = form.cleaned_data.get("full_time_only")

        if title_or_company:
            jobs = jobs.filter(
                Q(title__icontains=title_or_company)
                | Q(company__name__icontains=title_or_company)
                | Q(description__icontains=title_or_company)
            )
        if location:
            jobs = jobs.filter(location__icontains=location)
        if full_time_only:
            jobs = jobs.filter(employment_type="FT")

    paginator = Paginator(jobs, 12)
    page = request.GET.get("page", 1)
    jobs_page = paginator.get_page(page)

    return render(
        request,
        "dashboard.html",
        {
            "jobs": jobs_page,
            "form": form,
            "page": page,
            "has_next": jobs_page.has_next(),
        },
    )

def job_detail(request, pk):
    job = get_object_or_404(JobOffer, pk=pk)
    return render(request, "job_details.html", {"job": job})
