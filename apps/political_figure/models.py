from django.db import models

from apps.core.models import Address
from apps.political_party.models import PoliticalParty
from utils.core.base_models import BaseModel
from utils.core.general import check_and_generate_slug
from utils.core.validation import nepal_phone_number_validator

# Create your models here.


class PoliticalFigure(BaseModel):
    class Gender(models.TextChoices):
        MALE = "m", "Male"
        FEMALE = "f", "Female"

    full_name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=Gender.choices)
    biography = models.TextField(blank=True)
    photo = models.ImageField(
        upload_to="political_figures/photos/", null=True, blank=True
    )

    home_address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        null=True,
        related_name="home_politicians",
    )
    current_address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        null=True,
        related_name="current_politicians",
    )
    political_party = models.ForeignKey(
        PoliticalParty,
        on_delete=models.SET_NULL,
        null=True,
        related_name="figures",
    )

    contact_number = models.CharField(
        max_length=15, blank=True, validators=[nepal_phone_number_validator]
    )
    website = models.URLField(blank=True)

    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)

    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = check_and_generate_slug(
                self, "full_name", "slug", fail_silently=False
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = "political_figure"
        verbose_name = "Political Figure"
        verbose_name_plural = "Political Figures"
        ordering = ["-created_at"]
        constraints = []
