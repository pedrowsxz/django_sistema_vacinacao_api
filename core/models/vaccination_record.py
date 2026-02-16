from django.db import models
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta


class VaccinationRecord(models.Model):
    """
    Representa um registro de vacinação.
    Vincula um pet a uma vacina com detalhes da administração.
    """
    pet = models.ForeignKey(
        'Pet',
        on_delete=models.CASCADE,
        related_name='vaccination_records',
        help_text="Pet que recebeu a vacina"
    )
    vaccine = models.ForeignKey(
        'Vaccine',
        on_delete=models.PROTECT,
        related_name='vaccination_records',
        help_text="Vacina administrada"
    )
    administered_date = models.DateField(
        help_text="Data em que a vacina foi administrada"
    )
    veterinarian_name = models.CharField(
        max_length=200,
        help_text="Nome do veterinário que administrou a vacina"
    )
    clinic_name = models.CharField(
        max_length=200,
        blank=True,
        help_text="Nome da clínica veterinária"
    )
    batch_number = models.CharField(
        max_length=100,
        blank=True,
        help_text="Número do lote da vacina"
    )
    next_dose_date = models.DateField(
        null=True,
        blank=True,
        help_text="Data calculada para a próxima dose"
    )
    notes = models.TextField(
        blank=True,
        help_text="Observações adicionais ou reações"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-administered_date']
        verbose_name = 'Vaccination Record'
        verbose_name_plural = 'Vaccination Records'
        indexes = [
            models.Index(fields=['pet', '-administered_date']),
            models.Index(fields=['vaccine']),
            models.Index(fields=['next_dose_date']),
        ]
        # Evita vacinas duplicadas no mesmo dia
        unique_together = [['pet', 'vaccine', 'administered_date']]
    
    def __str__(self):
        return f"{self.pet.name} - {self.vaccine.name} on {self.administered_date}"
    
    @property
    def is_due(self):
        """Verifica se a próxima dose está próxima (dentro de 30 dias)"""
        if not self.next_dose_date:
            return False
        days_until_due = (self.next_dose_date - date.today()).days
        return 0 <= days_until_due <= 30
    
    @property
    def is_overdue(self):
        """Verifica se a próxima dose está atrasada"""
        if not self.next_dose_date:
            return False
        return date.today() > self.next_dose_date
    
    @property
    def days_until_due(self):
        """Calcula os dias restantes até a próxima dose"""
        if not self.next_dose_date:
            return None
        return (self.next_dose_date - date.today()).days
    
    def calculate_next_dose_date(self):
        """Calcula a data da próxima dose com base na duração da vacina"""
        if self.vaccine.duration_months:
            return self.administered_date + relativedelta(months=self.vaccine.duration_months)
        return None
    
    def clean(self):
        """Valida os campos do modelo"""
        super().clean()
        
        # Valida que a data aplicada não está no futuro
        if self.administered_date and self.administered_date > date.today():
            raise ValidationError({
                'administered_date': 'Vaccination date cannot be in the future.'
            })
        
        # Valida que a vacinação não ocorreu antes do nascimento do pet
        if self.pet_id and self.administered_date:
            if self.administered_date < self.pet.birth_date:
                raise ValidationError({
                    'administered_date': 'A data da vacinação não pode ser anterior ao nascimento do pet.'
                })
    
    def save(self, *args, **kwargs):
        """Sobrescreve o save para calcular automaticamente a próxima dose"""
        # Calcula próxima dose se não foi definida manualmente
        if not self.next_dose_date:
            self.next_dose_date = self.calculate_next_dose_date()
        
        # Validate before saving
        self.full_clean()
        super().save(*args, **kwargs)