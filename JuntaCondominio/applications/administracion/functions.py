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

def egreso_pdf(mes):
    mes = Corte_mes.objects.get(id=mes)
        #gastos= Egreso.objects.filter(corte_mes= self.kwargs['pk']).order_by("codigo__codigo")
    gastos= Egreso.objects.buscar_gasto_por_mes(mes)
    total = Egreso.objects.totalizar_gastos_mes(mes) #ESTOY PASANDO EL MES
    data = {
            'mes': mes,
            'gastos': gastos,
            'total':  total
        }
    pdf = render_to_pdf('administracion/egreso/recibo_mes.html', data)

    return pdf



def reporte_vaucher_pdf(id_reporte):
    reporte = Reporte.objects.get(id=id_reporte)
    gastos=  Egreso.objects.filter(corte_mes = reporte.corte_mes).order_by('codigo__codigo')
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
        }
    if mes.id == 3:
        
        pdf = render_to_pdf('administracion/reporte/reporte_vaucher.html', data)
    
        return pdf

    pdf = render_to_pdf('administracion/reporte/reporte_pdf.html', data)
    
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
        }

    pdf = render_to_pdf('administracion/reporte/reciboAlquiler.html', data)
    return pdf


def reportes_general_pdf(id_mes, id_torre):
    reportes = Reporte.objects.filter(corte_mes__id=id_mes, apartamento__torre=id_torre).order_by("apartamento")
    mes = Corte_mes.objects.get(id=id_mes)
    torre = Apartamento.objects.filter(torre=id_torre).first()
    data = {
        'reportes': reportes,
        'mes': mes,
        'torre':torre,
        }

    pdf = render_to_pdf('administracion/reporte/reporte_globalPDF.html', data)
    return pdf 


def enviar_correos(pdf, asunto, mensaje, correo, titulo):
    
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
    

def crear_codigo(self, **params):
   
    codigo = CodigoAcceso.objects.create(
        codigo= params["codigo"],
        nombre= params["nombre"],
    )
    codigo.save()
    return True


def update_corte_mes(self, **params):
    verificar = Corte_mes.objects.filter(mes=params["mes"]).exists()
   
    if verificar:
        instance = Corte_mes.objects.filter(mes=params["mes"]).first()
        instance.nota=params["nota"]
        instance.save()
    return verificar



def informe_alquiler_pdf(id_mes):
    reportes = Reporte.objects.filter(apartamento__torre="3", corte_mes=id_mes).exclude(apartamento__id=173).order_by("id")
 
    total_pagar = Reporte.objects.total_reporte_por_mes_alquiler(id_mes)
    data = {
            'reporte': reportes,
            'total_pagar': total_pagar,
            'fecha': timezone.now()
        }

    pdf = render_to_pdf('administracion/reporte/celtibera.html', data)
    return pdf