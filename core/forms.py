from django import forms
from .models import JobOffer

class JobOfferForm(forms.ModelForm):
    description = forms.CharField(widget=forms.HiddenInput())

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
