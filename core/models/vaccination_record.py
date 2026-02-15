from django.db import models
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta


class VaccinationRecord(models.Model):
    """
    Represents a vaccination event.
    Links a pet to a vaccine with administration details.
    """
    pet = models.ForeignKey(
        'Pet',
        on_delete=models.CASCADE,
        related_name='vaccination_records',
        help_text="Pet that received the vaccine"
    )
    vaccine = models.ForeignKey(
        'Vaccine',
        on_delete=models.PROTECT,  # Don't delete vaccine if records exist
        related_name='vaccination_records',
        help_text="Vaccine administered"
    )
    administered_date = models.DateField(
        help_text="Date the vaccine was given"
    )
    veterinarian_name = models.CharField(
        max_length=200,
        help_text="Name of the veterinarian who administered the vaccine"
    )
    clinic_name = models.CharField(
        max_length=200,
        blank=True,
        help_text="Veterinary clinic name"
    )
    batch_number = models.CharField(
        max_length=100,
        blank=True,
        help_text="Vaccine batch/lot number"
    )
    next_dose_date = models.DateField(
        null=True,
        blank=True,
        help_text="Calculated date for next dose"
    )
    notes = models.TextField(
        blank=True,
        help_text="Additional observations or reactions"
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
        # Prevent duplicate vaccinations on the same day
        unique_together = [['pet', 'vaccine', 'administered_date']]
    
    def __str__(self):
        return f"{self.pet.name} - {self.vaccine.name} on {self.administered_date}"
    
    @property
    def is_due(self):
        """Check if the next dose is due (within 30 days)"""
        if not self.next_dose_date:
            return False
        days_until_due = (self.next_dose_date - date.today()).days
        return 0 <= days_until_due <= 30
    
    @property
    def is_overdue(self):
        """Check if the next dose is overdue"""
        if not self.next_dose_date:
            return False
        return date.today() > self.next_dose_date
    
    @property
    def days_until_due(self):
        """Calculate days until next dose"""
        if not self.next_dose_date:
            return None
        return (self.next_dose_date - date.today()).days
    
    def calculate_next_dose_date(self):
        """Calculate next dose date based on vaccine duration"""
        if self.vaccine.duration_months:
            return self.administered_date + relativedelta(months=self.vaccine.duration_months)
        return None
    
    def clean(self):
        """Validate model fields"""
        super().clean()
        
        # Validate administered_date is not in the future
        if self.administered_date and self.administered_date > date.today():
            raise ValidationError({
                'administered_date': 'Vaccination date cannot be in the future.'
            })
        
        # Validate administered_date is not before pet's birth
        if self.pet_id and self.administered_date:
            if self.administered_date < self.pet.birth_date:
                raise ValidationError({
                    'administered_date': 'Vaccination date cannot be before pet\'s birth date.'
                })
    
    def save(self, *args, **kwargs):
        """Override save to auto-calculate next dose date"""
        # Calculate next dose if not manually set
        if not self.next_dose_date:
            self.next_dose_date = self.calculate_next_dose_date()
        
        # Validate before saving
        self.full_clean()
        super().save(*args, **kwargs)