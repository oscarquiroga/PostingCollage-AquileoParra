from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

class User(AbstractUser):
    ROLE_CHOICES = (
        ("estudiante", "Estudiante"),
        ("profesor", "Profesor"),
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[\w @.+-]+$',
                message="El nombre solo puede contener letras, números, espacios y @/./+/-/_"
            )
        ]
    )
    email = models.EmailField(
        unique=False,
        blank=False,
        null=False
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='estudiante')

    def __str__(self):
        return f"{self.username} ({self.role})"
