from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from .models import JobOffer
from .forms import JobOfferForm, JobFilterForm

@user_passes_test(lambda u: u.is_staff)
def job_create(request):
    if request.method == "POST":
        form = JobOfferForm(request.POST, request.FILES) 
        if form.is_valid():
            job = form.save(commit=False)
            logo = form.cleaned_data.get("logo")
            if logo:
                company = job.company
                company.logo = logo
                company.save()
            job.save()
            return redirect("job_list")
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
                company.logo = request.FILES["logo"]
                company.save()

            return redirect("job_detail", pk=job.pk)
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

    per_page = 12
    page = int(request.GET.get("page", 1))
    paginator = Paginator(jobs, per_page)

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
