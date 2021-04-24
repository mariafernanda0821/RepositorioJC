from django import forms
from django.contrib.auth import authenticate
#
from .models import User

class UserRegisterForm(forms.ModelForm):

    password1 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña',
                'class': 'input-group-field',
            }
        )
    )
    password2 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Repetir Contraseña',
                'class': 'input-group-field',
            }
        )
    )

    class Meta:
        """Meta definition for Userform."""

        model = User
        fields = (
            'email',
            'usuario',
            'full_name',
            'ocupation',
        )
        widgets = {
            'email': forms.EmailInput(
                attrs={
                    'placeholder': 'Correo Electronico ...',
                    'class': 'input-group-field',
                }
            ),
            'usuario': forms.TextInput(
                attrs={
                    'placeholder': 'Ingresar Usuario',
                    'class': 'input-group-field',
                }
            ),
            'full_name': forms.TextInput(
                attrs={
                    'placeholder': 'Nombres ...',
                    'class': 'input-group-field',
                }
            ),
            'ocupation': forms.Select(
                attrs={
                    'placeholder': 'Ocupacion ...',
                    'class': 'input-group-field',
                }
            ),
        }
    
    def clean_password2(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            self.add_error('password2', 'Las contraseñas no son iguales')


