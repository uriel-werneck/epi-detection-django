from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager


class User(AbstractUser):
    username = None
    first_name = None
    last_name = None

    nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    email = models.EmailField(max_length=120, unique=True)
    email_confirmado = models.BooleanField(default=False)
    # password field is inherited from AbstractUser

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome', 'sobrenome', 'telefone']

    objects = UserManager()

    def __str__(self):
        return f'{self.email} - {self.nome} {self.sobrenome}'
