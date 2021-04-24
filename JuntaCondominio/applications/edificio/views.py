# python
import datetime
from datetime import timedelta
from decimal import *
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
from applications.utils import render_to_pdf 

#
from .models import *
from applications.edificio.models import * 
from applications.deuda.models import * 

#---------*********VISTA DE Apart *********----------------------------

class AparTorreAView(TemplateView):
    template_name = "edificio/apart/torreA.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["apart"] = Apartamento.objects.filter(torre = 1).order_by("id")
        return context
    

class AparTorreBView(TemplateView):
    template_name = "edificio/apart/torreB.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["apart"] = Apartamento.objects.filter(torre = 2).order_by("id")
        return context


class AlquilerView(TemplateView):
    template_name = "edificio/apart/alquiler.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["apart"] = Apartamento.objects.filter(torre = 3).order_by("id")
        return context


class RegistroPagoApar(TemplateView):
    template_name = "edificio/apart/detail_apart.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["apart"] = Apartamento.objects.filter(id = self.kwargs["pk"]).first()
        context["referencia"] = ReferenciaPago.objects.buscar_referencia(self.kwargs["pk"])
        context["pago_total"] = ReferenciaPago.objects.calcular_referen_total(self.kwargs["pk"])
        return context
    

class RegistroReporte(TemplateView):
    template_name = "edificio/apart/detail_reporte.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["apart"] = Apartamento.objects.filter(id = self.kwargs["pk"]).first()
        context["reporte"] = Reporte.objects.buscar_reporte(self.kwargs["pk"])
        
        return context

#---------*********VISTA DE Apart *********----------------------------


#VISTA QUE GENERA INFORME DEL GASTO DEL MES
class ApartamentoPDF(View):
    #SE VA A GENERAR EL RECIBO DEL MES CORRESPONDIENTE, se actualiza ante de generar el pdf
    #
    def get(self, request, *args, **kwargs):
        apartamento = Apartamento.objects.all().order_by('id')
        #propietario = apartamento
        data = {
            'apartamento': apartamento,
        }
        pdf = render_to_pdf('edificio/apart/apart_voucher.html', data)
        return HttpResponse(pdf, content_type='application/pdf')


# Create your views here.
