# python
import datetime
from datetime import timedelta
from decimal import *
# django
#from django_weasyprint import *

from django.core.mail import EmailMessage
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
    EgresoForm, SeleccionForm, IngresoForm, CierreMesForm,
    )

#
from .models import *
from applications.edificio.models import * 
from applications.deuda.models import * 



#VISTA PRINCIPAL

class CierreMesListView(ListView):
    template_name = "administracion/cierre_mes/listar_cierre_mes.html"
    context_object_name = "cierre_mes"

    def get_queryset(self):

        return Corte_mes.objects.all().order_by("mes")


#VISTA DE OPCIONES PARA LISTAR O AGREGAR:
class OpcionesView(DetailView):
    template_name = "administracion/cierre_mes/opcion.html"
    model = Corte_mes
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_reporte"] = Reporte.objects.reporte_por_mes(self.kwargs['pk'])
        context["total_deuda"] = Reporte.objects.reporte_deuda_mes(self.kwargs['pk'])
        context["total_referencia"] = ReferenciaPago.objects.total_referencia_por_mes(self.kwargs['pk'])
        
        context["total_reporteA"] = Reporte.objects.total_reporte_por_mesA(self.kwargs['pk'])
        context["total_reporteB"] = Reporte.objects.total_reporte_por_mesB(self.kwargs['pk'])
        context["deuda_torreB"] = Reporte.objects.buscar_deudaB(self.kwargs['pk'])
        context["deuda_torreA"] = Reporte.objects.buscar_deudaA(self.kwargs['pk'])
        context["deuda_alquiler"] = Reporte.objects.buscar_deudaAlquiler(self.kwargs['pk'])

        context["total_reporteAlq"] = Reporte.objects.total_reporte_por_mes_alquiler(self.kwargs['pk'])
        context["total_referenciaA"] = ReferenciaPago.objects.total_referencia_por_mesA(self.kwargs['pk'])
        context["total_referenciaB"] = ReferenciaPago.objects.total_referencia_por_mesB(self.kwargs['pk'])
        context["total_referenciaAlq"] = ReferenciaPago.objects.total_referencia_por_mes_alquiler(self.kwargs['pk'])

        return context
    

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
        #print("====>", self.kwargs['pk'])
        return context


#VISTA PARA MODIFIAR UN GASTO
class EgresoUpdateView(UpdateView):
    template_name = "administracion/egreso/update_egreso.html"
    model = Egreso
    form_class = EgresoForm
    success_url = "."
    # def get_success_url(self):
    #     return reverse("admin_app:update_egres", args=(self.object.id,))



#VISTA PARA ELIMINAR UN GASTO
class EgresoDeleteView(DeleteView):
    #template_name = "administracion/egreso/delete_egreso.html"
    model = Egreso
    success_url = "/"
    #reverse_lazy("admin_app:detallar_gasto", kwargs={"pk": self.kwargs["pk"])



#VISTA QUE GENERA INFORME DEL GASTO DEL MES
class EgresoMesPdf(View):
    #SE VA A GENERAR EL RECIBO DEL MES CORRESPONDIENTE, se actualiza ante de generar el pdf
    #
    def get(self, request, *args, **kwargs):
        mes = Corte_mes.objects.get(id=self.kwargs['pk'])
        gastos= Egreso.objects.filter(corte_mes= self.kwargs['pk']).order_by("id")
        total = Egreso.objects.totalizar_gastos_mes(self.kwargs["pk"]) #ESTOY PASANDO EL MES
        #total1 = "{:,}".format(total).replace(',','.')
        data = {
            'mes': mes,
            'gastos': gastos,
            'total':  "{:,}".format(total)
            #"{:,}".format(total).replace(',','.')
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
            'ingresos': Ingreso.objects.filter(corte_mes= self.kwargs['pk']).order_by("id"),
            'total': Ingreso.objects.totalizar_ingreso_mes(self.kwargs["pk"])
        }
        pdf = render_to_pdf('administracion/ingreso/recibo_ingreso.html', data)
        return HttpResponse(pdf, content_type='application/pdf')


#-----------****** FIN VISTA DE INGRESO ********-----------

#---------**********FIN VISTA DE REPORTE**********--------- 

#VISTA LISTA TODO LOS REPORTE POR MES
class ReporteListView(FormView):
    template_name = "administracion/reporte/reporte.html"
    form_class = SeleccionForm
    #context_object_name = "reporte"

    def get_context_data(self, **kwargs):
        context = super(ReporteListView, self).get_context_data(**kwargs)
        mes = self.request.GET.get("mes", '') 
        torre = self.request.GET.get("torre", '')  
        if mes == '' or torre == '':
            context["reporte"] = []
            return context

        context["reporte"] = Reporte.objects.buscar_reporte_mes(mes, torre)
        context["mes"] = Corte_mes.objects.filter(id=mes).first() 
        return context

    
#VISTA PARA CREAR REPORTE
class ReporteCreateView(View):

    def get(self, request, *args, **kwargs):
        
        x = Corte_mes.objects.get(id= self.kwargs["pk"])

        if x.cerrar_mes:
            #print("=====> Entro al if", x.cerrar_mes)
            apart= Apartamento.objects.all()
            for apart in apart:
                if Reporte.objects.filter(apartamento=apart, corte_mes=x).exists():
                    continue
                    # monto = (x.monto_egreso * apart.alicuota/100)
                    # deuda = RegistroDeudas.objects.filter(apartamento=apart).first()
                    # total= monto + deuda.deuda_pagar 
                    # instance = Reporte.objects.filter(apartamento=apart, corte_mes=x).first()
                    # instance.monto = monto
                    # instance.deuda = deuda.deuda_pagar
                    # instance.total_pagar = total 
                    # instance.save()
                else:
                    monto = (x.monto_egreso * apart.alicuota/100)
                    deuda = RegistroDeudas.objects.filter(apartamento=apart).first()
                    #total= monto + deuda.deuda_pagar
                    total= monto + deuda.deuda_ocumulada

                    z = Reporte.objects.create(
                        apartamento = apart,
                        monto = monto,
                        fecha = timezone.now(),
                        corte_mes = x,
                        deuda = deuda.deuda_ocumulada,
                        total_pagar = total,
                    ) 
                    z.save()
                    #print(z)

            return HttpResponseRedirect(
                    reverse(
                    'admin_app:listar_cierre_mes'
                        )
                    )

        return HttpResponseRedirect(
                    reverse(
                        "admin_app:opciones",kwargs={'pk': x.id},)
                    )



#funcion
def reporte_vaucher_pdf(id_reporte):
    reporte = Reporte.objects.get(id=id_reporte)
    gastos=  Egreso.objects.filter(corte_mes = reporte.corte_mes)
    apart =  reporte.apartamento
    propietario = apart.propietario
    mes = reporte.corte_mes
    total= Egreso.objects.totalizar_gastos_mes(mes) 
    reserva = Corte_mes.objects.total_reserva() 
    data = {
            'reporte': reporte,
            'gastos': gastos ,
            'apart' : apart,
            'propietario': propietario,
            "mes": mes,
            'total': "{:,}".format(total), #ESTOY PASANDO EL MES 
            "reserva": reserva 
        }

    pdf = render_to_pdf('administracion/reporte/reporte_vaucher.html', data)
    return pdf

        


#RECIBO POR MES
class ReporteVoucherPdf(View):
    #CREO EL VOUCHER O RECIBO DE EGRESO DEL MES
    
    def get(self, request, *args, **kwargs):
        #reporte_vaucher_pdf(self.kwargs['pk'])
        # reporte = Reporte.objects.get(id=self.kwargs['pk'])
        # gastos=  Egreso.objects.filter(corte_mes = reporte.corte_mes)
        # apart =  reporte.apartamento
        # propietario = apart.propietario
        # mes = reporte.corte_mes
        # total= Egreso.objects.totalizar_gastos_mes(self.kwargs["pk"]) 
        # data = {
        #     'reporte': reporte,
        #     'gastos': gastos ,
        #     'apart' : apart,
        #     'propietario': propietario,
        #     "mes": mes,
        #     'total': Egreso.objects.totalizar_gastos_mes(reporte.corte_mes.id), #ESTOY PASANDO EL MES 
        #     #"reserva": Cierre_mes.objects.total_reserva() 
        # }

        # pdf = render_to_pdf('administracion/reporte/reporte_vaucher.html', data)
        
        return HttpResponse(reporte_vaucher_pdf(self.kwargs['pk']), content_type='application/pdf')


class EnviarReportePDF(View):

    def get(self, request, *args, **kwargs):
        i=0
        reportes = Reporte.objects.filter(corte_mes= self.kwargs['pk']).order_by("id")

        if not reportes: 
            return HttpResponseRedirect(reverse ("admin_app:opciones",kwargs={'pk': self.kwargs['pk']},))

        for reporte in reportes:
            i+=1
            correo = reporte.apartamento.propietario.email
            
            print("", i)
            #print("correo", correo)
            if correo is  "":
                print("correo", correo)
                continue
            else:
                pdf = reporte_vaucher_pdf(reporte.id)
                asunto = "Recibo " + '[' + reporte.apartamento.apartamento + ']'
                mensaje = "Se adjunta el recibo del mes " 
                #email_remitente = "mariaf0821@gmail.com"
                email_remitente = "lastorresedifcio@gmail.com"

                #send_mail(asunto, mensaje, email_remitente, mariaf0821@gmail.com)
                email = EmailMessage(asunto, mensaje, email_remitente, [correo,])
                email.attach("recibo", pdf.getvalue(), "application/pdf")
                email.content_subtype = pdf  # Main content is now text/html
                email.encoding = 'ISO-8859-1'
                email.send()
                print("se envio correo", correo)

        return HttpResponseRedirect(reverse("admin_app:listar_cierre_mes"))



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
        
        if not  instance.cerrar_mes:
 
            # aqui verifico que ingreso no sea vacio
            if  total_egreso is not None:
                instance.monto_egreso = total_egreso
                
            if total_ingreso is not None:
                instance.monto_ingreso = total_ingreso
               
            instance.save()
            
            return HttpResponseRedirect(
                reverse(
                    'admin_app:listar_cierre_mes'
                )
            )
            
        return HttpResponseRedirect(
                reverse(
                    'admin_app:opciones', kwargs={'pk': instance.id},
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
            instance.reserva = total_egreso*0.1
            #print("reserva=====>", instance.reserva)
            x = Egreso.objects.crear_egreso(instance)

            total_egreso = Egreso.objects.totalizar_gastos_mes(self.kwargs["pk"])
            # aqui verifico que no hallas errores
            if  total_egreso is not None:
                instance.monto_egreso = total_egreso

            if total_ingreso is not None:
                instance.monto_ingreso = total_ingreso
                
            instance.cerrar_mes = True
            instance.save()

            #print("se actualizo perfectamente", instance)

            return HttpResponseRedirect(
                reverse(
                    'admin_app:listar_cierre_mes'
                )
            )
        
        #si se cerro el mes nos deberia a crear otro ves o hacer una accion
        return HttpResponseRedirect(
                reverse(
                    'admin_app:opciones', kwargs={'pk': instance.id},
                )
            )

#---------********VISTA DE CIERRE MES *******--------------------


#--------*********VISTA A LISTAR POR TORRES *******------------- 

class ReporteTorreA(DetailView):
    model = Corte_mes
    template_name = "administracion/reporte/reporteTorres.html"
    
    def get_context_data(self, **kwargs):
        context = super(ReporteTorreA, self).get_context_data(**kwargs)
        context["reporte"] = Reporte.objects.filter(apartamento__torre=1, corte_mes=self.kwargs["pk"]).order_by('id')
        context["mes"] = Corte_mes.objects.get(id= self.kwargs["pk"])
        context["torre"] = Apartamento.objects.filter(torre=1).first()
        return context
    
        
class ReporteTorreB(DetailView):
    model = Corte_mes
    template_name = "administracion/reporte/reporteTorres.html"
    #context_object_name = "reporte"
    def get_context_data(self, **kwargs):
        context = super(ReporteTorreB, self).get_context_data(**kwargs)
        context["reporte"] = Reporte.objects.filter(apartamento__torre=2, corte_mes=self.kwargs["pk"]).order_by('apartamento')
        context["mes"] = Corte_mes.objects.get(id= self.kwargs["pk"])
        context["torre"] = Apartamento.objects.filter(torre=2).first()

        return context


class ReporteAlquiler(DetailView):
    model = Corte_mes
    template_name = "administracion/reporte/reporteTorres.html"
    
    def get_context_data(self, **kwargs):
        context = super(ReporteAlquiler, self).get_context_data(**kwargs)
        context["reporte"] = Reporte.objects.filter(apartamento__torre=3, corte_mes=self.kwargs["pk"]).order_by('apartamento')
        context["mes"] = Corte_mes.objects.get(id= self.kwargs["pk"])
        context["torre"] = Apartamento.objects.filter(torre=3).first()

        return context

#--------********* FIN VISTA A LISTAR POR TORRES *******------------- 


