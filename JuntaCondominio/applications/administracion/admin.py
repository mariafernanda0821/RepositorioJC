from django.contrib import admin
from .models import Egreso, Ingreso, Reporte, Corte_mes
# Register your models here.
class EgresoAdmin(admin.ModelAdmin):
    list_display = (

       "id" ,"egreso", "corte_mes"
    )   

admin.site.register(Egreso, EgresoAdmin)

admin.site.register(Ingreso)
admin.site.register(Reporte)

class Corte_mesAdmin(admin.ModelAdmin):
    list_display = (

       "id" ,"mes",
    )   

admin.site.register(Corte_mes,Corte_mesAdmin)


