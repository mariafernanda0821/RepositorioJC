import datetime
from django import forms 

# 
from .models import ReferenciaPago,RegistroDeudas 
from applications.administracion.models  import Corte_mes
from applications.edificio.models import Apartamento


class ReferenciaPagoForm(forms.ModelForm):
    
    class Meta:
        model = ReferenciaPago
        fields = (
            "tipo_pago",
            "monto_pagar", 
            "referencia_pago", 
            "descripcion",
            "pago_bool",
           # "reporte",
        )



class  SeleccionForm(forms.Form):

    mes = forms.ChoiceField(
        required=True,
        choices=Corte_mes.MES_CHOICES, 
        #queryset= ReferenciaPago.objects.filter(reporte__corte_mes=mes),
        widget=forms.Select(
            attrs = {
                'class': 'input-group-field',
            }
        )
    )

    torre = forms.ChoiceField(
        required=True,
        choices=Apartamento.TORRE_CHOICES, 
        #queryset= ReferenciaPago.objects.filter(reporte__apartamento__torre=torre),
        widget=forms.Select(
            attrs = {
                'class': 'input-group-field',
            }
        )
    )

    # def __init__(self, *args, **kwargs):    
    #     super( SeleccionForm, self).__init__(*args, **kwargs)
    #     #queryset = ReferenciaPago.objects.filter(reporte__apartamento__torre=torre, reporte__corte_mes=mes)

        
        #return queryset