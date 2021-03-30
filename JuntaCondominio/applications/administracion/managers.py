
# python
import datetime
from datetime import timedelta
# django
from django.utils import timezone
from django.db import models
#
from django.db.models import Q, Sum, F, FloatField, ExpressionWrapper

class EgresoManager(models.Manager):
   
    def listar_egresos(self):

       return self.all()

    def buscar_gasto_por_mes(self, mes):

        return self.filter(corte_mes=mes)

    def totalizar_gastos_mes(self, pk):

        consulta= self.filter(corte_mes =pk)
        x = consulta.aggregate(total = Sum(F("monto"),output_field=FloatField()))
        z= x['total']
        return z
    
    def buscar_fecha(self, fecha1,fecha2):
        #print("======>", fecha1)
        #print("======>", fecha2)
        
        resultado = self.filter(
            Q(fecha__gt= fecha1)|
            Q(fecha__lt= fecha2)
        )  
       # print("=====", resultado)
        return resultado
    #?date_start=2021-01-01&date_end=2021-01-24
    def crear_egreso(self, instance, reserva):
        x = self.create(
            tipo_egreso= "1",
            egreso="Reserva 10% ",
            descripcion= "Reserva del 10%",
            monto = reserva,
            fecha = timezone.now(),
            corte_mes = instance,
        )
        x.save()
        print("====> se creo el ingreso===>")
        return x 


class CierreMesManager(models.Manager):
   
   def total_gastos(self):

       return []


class IngresoManager(models.Manager):
    
    def totalizar_ingreso_mes(self, pk):
    
        consulta= self.filter(corte_mes =pk)
        x = consulta.aggregate(total = Sum(F("monto"),output_field=FloatField()))
        z= x['total']
        #print("entro manager===>", x)
        return z

    def buscar_ingreso_por_mes(self, pk):
        ingreso = self.filter(corte_mes=pk)
        return ingreso

class ReporteManager(models.Manager):
    pass
