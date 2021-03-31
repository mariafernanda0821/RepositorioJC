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
from applications.administracion.models import Reporte
from .forms import ReferenciaPagoForm 

class OpcionesView(TemplateView):
    template_name = "deuda/listar_referencia.html"

class CrearReferenciaPago(View):
    
    def get(self, request, *args, **kwargs):
        instance = Reporte.objects.get(id= self.kwargs["pk"])
        
        if not ReferenciaPago.objects.filter(reporte= instance).exists():
            #debo crear la referencia de pago
            x = ReferenciaPago.objects.create(
                reporte = instance,
            )
            x.save()
            return HttpResponseRedirect(
                reverse("deuda_app:update_referencia")
            )

            
        return HttpResponseRedirect(
            reverse("deuda_app:opciones")

        )



class ReferenciaPagoUpdateView(UpdateView):
    template_name = "deuda/referencia_crear.html"
    #model = ReferenciaPago
    form_class = ReferenciaPagoForm
    success_url= reverse_lazy("deuda_app:opciones")
    
