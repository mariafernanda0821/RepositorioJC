# python
import datetime
from datetime import timedelta

from django.core.mail import EmailMessage
from django.utils import timezone

from applications.utils import render_to_pdf 

from .models import *
from applications.edificio.models import * 
from applications.deuda.models import * 

#funcion
def reporte_vaucher_pdf(id_reporte):
    reporte = Reporte.objects.get(id=id_reporte)
    gastos=  Egreso.objects.filter(corte_mes = reporte.corte_mes).order_by('id')
    apart =  reporte.apartamento
    propietario = apart.propietario
    mes = reporte.corte_mes
    reserva = Corte_mes.objects.total_reserva() 
    data = {
            'reporte': reporte,
            'gastos': gastos ,
            'apart' : apart,
            'propietario': propietario,
            "mes": mes,
            "reserva":reserva,
            "nota":"A la Taza del dia BCV 2.363.858,21"
        }

    pdf = render_to_pdf('administracion/reporte/reporte_vaucher.html', data)
    return pdf


def reporte_alquiler_pdf(id_reporte):
    reporte = Reporte.objects.get(id=id_reporte)
    gastos=  Egreso.objects.filter(corte_mes = reporte.corte_mes).order_by('id')
    apart =  reporte.apartamento
    propietario = apart.propietario
    mes = reporte.corte_mes
    #total= Egreso.objects.totalizar_gastos_mes(mes) 
    reserva = Corte_mes.objects.total_reserva() 
    data = {
            'reporte': reporte,
            'gastos': gastos ,
            'apart' : apart,
            'propietario': propietario,
            "mes": mes,
            #'total': total, #ESTOY PASANDO EL MES 
            "reserva":reserva,
            #"control":control,
            "nota":"A la Taza del dia BCV 2.363.858,21"
        }

    pdf = render_to_pdf('administracion/reporte/reciboAlquiler.html', data)
    return pdf
        

def enviar_correos(pdf, asunto, mensaje, correo, titulo):
    
    email_remitente = "sanjosecondominio21@gmail.com"
    email = EmailMessage(asunto, mensaje, email_remitente, [correo,])
    email.attach(titulo, pdf.getvalue(), "application/pdf")
    email.content_subtype = pdf  # Main content is now text/html
    email.encoding = 'ISO-8859-1'
    email.send()
    