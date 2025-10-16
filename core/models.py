from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True, null=True)
    logo = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.name

class JobOffer(models.Model):
    EMPLOYMENT_TYPE_CHOICES = [
        ("FT", "Full time"),
        ("PT", "Part time"),
        ("IN", "Internship"),
        ("CT", "Contract"),
        ("FL", "Freelance"),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="job_offers")
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    employment_type = models.CharField(max_length=2, choices=EMPLOYMENT_TYPE_CHOICES)

    def __str__(self):
        return f"{self.title} — {self.company.name}"
