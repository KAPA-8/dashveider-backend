from django.db import models
from django.conf import settings

# Create your models here.


class Organization(models.Model):
    name = models.CharField(max_length=255, unique=True)
    logo_url = models.URLField(max_length=255, null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    document_number = models.CharField(max_length=255, null=True, blank=True)
    issues = models.TextField(null=True, blank=True)
    employees_count = models.IntegerField(default=0)

    class Meta:
        ordering = ["name"]

        def __str__(self):
            return self.name

    @classmethod
    def get_radical_org(cls):
        """Get or create the Radical superuser organization"""
        org, created = cls.objects.get_or_create(
            name="Radical", defaults={"description": "Super administrator organization"}
        )
        return org

    @property
    def is_radical(self):
        """Check if this is the Radical organization"""
        return self.name == "Radical"


class UserProfile(models.Model):
    """Links users to organizations for multi-tenancy"""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="organization_profile",
    )
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="users"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "organization"]

    def __str__(self):
        return f"{self.user.email} - {self.organization.name}"

    @property
    def can_create_organizations(self):
        """Only Radical organization users can create new organizations"""
        return self.organization.is_radical
