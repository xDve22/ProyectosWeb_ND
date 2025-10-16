from django.contrib import admin
from .models import Company, JobOffer

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "logo" ,"website")
    search_fields = ("name",)

@admin.register(JobOffer)
class JobOfferAdmin(admin.ModelAdmin):
    list_display = ("title", "company", "location", "employment_type", "created_at")
    list_filter = ("employment_type", "created_at")
    search_fields = ("title", "company__name", "description")
