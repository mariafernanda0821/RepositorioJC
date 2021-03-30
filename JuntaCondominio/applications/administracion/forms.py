import datetime
from django import forms 

from .models import Egreso , Corte_mes, Ingreso


class EgresoForm(forms.ModelForm):
    
    class Meta:
        model = Egreso
        fields = (
            "tipo_egreso",
            "egreso",
            "descripcion",
            "monto",
            "fecha",
            "corte_mes"
        )

        widgets = {
            'tipo_egreso': forms.Select(
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
        #print("self.cleaned_data['corte_mes']=====valor>",x.cerrar_mes  )
        #print("self.cleaned_data['corte_mes']=====valor>",x  )
        #print("self.cleaned_data['corte_mes']=====valor>",x.id  )

       # x =Corte_mes.objects.get(mes= self.cleaned_data['corte_mes'])
        #print ("=====>", )
        if x.cerrar_mes:
            raise forms.ValidationError("Error.Mes cerrado")
        else:
            return x


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
        fields = ("mes","fecha_inicio", "fecha_fin")

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
                )
        }

    def clean_mes(self):
        if  Corte_mes.objects.filter(cerrar_mes=False).exists() :
            raise forms.ValidationError('Existe un mes activo.')
        else:
            return self.cleaned_data['mes']


class MesForm(forms.Form):
    mes = forms.ChoiceField(
        required=True,
        choices=Corte_mes.MES_CHOICES,
        widget=forms.Select(
            attrs = {
                'class': 'input-group-field',
            }
        )
    )







