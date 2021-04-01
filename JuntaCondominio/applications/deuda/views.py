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
from applications.administracion.models import Reporte, Apartamento
from .forms import ReferenciaPagoForm 

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
    
      #def form_valid(self, form):

    
class CrearDeudasTabla(View):
    def get(self, request, *args, **kwargs):
        apart = Apartamento.objects.all()

        for  x in apart:
            a = RegistroDeudas.objects.create(apartamento = x)
            a.save()
        
        return HttpResponseRedirect(
            reverse("deuda_app:listar_deudas")
        )



class RegistroDeudasListView(ListView):
    model = RegistroDeudas
    template_name = "deuda/listar_deudas.html"
    context_object_name = "deudas"
    queryset = RegistroDeudas.objects.all().order_by("apartamento")


#VISTA CALCULA DEUDAS 
class CalcularDeudas(View):
    pass
