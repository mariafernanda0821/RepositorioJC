from django.db import models
#
from django.db.models import Q, Sum, F, FloatField, ExpressionWrapper 

class ReferenciaPagoManager(models.Manager):
    
    def  total_referencia_por_mes(self,mes ):
        
        x = self.filter(reporte__corte_mes= mes).aggregate(total = Sum(F("monto_pagar"),output_field=FloatField()))
        
        return x["total"]

    def  total_referencia_por_mesA(self,mes ):
        
        x = self.filter(reporte__corte_mes= mes, reporte__apartamento__torre=1, pago_bool=True).aggregate(total = Sum(F("monto_pagar"),output_field=FloatField()))
   
        return x["total"]

    def  total_referencia_por_mesB(self,mes ):
        
        x = self.filter(reporte__corte_mes= mes, reporte__apartamento__torre=2, pago_bool=True).aggregate(total = Sum(F("monto_pagar"),output_field=FloatField()))
   
        return x["total"]

    def  total_referencia_por_mes_alquiler(self,mes):
        
        x = self.filter(reporte__corte_mes= mes, reporte__apartamento__torre=3, pago_bool=True).aggregate(total = Sum(F("monto_pagar"),output_field=FloatField()))
   
        return x["total"]

    def  calcular_referen_total(self,apart):
       
        x = self.filter(reporte__apartamento= apart).exclude(reporte__corte_mes__in=[1,2]).aggregate(total = Sum(F("monto_pagar"),output_field=FloatField()))
   
        return x["total"]

    def buscar_referencia(self, apart):
        #buscar referencia por apartamento pagadas
       
        x = self.filter(reporte__apartamento = apart, pago_bool=True).exclude(reporte__corte_mes__in=[1,2])

        return x 

    def buscar_referencia_mes(self, mes, torre):
       
        x = self.filter(reporte__apartamento__torre = torre, reporte__corte_mes=mes, pago_bool=True).exclude(reporte__corte_mes__in=[1,2]).order_by("reporte__apartamento")
        
        return x


class RegistroDeudaManager(models.Manager):
    def deuda_acumulada(self):
        x = self.all().aggregate(total = Sum(F("deuda_ocumulada"),output_field=FloatField()))
        return x["total"]

    def deuda_total(self):
        x = self.all().aggregate(total = Sum(F("deuda_pagar"),output_field=FloatField()))
        return x["total"]