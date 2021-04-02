from django.db import models
from django.db.models.signals import post_save
from model_utils.models import TimeStampedModel

from applications.administracion.models import Reporte
from applications.edificio.models import Apartamento
#
from .signals import calcular_deuda 

from .managers import ReferenciaPagoManager, RegistroPagoManager


class RegistroDeudas(TimeStampedModel):
    
    apartamento = models.OneToOneField("edificio.Apartamento", verbose_name="Apartamento", on_delete=models.CASCADE)
    deuda_ocumulada = models.DecimalField("Deuda", max_digits=20, decimal_places=2, default=0)
    deuda_pagar = models.DecimalField("Deuda Acumulada", max_digits=20, decimal_places=2, default=0)
    objects = ReferenciaPagoManager()


    class Meta:
        verbose_name = "Registro Deuda"
        verbose_name_plural = "Registro Deudas"

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





post_save.connect(calcular_deuda, sender=ReferenciaPago) 
 