from django.db.models import Q, Sum, F, FloatField, ExpressionWrapper 
#from applications.deuda.models import ReferenciaPago, RegistroDeudas 
#from decimal import Decimal
import decimal
def actualizar_gastos(sender, instance, **kwargs):
    x = instance.corte_mes # la instancia de gastos y busco el corte mesde corte_mes  indica 
    
    print("===>",instance.monto)
    x.monto_egreso = decimal.Decimal(x.monto_egreso) + decimal.Decimal(instance.monto)
    x.save()
  

def actualizar_ingreso(sender, instance, **kwargs):
    x = instance.corte_mes
    x.monto_ingreso = decimal.Decimal(x.monto_ingreso) + decimal.Decimal(instance.monto)
    x.save()

def delete_gastos(sender, instance, **kwargs):
    x = instance.corte_mes
    x.monto_egreso = decimal.Decimal(x.monto_egreso) - decimal.Decimal(instance.monto)
    x.save()


def delete_ingreso(sender, instance, **kwargs):
    x = instance.corte_mes
    x.monto_ingreso = decimal.Decimal(x.monto_ingreso) - decimal.Decimal(instance.monto)
    x.save()
