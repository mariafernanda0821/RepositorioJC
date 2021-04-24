import decimal
from django.db import models
from django.db.models.signals import post_save
from model_utils.models import TimeStampedModel
from django.db.models import Q, Sum, F, FloatField, ExpressionWrapper  


from applications.administracion.models import Reporte  
#from applications.edificio.models import Apartamento
#
#from .signals import calcular_deuda 

from .managers import ReferenciaPagoManager, RegistroPagoManager


class RegistroDeudas(TimeStampedModel):
    
    apartamento = models.OneToOneField("edificio.Apartamento", verbose_name="Apartamento", on_delete=models.CASCADE)
    deuda_ocumulada = models.DecimalField("Deuda Acumulada", max_digits=20, decimal_places=2, default=0)
    deuda_pagar = models.DecimalField("Deuda Pagar", max_digits=20, decimal_places=2, default=0, null=True)
    objects = ReferenciaPagoManager()


    class Meta:
        verbose_name = "Registro Deuda"
        verbose_name_plural = "Registro Deudas"
        ordering = ['apartamento']

    def __str__(self):
        return str (self.id)



class ReferenciaPago(TimeStampedModel):
    
    PAGO_CHOICES = (
        ("Transferencia", "Transferencia"),
        ("Efectivo BS", "Efectivo BS"), 
        ("Divisa", "Divisa"),
        ("Deposito", "Depositos")
    )
    tipo_pago= models.CharField("Tipo de pago", choices=PAGO_CHOICES, max_length=50 , blank=True)
    monto_pagar = models.DecimalField("Monto de Pago", max_digits=20, decimal_places=2,default=0)
    referencia_pago = models.CharField("Referencia de Pago", max_length=50, blank=True) 
    descripcion = models.CharField("Anotaciones", max_length=50 , blank=True) 
    pago_bool = models.BooleanField("Pago", default= False)
    reporte = models.OneToOneField("administracion.Reporte", verbose_name="Reporte", on_delete=models.CASCADE)
    objects = ReferenciaPagoManager()

    class Meta:
        verbose_name = "Referencia Pago"
        verbose_name_plural = "Referencia Pagos"
    

    def __str__(self):
        return str(self.id) 




def calcular_deuda(sender, instance, **kwargs):

    if sender == ReferenciaPago:

        apart = instance.reporte.apartamento
        
    if sender == Reporte:
        apart = instance.apartamento
    
    lista_pagos = ReferenciaPago.objects.filter(reporte__apartamento= apart).exclude(reporte__corte_mes__in=[1,2]).aggregate(total = Sum(F("monto_pagar"),output_field=FloatField()))
    lista_reporte = Reporte.objects.filter(apartamento= apart).exclude(corte_mes__in=[1,2]).aggregate(total = Sum(F("monto"),output_field=FloatField()))
    registro_deudas= RegistroDeudas.objects.filter(apartamento= apart).first()
   
    print("====> lista de pago:",lista_pagos["total"])
    print("====> lista de reporte:",lista_reporte["total"])
  
    if lista_pagos["total"] is None:
        print("entre") 
        registro_deudas.deuda_pagar =  decimal.Decimal(lista_reporte["total"])
        registro_deudas.save() 
    else:
        registro_deudas.deuda_pagar = decimal.Decimal(lista_reporte["total"]) - decimal.Decimal(lista_pagos["total"])
        registro_deudas.save()

post_save.connect(calcular_deuda, sender = ReferenciaPago)  
post_save.connect(calcular_deuda, sender = Reporte)  

 