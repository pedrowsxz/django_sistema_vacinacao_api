from django.db import models
from django.contrib.auth.models import User
from django.core.validators import EmailValidator, RegexValidator


class Pessoa(models.Model):
    """
    Represents a pet owner.
    Linked to Django's User model for authentication.
    """
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='pessoa',
        help_text="Associated user account"
    )
    name = models.CharField(max_length=150)
    email = models.EmailField(
        unique=True,
        validators=[EmailValidator()],
        help_text="Contact email"
    )
    phone = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            )
        ],
        blank=True,
        help_text="Contact phone number"
    )
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Pessoa'
        verbose_name_plural = 'Pessoas'
    
    def __str__(self):
        return self.name
    
    @property
    def total_pets(self):
        """Return the total number of pets owned"""
        return self.pets.count()