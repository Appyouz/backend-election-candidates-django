from django.db import models
from utils.core.base_models import BaseModel
from django_countries.fields import CountryField

# Create your models here.


class Address(BaseModel):

    # Universal parts
    street_address = models.CharField(max_length=255)  # "123 Main St"
    street_address_2 = models.CharField(max_length=255, blank=True)  # Apt, suite, etc.

    city = models.CharField(max_length=100)

    # State/Province/Region (generic naming to cover US states, Canadian provinces, Indian states, etc.)
    region = models.CharField(max_length=100, blank=True)

    postal_code = models.CharField(max_length=20, blank=True)

    # Always required
    country = CountryField()

    # Extra flexibility
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)

    class Meta:
        db_table = "address"
        verbose_name = "Address"
        verbose_name_plural = "Addresses"
        ordering = ["-created_at"]
        constraints = []
