from django.db import models

# Create your models here.
from model_utils.models import TimeStampedModel 
from applications.cierreMes.models import Corte_mes
from .managers import  ReporteManager 


class Reporte(TimeStampedModel):
    
    apartamento = models.ForeignKey(Apartamento, verbose_name="Apartamento", on_delete=models.CASCADE)
    monto = models.DecimalField("Monto a pagar ", max_digits=20, decimal_places=2, default=0)
    fecha = models.DateField("Fecha", auto_now=False, auto_now_add=False)
    corte_mes= models.ForeignKey(Corte_mes, verbose_name="Administracion del Mes ", on_delete=models.CASCADE) 
    deuda = models.DecimalField("Deuda Ocumulada", max_digits=20, decimal_places=2, default=0, blank=True)
    total_pagar=models.DecimalField("Total a pagar", max_digits=20, decimal_places=2, default=0)
    objects = ReporteManager

    class Meta:
        verbose_name = "Reporte"
        verbose_name_plural = "Reportes"

    def __str__(self):
        # return str(self.id)