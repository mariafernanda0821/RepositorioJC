
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

        return self.filter(corte_mes=mes).order_by("id")

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
    def crear_egreso(self, instance):
        x = self.create(
            tipo_egreso= "1",
            egreso=" Reserva 10% ",
            descripcion= "Reserva del 10%",
            monto = instance.reserva,
            fecha = timezone.now(),
            corte_mes = instance,
        )
        x.save()
        #print("====> se creo el ingreso===>")
        return x 

class CierreMesManager(models.Manager):
   
   def total_reserva(self):
       
       x = self.all().exclude(id__in=[1,2]).aggregate(total = Sum(F("reserva"),output_field=FloatField()))

       return x["total"]


class IngresoManager(models.Manager):
    
    def totalizar_ingreso_mes(self, pk):
    
        consulta= self.filter(corte_mes =pk)
        x = consulta.aggregate(total = Sum(F("monto"),output_field=FloatField()))
        z= x['total']
        #print("entro manager===>", x)
        return z

    def buscar_ingreso_por_mes(self, pk):
        ingreso = self.filter(corte_mes=pk).order_by("id")
        return ingreso


class ReporteManager(models.Manager):
    
    # def  total_pagado(self,apart):

    #     x = self.filter(apartamento= apart).aggregate(total = Sum(F("monto"),output_field=FloatField()))   
    #     return x
    def buscar_reporte(self, apart):
        x = self.filter(apartamento = apart).exclude(corte_mes__in=[1,2])

        return x

    def buscar_reporte_mes(self, mes, torre):
        #vista para reporte de cada ves y torre
        x = self.filter(apartamento__torre = torre, corte_mes=mes).exclude(corte_mes__in=[1,2])
        
        return x 

    def calcular_reporte_total(self, apart):
        #calcular el monto tootal por reporte de cada apartamento
        #x = self.filter(apartamento= apart).exclude(corte_mes__in=[1,2]).aggregate(total = Sum(F("monto"),output_field=FloatField()))
        x = self.filter(apartamento= apart).aggregate(total = Sum(F("total_pagar"),output_field=FloatField()))

        return x["total"]

    def reporte_por_mes(self,mes):
        #calcular el total de reporte por mes 
        x = self.filter(corte_mes= mes).aggregate(total = Sum(F("monto"),output_field=FloatField()))
        
        return x["total"]
    
    def reporte_deuda_mes(self, mes):
        
        x = self.filter(corte_mes= mes).aggregate(total = Sum(F("deuda"),output_field=FloatField()))
   
        return x["total"]

    def total_reporte_por_mesA(self, mes):
        
        x = self.filter(corte_mes= mes, apartamento__torre=1).aggregate(total = Sum(F("monto"),output_field=FloatField()))
   
        return x["total"]

    def total_reporte_por_mesB(self, mes):
         
        x = self.filter(corte_mes= mes, apartamento__torre=2).aggregate(total = Sum(F("monto"),output_field=FloatField()))
   
        return x["total"]

    def total_reporte_por_mes_alquiler(self, mes):
        
        x = self.filter(corte_mes= mes, apartamento__torre=3).aggregate(total = Sum(F("monto"),output_field=FloatField()))
   
        return x["total"]
    
    def buscar_deudaA(self, mes):
        
        x = self.filter(corte_mes= mes, apartamento__torre=1).aggregate(total = Sum(F("deuda"),output_field=FloatField()))
   
        return x["total"]

    def buscar_deudaB(self, mes):
        
        x = self.filter(corte_mes= mes, apartamento__torre=2).aggregate(total = Sum(F("deuda"),output_field=FloatField()))
   
        return x["total"]

    def buscar_deudaAlquiler(self, mes):
        
        x = self.filter(corte_mes= mes, apartamento__torre=3).aggregate(total = Sum(F("deuda"),output_field=FloatField()))
   
        return x["total"]