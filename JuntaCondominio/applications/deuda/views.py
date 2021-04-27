import datetime
from datetime import timedelta
# django
from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin)

from django.views.generic import (
    ListView, TemplateView, 
    CreateView, UpdateView, DeleteView, DetailView, View )

from django.views.generic.edit import (
    FormView
)
from .models import ReferenciaPago, RegistroDeudas
from applications.administracion.models import Reporte , Corte_mes
from applications.edificio.models import Apartamento
from .forms import ReferenciaPagoForm , SeleccionForm

from django.db.models import Q, Sum, F, FloatField, ExpressionWrapper  
from .signals import calcular_deuda
from applications.utils import render_to_pdf 

from django.core.mail import EmailMessage
from .functions import referencias_listar_Pdf, comprobande_pagoPdf, deuda_pdf, enviar_correos
from applications.usuario.mixins import AdminPermisoMixin, UsuarioPermisoMixin

class ReferenciaView(TemplateView):
    template_name = "deuda/listar_referencia.html"


#VISTA PARA CREAR LA REFERENCIA DE PAGO
class CrearReferenciaPago(AdminPermisoMixin,View):
    
    def get(self, request, *args, **kwargs):
        instance = Reporte.objects.get(id= self.kwargs["pk"]) 
        z = ReferenciaPago.objects.filter(reporte= instance)

        if not z.exists():
            x = ReferenciaPago.objects.create(
                reporte = instance,
            )
            x.save()
            #print("valor de x ")
            #lista_pagos = ReferenciaPago.objects.filter(reporte__apartamento= instance.apartamento).aggregate(total = Sum(F("monto_pagar"),output_field=FloatField()))
            #calcular_deuda(x,lista_pagos)
            return HttpResponseRedirect(
                reverse("deuda_app:update_referencia" , kwargs={'pk': x.id},)
            )

            
        return HttpResponseRedirect(
            reverse("deuda_app:update_referencia" , kwargs={'pk': z[0].id},)

        )


#VISTA PARA ACTUALIZAR EL PAGO POR MES
class ReferenciaPagoUpdateView(AdminPermisoMixin,UpdateView):
    template_name = "deuda/update_referencia.html"
    model = ReferenciaPago
    form_class = ReferenciaPagoForm
    # = "prueba"
    success_url= '.'
    
    def get_context_data(self, **kwargs):
        context = super(ReferenciaPagoUpdateView, self).get_context_data(**kwargs)
        x = ReferenciaPago.objects.filter(id = self.kwargs["pk"]).first() 
        context["reporte"]= x.reporte
        return context


class CrearDeudasTabla(View):
    def get(self, request, *args, **kwargs):
        apart = Apartamento.objects.all()
        for  x in apart:
            a = RegistroDeudas.objects.get(apartamento = x)
            #a.save()
        
        return HttpResponseRedirect(
            reverse("deuda_app:listar_deudas")
        )


class RegistroDeudasListView(UsuarioPermisoMixin,ListView):
    model = RegistroDeudas
    template_name = "deuda/listar_deudas.html"
    context_object_name = "deudas"
    #queryset = RegistroDeudas.objects.all().order_by("apartamento")
   
    def get_queryset(self):
        queryset = RegistroDeudas.objects.all().order_by("apartamento")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_acumulada"] = RegistroDeudas.objects.deuda_acumulada()
        context["total_deudas"] = RegistroDeudas.objects.deuda_total()
        return context
    
    

class ReferenciaListView(UsuarioPermisoMixin,FormView):
   # filtar las referencias 
    template_name = "deuda/referencias.html"
    form_class = SeleccionForm

    def get_context_data(self, **kwargs):
        context = super(ReferenciaListView, self).get_context_data(**kwargs)
        mes = self.request.GET.get("mes", '') 
        torre = self.request.GET.get("torre", '')  
        if mes == '' or torre == '':
            context["referencias"] = []
            return context      
        context["referencias"] = ReferenciaPago.objects.buscar_referencia_mes(mes, torre)
        context["mes"] = Corte_mes.objects.filter(id=mes).first() 
        return context


class EnviarComprobantePDF(UsuarioPermisoMixin,View):
    #enviar el comprobante, se obtiene es el id de referencia 
    def get(self, request, *args, **kwargs):
        pdf = comprobande_pagoPdf(self.kwargs['pk'])
        x = ReferenciaPago.objects.filter(id=self.kwargs['pk']).first()
        correo = x.reporte.apartamento.propietario.email
        apartamento =  x.reporte.apartamento.apartamento
        titulo = "comprobante.pdf"
        asunto = "Comprobante de pago del " + "[" + apartamento + "]"
        mensaje = "Se adjunta el comprobante correspondiente a su pago del mes " 
        enviar_correos(pdf, asunto, mensaje, correo,titulo)
        print("se envio correo", correo)
        print("mes", x.reporte.corte_mes.mes) 

        return HttpResponse(comprobande_pagoPdf(self.kwargs['pk']), content_type='application/pdf')


class ReferenciasPDF(UsuarioPermisoMixin,View):
    def get(self, request, *args, **kwargs):
        
        return HttpResponse(referencias_listar_Pdf(self.kwargs["pk"]), content_type='application/pdf')


class EnviarReferenciasPDF(UsuarioPermisoMixin,View):
    #enviar el comprobante, se obtiene es el id de referencia 
    def get(self, request, *args, **kwargs):
       
        pdf = referencias_listar_Pdf(self.kwargs["pk"])
        asunto = "Rerencias"
        mensaje = "Se adjunta referencias "
        corre="mariadelsocorro2108@gmail.com"
        titulo="referencias.pdf"
        enviar_correos(pdf,asunto,mensaje, correo, titulo)

        return HttpResponse(deuda_pdf(), content_type='application/pdf')


class DeudasPDF(UsuarioPermisoMixin,View):
    def get(self, request, *args, **kwargs):
        
        return HttpResponse(deuda_pdf(), content_type='application/pdf')

    
class EnviarDeudaPDF(UsuarioPermisoMixin,View):
    #enviar el deudas
    def get(self, request, *args, **kwargs):
        pdf = deuda_pdf()
        asunto = "Deuda"
        mensaje = "Se adjunta deudas"
        titulo="deuda.pdf"
        correo="mariadelsocorro2108@gmail.com"
        if enviar_correos(pdf,asunto,mensaje, correo, titulo):
            print("=========> se envio el correo")
            return HttpResponseRedirect(
                reverse("deuda_app:listar_deudas")
            )
        return []




#VISTA DE CUANTO DINERO LE ENTRO EN CADA MES 
