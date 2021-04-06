from django.contrib import admin
from .models import ReferenciaPago, RegistroDeudas
# Register your models here.

class RegistroDeudasAdmin(admin.ModelAdmin):
    list_display = (

        "apartamento", "deuda_ocumulada", "deuda_pagar" , 
    )   

admin.site.register(RegistroDeudas, RegistroDeudasAdmin)

class ReferenciaPagoAdmin(admin.ModelAdmin):
    list_display = (
       "id", "reporte", "monto_pagar",
    )   

admin.site.register(ReferenciaPago, ReferenciaPagoAdmin)