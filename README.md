# RepositorioJC

    Este es un mini proyecto, sobre un Sistema de Condominio para el edificio Residencias San Jose.
Esta dividido por 4 aplicaciones que consta de :
Administracion:
    los gastos y ingresos del edificio, que depende de 2 claves ForeignKey una es Corte mes y la otra seria los codigo de Acceso que nos ayuda para llevar un control en los gastos del edificio
    El corte de mes es el principal modelos, ya que aqui llevamos el control por mes 
    Reporte este modelo nos ayuda a llevar control por apartamentos, es decir, aqui se le indica a cada apartamento cuales fueron los gastos del mes y cual es el monto a pagar de ese mes y su deuda actual, cuyo reporte se les manda por correo electronico en el formato PDF. 

Deudas: aqui hay 2 models 
    Registro de deudas, este modelo va variando ya que cuando los reportes son creados se actualizan las deudas actuales de cada apartamento, al igual que cuando se registra una Referencia de Pago, se actualiza cuyas deudas.
    Referencia de Pago, est modelo es para llevar un control de los apartamentos que realizaron su pago, se ingresa cuyo pago y se genera un comprobante de pago que se le envia al propietario. 

Edificio: aqui se encuentra 2 modelos
    Apartamento, todo los apartamentos esta registrado y depende de una clave foreingKey que seria propietario.
    Propietario, esta los registro de cada propietario.

