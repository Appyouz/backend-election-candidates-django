from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from apps import political_figure
from utils.core.base_models import BaseModel
from .core import PoliticalFigure


# Custom validator for 4-digit year
def validate_4_digit_year(value):
    """Validator to ensure year is exactly 4 digits."""
    if not (1000 <= value <= 9999):
        raise ValidationError(
            _('%(value)s is not a valid 4-digit year.'),
            params={'value': value},
        )


class Achievement(BaseModel):
    class CategoryChoices(models.TextChoices):
        LEADERSHIP = 'leadership', _('Leadership')
        ACADEMIC = 'academic', _('Academic')
        PUBLIC_SERVICE = 'public_service', _('Public Service')
        MILITARY = 'military', _('Military')
        OTHER = 'other', _('Other')

    class StatusChoices(models.TextChoices):
        UNVERIFIED = 'unverified', _('Unverified')
        PENDING = 'pending', _('Pending')
        VERIFIED = 'verified', _('Verified')


    political_figure = models.ForeignKey(
        PoliticalFigure,
        on_delete=models.CASCADE,
        related_name='achievements'
    )

    title = models.CharField(max_length=255)
    category = models.CharField(
        max_length=50,
        choices=CategoryChoices.choices,
        default=CategoryChoices.OTHER,
    )
    description = models.TextField(blank=True)
    year = models.IntegerField(validators=[validate_4_digit_year])
    awarding_body = models.CharField(max_length=255)
    evidence_link = models.URLField(max_length=500, blank=True, null=True)
    status = models.CharField(
        max_length=50,
        choices=StatusChoices.choices,
        default=StatusChoices.UNVERIFIED,
    )

    def __str__(self):
        return f"{self.title} ({self.year}) - {self.political_figure.full_name}"


    class Meta:
        ordering = ['-year', 'title']
        db_table = "political_figure_achievement"
        verbose_name = "Achievement"
        verbose_name_plural = "Achievements"
        unique_together = ('political_figure', 'title', 'year')
