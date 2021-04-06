from django.db.models import Q, Sum, F, FloatField, ExpressionWrapper  



def calcular_deuda(sender, instance, **kwargs):
    apart = instance.reporte.apartamento
    lista_pagos = ReferenciaPago.objects.total_pagado(apart)
    lista_reporte = Reporte.objects.filter(apartamento= apart).aggregate(total = Sum(F("monto"),output_field=FloatField()))
    registro_deudas= RegistroDeudas.objects.filter(apartamento= apart).first()

    if lista_pagos["total"] is None:
        registro_deudas.deuda_pagar = lista_reporte["total"] 
        registro_deudas.save() 

    registro_deudas.deuda_pagar = lista_reporte["total"] + lista_pagos["total"]
    registro_deudas.save()