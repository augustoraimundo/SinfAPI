from django.contrib.auth.models import AbstractUser
from django.db import models
from decimal import Decimal
import random
from datetime import datetime, timedelta


class Usuario(AbstractUser):
    GENERO_CHOICES = [
        ('Masculino', 'Masculino'),
        ('Feminino', 'Feminino'),
    ]

    nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100)
    genero = models.CharField(max_length=10, choices=GENERO_CHOICES)
    telefone = models.CharField(max_length=20, unique=True)
    provincia = models.CharField(max_length=50)
    municipio = models.CharField(max_length=50)
    saldo = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))

    # 🔹 Campos para verificação dupla
    telefone_verificado = models.BooleanField(default=False)
    codigo_telefone = models.CharField(max_length=6, blank=True, null=True)
    email_verificado = models.BooleanField(default=False)

    # 🔹 Usuário só é ativo após verificação
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nome} {self.sobrenome} ({self.username})"


# 🔹 Modelo separado para códigos de verificação
class VerificationCode(models.Model):
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='codes')
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_valid(self):
        return datetime.now() < self.expires_at

    def __str__(self):
        return f"Código {self.code} para {self.user.telefone}"