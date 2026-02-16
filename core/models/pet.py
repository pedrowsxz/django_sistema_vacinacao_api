from django.db import models
from django.core.exceptions import ValidationError
from datetime import date


class Pet(models.Model):
    """
    Representa um pet cadastrado no sistema.
    Cada pet pertence a uma pessoa.
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
        help_text="Pessoa dona do pet"
    )
    name = models.CharField(max_length=100)
    species = models.CharField(
        max_length=20,
        choices=SPECIES_CHOICES,
        help_text="Tipo de animal"
    )
    breed = models.CharField(
        max_length=100,
        blank=True,
        help_text="Raça (se aplicável)"
    )
    birth_date = models.DateField(help_text="Data de nascimento")
    color = models.CharField(max_length=50, blank=True)
    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Peso in kg"
    )
    notes = models.TextField(
        blank=True,
        help_text="Observações adicionais sobre o pet"
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
        """Calcula a idade do pet em anos"""
        today = date.today()
        age = today.year - self.birth_date.year
        # Ajusta se o aniversário ainda não ocorreu neste ano
        if (today.month, today.day) < (self.birth_date.month, self.birth_date.day):
            age -= 1
        return age
    
    @property
    def age_months(self):
        """Calcula a idade do pet em meses"""
        today = date.today()
        months = (today.year - self.birth_date.year) * 12
        months += today.month - self.birth_date.month
        if today.day < self.birth_date.day:
            months -= 1
        return max(0, months)
    
    def clean(self):
        """Valida os campos do modelo"""
        super().clean()
        
        # Valida que a data de nascimento não esteja no futuro
        if self.birth_date and self.birth_date > date.today():
            raise ValidationError({
                'birth_date': 'Data de nascimento não pode estar no futuro.'
            })
        
        # Valida que o peso seja positivo
        if self.weight is not None and self.weight <= 0:
            raise ValidationError({
                'weight': 'Peso deve ser maior que zero.'
            })
    
    def save(self, *args, **kwargs):
        """Sobrescreve o save para chamar clean()"""
        self.full_clean()
        super().save(*args, **kwargs)