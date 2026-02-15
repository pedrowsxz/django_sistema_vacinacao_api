from django.db import models
from django.core.validators import MinValueValidator


class Vaccine(models.Model):
    """
    Represents a type of vaccine that can be administered to pets.
    """
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Vaccine name (e.g., 'Rabies', 'DHPP')"
    )
    manufacturer = models.CharField(
        max_length=200,
        blank=True,
        help_text="Pharmaceutical company"
    )
    description = models.TextField(
        blank=True,
        help_text="What the vaccine protects against"
    )
    species_target = models.CharField(
        max_length=50,
        blank=True,
        help_text="Target species (e.g., 'dog', 'cat', 'all')"
    )
    duration_months = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Validity period in months (for next dose calculation)"
    )
    is_mandatory = models.BooleanField(
        default=False,
        help_text="Whether this vaccine is legally required"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Vaccine'
        verbose_name_plural = 'Vaccines'
    
    def __str__(self):
        return f"{self.name} ({self.duration_months} months)"