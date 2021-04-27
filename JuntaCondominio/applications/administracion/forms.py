import datetime
from django import forms 
from django.db import IntegrityError
from .models import Egreso , Corte_mes, Ingreso, CodigoAcceso
from applications.edificio.models import Apartamento


class EgresoForm(forms.ModelForm):
    class Meta:
        model = Egreso
        fields = (
            "tipo_egreso",
            "codigo",
            "egreso",
            "descripcion",
            "monto",
            "monto_dolar",
            "precio_dolar",
            "fecha",
            "corte_mes",
        )

        widgets = {
            'tipo_egreso': forms.Select(
                attrs = {
                    'class': 'input-group-field',
                }
            ),
            'codigo': forms.Select(
                #choices=Corte_mes.MES_CHOICES,
                attrs = {
                    'class': 'input-group-field',
                 }
             ),
            'egreso': forms.TextInput(
                attrs = {
                    'placeholder': 'Egreso',
                    'class': 'input-group-field',
                }
            ),
            'descripcion': forms.Textarea(
                attrs = {
                    'placeholder': 'Descripcion',
                    'class': 'input-group-field',
                }
            ),
            'monto': forms.NumberInput(
                attrs = {
                    'placeholder': '1',
                    'class': 'input-group-field',
                }
            ),
            
            'monto_dolar': forms.NumberInput(
                attrs = {
                    'placeholder': 'monto en dolares',
                    'class': 'input-group-field',
                }
            ),

            'precio_dolar': forms.NumberInput(
                attrs = {
                    'placeholder': 'Precio en dolares',
                    'class': 'input-group-field',
                }
            ),

            'fecha': forms.DateInput(
                format='%Y-%m-%d',
                attrs = {
                    'type': 'date',
                    'class': 'input-group-field',
                }
            ),
            'corte_mes': forms.Select(
                #choices=Corte_mes.MES_CHOICES,
                attrs = {
                    'class': 'input-group-field',
                 }
             ),
        }

    #los formularios me traen las instance
    def clean_corte_mes(self):
        x = self.cleaned_data['corte_mes']
        #print("self.cleaned_data['corte_mes']=====valor>",self.cleaned_data)
        #print("self.cleaned_data['corte_mes']=====valor>",x  )
        #print("self.cleaned_data['corte_mes']=====valor>",x.id  )
        # x =Corte_mes.objects.get(mes= self.cleaned_data['corte_mes'])
        #print ("=====>",)
        if x.cerrar_mes:
            raise forms.ValidationError("Error.Mes cerrado")
        else:
            return x

    
    # def clean_codigo_acceso(self):
    #     print("entrar")
    #     try:
    #         CodigoAcceso.objects.get(
    #             nombre=self.cleaned_data['codigo_acceso']
    #             )
    #         #if not self.instance.pk:
    #          #   raise forms.ValidationError("Notificación Ya Existe")
    #     except CodigoAcceso.DoesNotExist:
    #         pass
    #     except IntegrityError:
    #             raise forms.ValidationError("Codigo de Acceso Ya Existe")
    #     return self.cleaned_data
    
    # def clean_codigo_acceso(self):
    #     if  CodigoAcceso.objects.filter(codigo=self.cleaned_data['codigo_acceso']).exist():
    #         raise forms.ValidationError("Codigo ya existe")
    #     return self.cleaned_data['codigo_acceso']
    
    # def clean_codigo_nombre(self): 
    #     if CodigoAcceso.objects.filter(nombre=self.cleaned_data['codigo_nombre']):
    #         raise forms.ValidationError("Nombre ya existe")
         
    #     print("===>",self.cleaned_data)
    #     return self.cleaned_data


class IngresoForm(forms.ModelForm):
    
    class Meta:
        model = Ingreso
        fields = (
            "tipo_ingreso",
            "ingreso",
            "descripcion",
            "monto",
            "fecha",
            "corte_mes"
        )

        widgets = {
            'tipo_ingreso': forms.Select(
                attrs = {
                    'class': 'input-group-field',
                }
            ),
            'ingreso': forms.TextInput(
                attrs = {
                    'placeholder': 'Egreso',
                    'class': 'input-group-field',
                }
            ),
            'descripcion': forms.Textarea(
                attrs = {
                    'placeholder': 'Descripcion',
                    'class': 'input-group-field',
                }
            ),
            'monto': forms.NumberInput(
                attrs = {
                    'placeholder': '1',
                    'class': 'input-group-field',
                }
            ),
            'fecha': forms.DateInput(
                format='%Y-%m-%d',
                attrs = {
                    'type': 'date',
                    'class': 'input-group-field',
                }
            ),
            'corte_mes': forms.Select(
                attrs = {
                    'class': 'input-group-field',
                }
            ),
        }

    def clean_corte_mes(self):
        x = self.cleaned_data['corte_mes']
       
        if x.cerrar_mes:
            raise forms.ValidationError('Error. Mes cerrado.')
        else:
            return x


class CierreMesForm(forms.ModelForm):
    
    class Meta:
        model = Corte_mes
        fields = ("mes","fecha_inicio", "fecha_fin", "nota")

        widgets = {
            'fecha_inicio': forms.DateInput(
                    format='%Y-%m-%d',
                    attrs = {
                        'type': 'date',
                        'class': 'input-group-field',
                    }
                ),
            'fecha_fin': forms.DateInput(
                    format='%Y-%m-%d',
                    attrs = {
                        'type': 'date',
                        'class': 'input-group-field',
                    }
                ),
            'mes': forms.Select(
                    attrs = {
                        'class': 'input-group-field',
                    }
                ),
            'nota': forms.Textarea(
                attrs = {
                    'placeholder': 'Anotacion',
                    'class': 'input-group-field',
                }
            ),
        }

    def clean_mes(self):
        if  Corte_mes.objects.filter(cerrar_mes=False).exists() :
            raise forms.ValidationError('Existe un mes activo.')
        else:
            return self.cleaned_data['mes']


class CodigoAccesoForm(forms.ModelForm):
    
    class Meta:
        model = CodigoAcceso
        fields= (
            "codigo",
            "nombre",
            "tipo",
        )
         

class SeleccionForm(forms.Form):
    OPCION_CHOICES = (
        ("1", "Reporte"),
        ("2", "Referencia"),
    )
    mes = forms.ChoiceField(
        required=True,
        choices=Corte_mes.MES_CHOICES,
        widget=forms.Select(
            attrs = {
                'class': 'input-group-field',
            }
        )
    )

    opciones = forms.ChoiceField(
        required=True,
        choices=OPCION_CHOICES,
        widget=forms.Select(
            attrs = {
                'class': 'input-group-field',
            }
        )
    )

    torre = forms.ChoiceField(
        required=True,
        choices=Apartamento.TORRE_CHOICES,
        widget=forms.Select(
            attrs = {
                'class': 'input-group-field',
            }
        )
    )




class CodigoAcceso2Form(forms.Form):
    codigo_tipo = forms.ChoiceField(
        required=False,
        choices=CodigoAcceso.CHOICES_TIPO,
        widget=forms.Select(
            attrs = {
                'class': 'input-group-field',
            }
        )
    )
    codigo_acceso = forms.CharField(
        label='Codigo',
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Contraseña',
                'class': 'input-group-field',
            }
        )
    )

    codigo_nombre = forms.CharField(
        label='Nombre',
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Contraseña',
                'class': 'input-group-field',
            }
        )
    )



