from django.db import models
from django.forms import ValidationError

from utils.core.base_models import BaseModel

# Create your models here.


class PoliticalParty(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    # we can keep slugfield as unique=True since we can just add random suffix if a soft deleted party has same slug
    slug = models.SlugField(unique=True)
    abbreviation = models.CharField(max_length=50)
    founded_date = models.DateField()
    dissolved_date = models.DateField(
        null=True, blank=True
    )  # NULL if the party is active
    ideology = models.TextField(blank=True)
    hq_location = models.CharField(max_length=255)
    website = models.URLField(blank=True)
    logo_url = models.URLField(blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        from utils.core.general import check_and_generate_slug

        # set slug if it is not set
        if not self.id:
            # fail_silently=False does not allow the slug field to be set if it already exists
            self.slug = check_and_generate_slug(
                self, "name", "slug", fail_silently=False
            )

        return super().save(*args, **kwargs)

    class Meta:
        db_table = "political_party"
        verbose_name = "Political Party"
        verbose_name_plural = "Political Parties"
        ordering = ["-created_at"]
        # Adding the check constraint here - founded date must be strictly before dissolved date
        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(founded_date__lt=models.F("dissolved_date"))
                    | models.Q(dissolved_date__isnull=True)
                ),
                name="founded_date_before_dissolved_date_or_active",
            )
        ]
