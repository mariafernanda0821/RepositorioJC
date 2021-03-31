import datetime
from django import forms 

# 
from .models import ReferenciaPago,RegistroDeudas

class ReferenciaPagoForm(forms.Form):
    model = ReferenciaPago
    fields = (
        "tipo_pago",
        "monto_pagar", 
        "referencia_pago", 
        "descripcion",
        "pago_bool",
        )
