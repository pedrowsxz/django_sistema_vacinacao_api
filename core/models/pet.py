from django.db import models
from django.core.exceptions import ValidationError
from datetime import date


class Pet(models.Model):
    """
    Represents a pet registered in the system.
    Each pet belongs to one pessoa.
    """
    SPECIES_CHOICES = [
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('bird', 'Bird'),
        ('rabbit', 'Rabbit'),
        ('hamster', 'Hamster'),
        ('reptile', 'Reptile'),
        ('other', 'Other'),
    ]
    
    pessoa = models.ForeignKey(
        'Pessoa',
        on_delete=models.CASCADE,
        related_name='pets',
        help_text="Pet pessoa"
    )
    name = models.CharField(max_length=100)
    species = models.CharField(
        max_length=20,
        choices=SPECIES_CHOICES,
        help_text="Type of animal"
    )
    breed = models.CharField(
        max_length=100,
        blank=True,
        help_text="Breed (if applicable)"
    )
    birth_date = models.DateField(help_text="Date of birth")
    color = models.CharField(max_length=50, blank=True)
    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Weight in kg"
    )
    notes = models.TextField(
        blank=True,
        help_text="Additional notes about the pet"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Pet'
        verbose_name_plural = 'Pets'
        indexes = [
            models.Index(fields=['pessoa', '-created_at']),
            models.Index(fields=['species']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.get_species_display()})"
    
    @property
    def age_years(self):
        """Calculate pet's age in years"""
        today = date.today()
        age = today.year - self.birth_date.year
        # Adjust if birthday hasn't occurred yet this year
        if (today.month, today.day) < (self.birth_date.month, self.birth_date.day):
            age -= 1
        return age
    
    @property
    def age_months(self):
        """Calculate pet's age in months"""
        today = date.today()
        months = (today.year - self.birth_date.year) * 12
        months += today.month - self.birth_date.month
        if today.day < self.birth_date.day:
            months -= 1
        return max(0, months)
    
    def clean(self):
        """Validate model fields"""
        super().clean()
        
        # Validate birth_date is not in the future
        if self.birth_date and self.birth_date > date.today():
            raise ValidationError({
                'birth_date': 'Birth date cannot be in the future.'
            })
        
        # Validate weight is positive
        if self.weight is not None and self.weight <= 0:
            raise ValidationError({
                'weight': 'Weight must be greater than zero.'
            })
    
    def save(self, *args, **kwargs):
        """Override save to call clean()"""
        self.full_clean()
        super().save(*args, **kwargs)