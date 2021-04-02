from django.db.models import Q, Sum, F, FloatField, ExpressionWrapper  


# ESTA SENAL ES CUANDO SE GENERE de creacion y actualizacion para REFERENCIA DE PAGO
def calcular_deuda(sender, instance, **kwargs):
    #instance de referencia
    reporte = instance.reporte
    lista_reporte = Reporte.objects.filter(apartamento= reporte.apartamento).aggregate(total = Sum(F("monto"),output_field=FloatField()))
    lista_pagos = ReferenciaPago.objects.filter(reporte__apartamento= reporte.apartamento).aggregate(total = Sum(F("monto_pagar"),output_field=FloatField()))
    registro_deudas= RegistroDeudas.objects.filter(apartamento= reporte.apartamento).first()

    # if lista_pagos["total"] is None:
    #     registro_deudas.deuda_pagar = lista_reporte["total"] + 0

    registro_deudas.deuda_pagar = lista_reporte["total"] + lista_pagos["total"]