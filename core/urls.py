from django.urls import path
from . import views

urlpatterns = [
    path("", views.job_list, name="job_list"),
    path("jobs/create/", views.job_create, name="job_create"),
]
