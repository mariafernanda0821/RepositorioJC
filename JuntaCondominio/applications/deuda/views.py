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




class ReferenciaView(TemplateView):
    template_name = "deuda/listar_referencia.html"

#VISTA PARA CREAR LA REFERENCIA DE PAGO
class CrearReferenciaPago(View):
    
    def get(self, request, *args, **kwargs):
        instance = Reporte.objects.get(id= self.kwargs["pk"]) 
        z = ReferenciaPago.objects.filter(reporte= instance)

        if not z.exists():
            #debo crear la referencia de pago
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
class ReferenciaPagoUpdateView(UpdateView):
    template_name = "deuda/update_referencia.html"
    model = ReferenciaPago
    form_class = ReferenciaPagoForm
    success_url= reverse_lazy("deuda_app:referencia")
    
    def get_context_data(self, **kwargs):
        context = super(ReferenciaPagoUpdateView, self).get_context_data(**kwargs)
        x=ReferenciaPago.objects.filter(id = self.kwargs["pk"]).first() 
        reporte = x.reporte
        mes = reporte.corte_mes
        apartamento = reporte.apartamento
        propietario = apartamento.propietario
        context["reporte"]= reporte
        context["mes"] = mes
        context["apartamento"] = apartamento
        context["propietario"] = propietario
        context["referencia"] = x
        return context


class CrearDeudasTabla(View):
    def get(self, request, *args, **kwargs):
        apart = Apartamento.objects.all()

        for  x in apart:
            a = RegistroDeudas.objects.create(apartamento = x)
            #a.deuda_pagar = 0.00
            a.save()
        
        return HttpResponseRedirect(
            reverse("deuda_app:listar_deudas")
        )



class RegistroDeudasListView(ListView):
    model = RegistroDeudas
    template_name = "deuda/listar_deudas.html"
    context_object_name = "deudas"
    queryset = RegistroDeudas.objects.all().order_by("apartamento")



#-------------******* VISTA DE REFERENCIA*******--------------------

class ReferenciaListView(FormView):
   # filtar las referencias 
    template_name = "deuda/referencias.html"
    form_class = SeleccionForm

    def get_context_data(self, **kwargs):
        context = super(ReferenciaListView, self).get_context_data(**kwargs)
        mes = self.request.GET.get("mes", '') 
        torre = self.request.GET.get("torre", '')  
        if mes == '' or torre == '':
            context["referencia"] = []
            return context      
        context["referencia"] = ReferenciaPago.objects.buscar_referencia_mes(mes, torre)
        context["mes"] = Corte_mes.objects.filter(id=mes).first() 
        return context


#VISTA DE CUANTO DINERO LE ENTRO EN CADA MES 
