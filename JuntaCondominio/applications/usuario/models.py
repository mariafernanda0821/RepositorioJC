from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
#
from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    # TIPO DE USUARIOS
    ADMINISTRADOR = '0'
    USUARIO = '1'
    OTROS= '2'
    # GENEROS
    VARON = 'M'
    MUJER = 'F'
    #
    OCUPATION_CHOICES = [
        (ADMINISTRADOR, 'Administrador'),
        (USUARIO, 'Usuario'),
        (OTROS, 'Otros'),
    ]

    GENDER_CHOICES = [
        (VARON, 'Masculino'),
        (MUJER, 'Femenino'),
    ]

    email = models.EmailField(unique=True)
    full_name = models.CharField('Nombres', max_length=100)
    ocupation = models.CharField(
        max_length=1, 
        choices=OCUPATION_CHOICES, 
        blank=True
    )
    genero = models.CharField(
        max_length=1, 
        choices=GENDER_CHOICES, 
        blank=True
    )
    date_birth = models.DateField(
        'Fecha de nacimiento', 
        blank=True,
        null=True
    )
    #
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['full_name']

    objects = UserManager()

    def get_short_name(self):
        return self.email
    
    def get_full_name(self):
        return self.full_name
