from django.db import models
from django.core.validators import MinValueValidator


class Vaccine(models.Model):
    """
    Representa um tipo de vacina que pode ser administrada.
    """
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Nome da vacina"
    )
    manufacturer = models.CharField(
        max_length=200,
        blank=True,
        help_text="Fabricante farmacêutico"
    )
    description = models.TextField(
        blank=True,
        help_text="Descrição do que a vacina protege"
    )
    species_target = models.CharField(
        max_length=50,
        blank=True,
        help_text="Espécies alvo"
    )
    duration_months = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Periodo de validade em meses (para cálculo da próxima dose)"
    )
    is_mandatory = models.BooleanField(
        default=False,
        help_text="Se esta vacina é legalmente obrigatória"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Vaccine'
        verbose_name_plural = 'Vaccines'
    
    def __str__(self):
        return f"{self.name} ({self.duration_months} months)"