from django.shortcuts import render, redirect
from .models import JobOffer
from .forms import JobOfferForm

def job_create(request):
    if request.method == "POST":
        form = JobOfferForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("job_list")
    else:
        form = JobOfferForm()
    return render(request, "job_create.html", {"form": form})

def job_list(request):
    jobs = JobOffer.objects.select_related("company").order_by("-created_at")
    return render(request, "dashboard.html", {"jobs": jobs})
