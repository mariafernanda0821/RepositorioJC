from django.contrib import admin
from .models import Propietario, Edificio, Apartamento
# Register your models here.

class PropietarioAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nombre",
    )   

admin.site.register(Propietario, PropietarioAdmin)


admin.site.register(Edificio)

class ApartamentoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "apartamento",
        "piso",
        "torre",
        "alicuota",
    )   

    # class Meta:
    #     orde

admin.site.register(Apartamento, ApartamentoAdmin)


