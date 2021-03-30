# python
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
from applications.utils import render_to_pdf 

#formulario
from .forms import (
    EgresoForm, MesForm , IngresoForm, CierreMesForm,
    )

#
from .models import *
from applications.edificio.models import *

#VISTA PRINCIPAL

class CierreMesListView(ListView):
    template_name = "administracion/cierre_mes/listar_cierre_mes.html"
    context_object_name = "cierre_mes"

    def get_queryset(self):

        return Corte_mes.objects.all()


#VISTA DE OPCIONES PARA LISTAR O AGREGAR:
class OpcionesView(FormView):
    template_name = "administracion/opcion.html"
    form_class = MesForm

    def form_valid(self, form):
        mes = form.cleaned_data['mes']
        if Corte_mes.objects.filter(id=mes).exists():
            return  HttpResponseRedirect(
                reverse(
                        'admin_app:detail_egreso_mes',
                        kwargs={'pk': mes},
                    )
            )
        else:
            return  HttpResponseRedirect(
                reverse(
                    'admin_app:opciones'
                ) 
            )
       

#----------*****EGRESO*****----------------
#VISTA AGREGAR UN INGRESO 
class EgresoCreateView(CreateView):
    template_name = "administracion/egreso/egreso_add.html"
    form_class = EgresoForm
    success_url=  '.'

        
#VISTA DETALLA LOS EGRESO POR MES
class EgresoMesDetailView(DetailView):
    template_name = "administracion/egreso/detail_egreso_mes.html"
    model = Corte_mes
    
    def get_context_data(self, **kwargs):
        context = super(EgresoMesDetailView, self).get_context_data(**kwargs)
        context["fecha"] = timezone.now()
        context['monto_total']= Egreso.objects.totalizar_gastos_mes(self.kwargs['pk'])
        context["mes"] = Corte_mes.objects.get(id= self.kwargs['pk'])
        context["gastos_mes"] = Egreso.objects.buscar_gasto_por_mes(self.kwargs['pk'])
        print("====>", self.kwargs['pk'])
        return context


#VISTA PARA MODIFIAR UN GASTO
class EgresoUpdateView(UpdateView):
    model = Egreso
    template_name = "administracion/egreso/update_egreso.html"
    form_class = EgresoForm
    success_url = '.'


#VISTA DETALLAR UN gasto
class DetallarEgreso(DetailView):
   # model = Egreso
    template_name = "administracion/egreso/detallar_egreso.html"
    context_object_name = "prueba"
    
    def get_queryset(self):
       return Egreso.objects.filter(id=self.kwargs['pk'])
    

#VISTA PARA ELIMINAR UN GASTO
class EgresoDeleteView(DeleteView):
    #template_name = "administracion/egreso/delete_egreso.html"
    model = Egreso
    success_url = "/"



#VISTA QUE GENERA INFORME DEL GASTO DEL MES
class EgresoMesPdf(View):
    #SE VA A GENERAR EL RECIBO DEL MES CORRESPONDIENTE, se actualiza ante de generar el pdf
    #
    def get(self, request, *args, **kwargs):
        mes = Corte_mes.objects.get(id=self.kwargs['pk'])
        data = {
            'mes': mes,
            'gastos': Egreso.objects.filter(corte_mes= self.kwargs['pk']),
            'total': Egreso.objects.totalizar_gastos_mes(self.kwargs["pk"])
        }
        pdf = render_to_pdf('administracion/egreso/recibo_mes.html', data)
        return HttpResponse(pdf, content_type='application/pdf')


#-----------****** FIN VISTA DE EGRESO ********-----------


#----------***** Vista de Ingreso*******--------------

#VISTA AGREGAR UN INGRESO 
class IngresoCreateView(CreateView):
    template_name = "administracion/ingreso/ingreso_add.html"
    form_class = IngresoForm
    success_url=  '.'


#VISTA DETALLA LOS INGRESO POR MES
class IngresoMesDetailView(DetailView):
    template_name = "administracion/ingreso/detail_ingreso_mes.html"
    model = Corte_mes
    
    def get_context_data(self, **kwargs):
        context = super(IngresoMesDetailView, self).get_context_data(**kwargs)
        context["fecha"] = timezone.now()
        context['monto_total']= Ingreso.objects.totalizar_ingreso_mes(self.kwargs['pk'])
        context["mes"] = Corte_mes.objects.get(id= self.kwargs['pk'])
        context["ingreso_mes"] = Ingreso.objects.buscar_ingreso_por_mes(self.kwargs['pk'])
        #print("====>", self.kwargs['pk'])
        return context


#VISTA QUE GENERA INFORME DEL INGRESO DEL MES
class IngresoMesPdf( View):
    #SE VA A GENERAR EL RECIBO DEL MES CORRESPONDIENTE, se actualiza ante de generar el pdf
    #
    def get(self, request, *args, **kwargs):
        mes = Corte_mes.objects.get(id=self.kwargs['pk'])
        data = {
            'mes': mes,
            'ingresos': Ingreso.objects.filter(corte_mes= self.kwargs['pk']),
            'total': Ingreso.objects.totalizar_ingreso_mes(self.kwargs["pk"])
        }
        pdf = render_to_pdf('administracion/ingreso/recibo_ingreso.html', data)
        return HttpResponse(pdf, content_type='application/pdf')


#-----------****** FIN VISTA DE INGRESO ********-----------

#---------**********FIN VISTA DE REPORTE**********--------- 


#VISTA LISTA TODO LOS REPORTE POR MES
class ReporteListView(DetailView):
    model = Corte_mes
    template_name = "administracion/reporte/reporte.html"
    #context_object_name = "reportes"
 
    def get_context_data(self, **kwargs):
        context = super(ReporteListView, self).get_context_data(**kwargs)
        context["reporte"] = Reporte.objects.filter(corte_mes = self.kwargs['pk'])
        context["mes"] = Corte_mes.objects.get(id = self.kwargs['pk'])
        return context



#VISTA PARA CREAR REPORTE
class ReporteCreateView(View):

    def get(self, request, *args, **kwargs):
        
        x = Corte_mes.objects.get(id= self.kwargs["pk"])

        if x.cerrar_mes:
            #print("=====> Entro al if", x.cerrar_mes)
            apart= Apartamento.objects.all()
            for reporte in apart:
                if Reporte.objects.filter(apartamento=reporte, corte_mes=x).exists():
                    continue
                else:
                    monto = (x.monto_egreso * reporte.alicuota)
                    total= monto + 0 
                    z = Reporte.objects.create(
                        apartamento = reporte,
                        monto = monto,
                        fecha = timezone.now(),
                        corte_mes = x,
                        deuda = 0,
                        total_pagar = total,
                    ) 
                    z.save()
                    #print(z)

            return HttpResponseRedirect(
                    reverse(
                        "admin_app:listar_reporte",
                        kwargs={'pk': x.id },
                        )
                    )

        return HttpResponseRedirect(
                    reverse(
                        "admin_app:opciones",)
                    )


#RECIBO POR MES
class ReporteVoucherPdf(View):
    #CREO EL VOUCHER O RECIBO DE EGRESO DEL MES(necesito restricciones)
    #
    def get(self, request, *args, **kwargs):
        reporte = Reporte.objects.get(id=self.kwargs['pk'])
        gastos=  Egreso.objects.filter(corte_mes=reporte.corte_mes)
        apart =  reporte.apartamento
        propietario = apart.propietario
        mes = Corte_mes.objects.get(id=self.kwargs['pk'])
        data = {
            'reporte': reporte,
            'gastos': gastos ,
            'apart' : apart,
            'propietario': propietario,
            "mes": mes
        }

        pdf = render_to_pdf('administracion/reporte/reporte_vaucher.html', data)
        return HttpResponse(pdf, content_type='application/pdf')

#---------**********FIN VISTA DE REPORTE**********-------------- 



#---------********VISTA DE CIERRE MES *******--------------------

#VISTA CREAR CORTE_MES 
class CierreMesCreateView(CreateView):
   # model = Corte_mes
    template_name = "administracion/cierre_mes/crear_mes.html"
    form_class = CierreMesForm
    success_url = reverse_lazy("admin_app:listar_cierre_mes")


#VISTA ACTUALIZAR TODO EL MES
class CierreMesUpdateView(View):
    #actualizar los gastos e ingresos del cierre del mes correspondiente
    def get(self, request, *args, **kwargs):
        
        total_egreso = Egreso.objects.totalizar_gastos_mes(self.kwargs["pk"])
        total_ingreso = Ingreso.objects.totalizar_ingreso_mes(self.kwargs["pk"])
        instance = Corte_mes.objects.get(id = self.kwargs["pk"])
        #print("====> instance", instance) instance 1 - 1
        #print("====>", self.kwargs["pk"])
        #print("====>", self.kwargs) ====> {'pk': '1'}
        if not  instance.cerrar_mes:
 
            # aqui verifico que ingreso no sea vacio
            if  total_egreso is not None:
                instance.monto_egreso = total_egreso
                # print("entro a egreso", total_egreso)
                # print("==========================")
            if total_ingreso is not None:
                instance.monto_ingreso = total_ingreso
                # print("entro a ingreso", total_ingreso)
                # print("==========================")

            instance.save()
            # print("==========================")
            # print("funciono", total_egreso)
            # print("funciono", total_ingreso)
            # print("==========================")
            return HttpResponseRedirect(
                reverse(
                    'admin_app:listar_cierre_mes'
                )
            )
            
        return HttpResponseRedirect(
                reverse(
                    'admin_app:opciones'
                )
            )


#VISTA CERRAR EL MES COMPLETO
class CerrarMesUpdateView(View):
    #ultima actualizancion de mes 
    def get(self, request, *args, **kwargs):
        instance = Corte_mes.objects.get(id = self.kwargs["pk"])
        if not instance.cerrar_mes:
            
            total_egreso = Egreso.objects.totalizar_gastos_mes(self.kwargs["pk"])
            total_ingreso = Ingreso.objects.totalizar_ingreso_mes(self.kwargs["pk"])
            reserva = total_egreso*0.1

            print("reserva=====>", reserva)
            x = Egreso.objects.crear_egreso(instance, reserva)

            total_egreso = Egreso.objects.totalizar_gastos_mes(self.kwargs["pk"])
            # aqui verifico que no hallas errores
            if  total_egreso is not None:
                instance.monto_egreso = total_egreso
                print("entro a egreso", total_egreso)
                print("==========================")

            if total_ingreso is not None:
                instance.monto_ingreso = total_ingreso
                print("entro a ingreso", total_ingreso)
                print("==========================")

           
            instance.reserva = reserva
            instance.cerrar_mes = True
            instance.save()

            print("se actualizo perfectamente", instance)

            return HttpResponseRedirect(
                reverse(
                    'admin_app:listar_cierre_mes'
                )
            )
        
        #si se cerro el mes nos deberia a crear otro ves o hacer una accion
        return HttpResponseRedirect(
                reverse(
                    'admin_app:opciones'
                )
            )

#---------********VISTA DE CIERRE MES *******--------------------
