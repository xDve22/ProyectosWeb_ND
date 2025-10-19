from django import forms
from .models import JobOffer

class JobOfferForm(forms.ModelForm):
    description = forms.CharField(widget=forms.HiddenInput())
    logo = forms.ImageField(required=False)
    class Meta:
        model = JobOffer
        fields = ["company", "title", "description", "location", "employment_type"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Enter job title"}),
            "location": forms.TextInput(attrs={"placeholder": "Enter job location"}),
            "employment_type": forms.Select(attrs={"placeholder": "Select employment type"}),
            "company": forms.Select(attrs={"placeholder": "Select a company"}),
            "description": forms.HiddenInput(),
        }

class JobFilterForm(forms.Form):
    title_or_company = forms.CharField(
        required=False,
        label="Title / Company / Expertise",
        widget=forms.TextInput(attrs={"placeholder": "Filter by title, companies, expertise…"}),
    )
    location = forms.CharField(
        required=False,
        label="Location",
        widget=forms.TextInput(attrs={"placeholder": "Filter by location"}),
    )
    full_time_only = forms.BooleanField(
        required=False,
        label="Full time only",
        label_suffix="",
    )
