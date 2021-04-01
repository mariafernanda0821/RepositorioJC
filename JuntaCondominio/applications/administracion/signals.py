


def actualizar_gastos(sender, instance, **kwargs):
    x = instance.corte_mes # la instancia de corte_mes  indica 
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
