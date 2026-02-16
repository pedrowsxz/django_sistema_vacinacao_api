from django.db import models
from django.contrib.auth.models import User
from django.core.validators import EmailValidator, RegexValidator


class Pessoa(models.Model):
    """
    Representa o dono de pets.
    Vinculado ao modelo User do Django para autenticação.
    """
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='pessoa',
        help_text="Conta de usuário associada"
    )
    name = models.CharField(max_length=150)
    email = models.EmailField(
        unique=True,
        validators=[EmailValidator()],
        help_text="Email para contato"
    )
    phone = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Número de telefone deve ser inserido no formato: '+999999999'. Até 15 dígitos permitidos."
            )
        ],
        blank=True,
        help_text="Número de telefone para contato"
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
        """Retorna o número total de pets desta pessoa"""
        return self.pets.count()