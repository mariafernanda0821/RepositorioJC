from django.db.models import Q, Sum, F, FloatField, ExpressionWrapper 


def actualizar_gastos(sender, instance, **kwargs):
    x = instance.corte_mes # la instancia de gastos y busco el corte mesde corte_mes  indica 
    x.monto_egreso = x.monto_egreso + instance.monto
    x.save()


def actualizar_ingreso(sender, instance, **kwargs):
    x = instance.corte_mes
    x.monto_ingreso = x.monto_ingreso + instance.monto
    x.save()

def delete_gastos(sender, instance, **kwargs):
    x = instance.corte_mes
    x.monto_egreso = x.monto_egreso - instance.monto
    x.save()


def delete_ingreso(sender, instance, **kwargs):
    x = instance.corte_mes
    x.monto_ingreso = x.monto_ingreso - instance.monto
    x.save()



def calcular_deuda_reporte(sender, instance, **kwargs):
    #instance de REPORTE cuando se crea
    lista_reporte = Reporte.objects.filter(apartamento= instancia.apartamento).aggregate(total = Sum(F("monto"),output_field=FloatField()))
    lista_pagos = ReferenciaPago.objects.filter(reporte__apartamento= instance.apartamento).aggregate(total = Sum(F("monto_pagar"),output_field=FloatField()))
    registro_deudas= RegistroDeudas.objects.filter(apartamento= instance.apartamento).first()

    if lista_pagos["total"] is None:
        registro_deudas.deuda_pagar = lista_reporte["total"] + 0

    registro_deudas.deuda_pagar = lista_reporte["total"] + lista_pagos["total"]