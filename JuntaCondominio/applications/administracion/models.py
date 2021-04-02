from model_utils.models import TimeStampedModel 
from django.db import models
from django.db.models.signals import post_save, post_delete

# modelos terceros
from applications.edificio.models import Apartamento
from applications.deuda.models import ReferenciaPago, RegistroDeudas
#senales
from .signals import actualizar_gastos, actualizar_ingreso, delete_gastos, delete_ingreso, calcular_deuda_reporte


from .managers import EgresoManager, CierreMesManager , IngresoManager, ReporteManager 
#signal


class Corte_mes(TimeStampedModel):
    MES_CHOICES =(
        ("1","Enero"), ("2","Febrero"), ("3","Marzo"), ("4","Abril"), ("5","Mayo"), ("6","Junio"), 
        ("7","Julio"), ("8","Agosto"), ("9","Septiembre"), ("10","Octubre"), ("11","Noviembre"), ("12","Diciembre"),
    )
    mes = models.CharField("Mes",choices=MES_CHOICES, max_length=2, unique= True) 
    fecha_inicio = models.DateField("Fecha de Inicio ", auto_now=False, auto_now_add=False, blank=True) 
    fecha_fin = models.DateField("Fecha de Fin", auto_now=False, auto_now_add=False, blank=True) 
    monto_egreso = models.DecimalField("Monto total de egreso ", max_digits=20, decimal_places=2, default=0) 
    monto_ingreso = models.DecimalField("Monto total de ingreso ", max_digits=20, decimal_places=2, default=0) 
    reserva= models.DecimalField("Reserva", max_digits=20, decimal_places=2, default=0)
    cerrar_mes=models.BooleanField("Cierre Mes", default=False)
    objects = CierreMesManager()
    
    class Meta:
        verbose_name = "Administracion del Mes"
        verbose_name_plural = "Cierre de Mes"

    def __str__(self):
        return  str(self.id)+ " - "+ self.mes


class Egreso(TimeStampedModel):
    EGRESO_CHOICES =(
        ("1", "Fijo"),
        ("2", "Comunes"),
        ("3", "Otros Gastos"),
    )
    tipo_egreso = models.CharField("Tipo de Egreso", max_length=3, choices=EGRESO_CHOICES) 
    egreso = models.CharField("Egreso", max_length=50)
    descripcion = models.TextField("Texto", blank=True)
    monto = models.DecimalField("Monto", max_digits=20, decimal_places=2, default=0)
    fecha = models.DateField("Fecha ", auto_now=False, auto_now_add=False)
    corte_mes= models.ForeignKey(Corte_mes, verbose_name="Administracion del Mes ", related_name="egreso_mes",on_delete=models.CASCADE) 
    objects = EgresoManager()

    class Meta:
        verbose_name = "Egreso"
        verbose_name_plural = "Egresos"

    def __str__(self):
        return str(self.id) + " " +  self.egreso 


class Ingreso(TimeStampedModel):
    INGRESO_CHOICES =(
        ("1", "Fijo"),
        ("2", "Comunes"),
        ("3", "Otros Ingreso"),
    ) 
    tipo_ingreso = models.CharField("Tipo de Ingreso", max_length=3, choices=INGRESO_CHOICES) 
    ingreso = models.CharField("Ingreso", max_length=50)
    descripcion = models.TextField("Texto", blank=True)
    monto = models.DecimalField("Cantidad", max_digits=20, decimal_places=2, default=0)
    fecha = models.DateField("Fecha ", auto_now=False, auto_now_add=False)
    corte_mes= models.ForeignKey(Corte_mes, verbose_name="Administracion del Mes ",related_name="ingreso_mes", on_delete=models.CASCADE) 
    objects = IngresoManager()

    class Meta:
        verbose_name = "Ingreso"
        verbose_name_plural = "Ingresos"

    def __str__(self):
        return str(self.id) + " " +  self.ingreso
        

class Reporte(TimeStampedModel):
    
    apartamento = models.ForeignKey(Apartamento, verbose_name="Apartamento",related_name="apart_reporte", on_delete=models.CASCADE)
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
        return str(self.id)
        
# Create your models here.



post_save.connect(actualizar_gastos , sender=Egreso) 

post_save.connect(actualizar_ingreso , sender=Ingreso)

post_delete.connect(delete_gastos , sender=Egreso)

post_delete.connect(delete_ingreso , sender=Ingreso)

post_save.connect(calcular_deuda_reporte, sender=Reporte) 