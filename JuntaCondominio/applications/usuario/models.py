from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
#
from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    # TIPO DE USUARIOS
    ADMINISTRADOR = '0'
    NORMAL = '1'
    
    OCUPATION_CHOICES = [
        (ADMINISTRADOR, 'Administrador'),
        (NORMAL, 'Normal'),
    ]

    email = models.EmailField(unique=True)
    usuario = models.CharField('Usuario', unique=True, max_length= 20)
    full_name = models.CharField('Nombres Completo', max_length=100)
    ocupation = models.CharField(
        max_length=1, 
        choices=OCUPATION_CHOICES, 
        blank=True
    )
    
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'usuario'

    REQUIRED_FIELDS = ['full_name']

    objects = UserManager()

    def get_short_name(self):
        return self.usuario
    
    def get_full_name(self):
        return self.full_name
