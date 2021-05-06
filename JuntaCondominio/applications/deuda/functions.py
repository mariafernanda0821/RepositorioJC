# python
import datetime
from datetime import timedelta
from django.core.mail import EmailMessage
from django.utils import timezone
from applications.utils import render_to_pdf 
from .models import *
from applications.edificio.models import * 
from applications.deuda.models import *


def referencias_listar_Pdf(id_mes):
    referencias = ReferenciaPago.objects.filter(reporte__corte_mes = id_mes, pago_bool=True).order_by('reporte__apartamento__apartamento')
    data = {
        'referencias': referencias,
    }
    pdf = render_to_pdf('deuda/PDF_referencias.html', data)
    return pdf


def comprobande_pagoPdf(id_referencia):
    referencia = ReferenciaPago.objects.get(id = id_referencia)
    reporte = referencia.reporte
    apart = referencia.reporte.apartamento
    propietario = apart.propietario
    mes = referencia.reporte.corte_mes
    data = {
        'referencia': referencia,
        'reporte' : reporte,
        'apart': apart,
       'propietario': propietario,
       'mes':mes
    }
    pdf = render_to_pdf('deuda/comprobante.html', data)
    return pdf


def deuda_pdf():
    deudas = RegistroDeudas.objects.all().order_by("apartamento")
    total_acumulada = RegistroDeudas.objects.deuda_acumulada()
    total_deudas = RegistroDeudas.objects.deuda_total()
    #total = total_acumulada + total_deudas
    data = {
        'deudas': deudas,
        'total_acumulada':total_acumulada,
        'total_deudas':total_deudas,
     #   'total': total,
        }
    pdf = render_to_pdf('deuda/deudas_pdf.html', data)
    return pdf


def enviar_correos(pdf, asunto, mensaje, correo,titulo):
    #pdf = deuda_pdf()

    #asunto = "Deuda"
    #mensaje = "Se adjunta deudas " 
    email_remitente = "sanjosecondominio21@gmail.com"
    if type(correo) == list: 
        #print("entre a lista")
        email = EmailMessage(asunto, mensaje, email_remitente, correo)
    else:
        #print("entre variable")
        email = EmailMessage(asunto, mensaje, email_remitente, [correo,])

    email.attach(titulo, pdf.getvalue(), "application/pdf")
    email.content_subtype = pdf  # Main content is now text/html
    email.encoding = 'ISO-8859-1'
    email.send()
    return True