# python
import datetime
from datetime import timedelta
from decimal import *

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
    EgresoForm, SeleccionForm, IngresoForm, CierreMesForm, CodigoAccesoForm, CodigoAcceso2Form
    )
#
from .models import *
from applications.edificio.models import * 
from applications.deuda.models import * 

from .functions import (
    reporte_vaucher_pdf, reporte_alquiler_pdf, enviar_correos,crear_codigo,
    reportes_general_pdf, update_corte_mes, informe_alquiler_pdf, egreso_pdf,
    )

from applications.usuario.mixins import AdminPermisoMixin, UsuarioPermisoMixin
#VISTA PRINCIPAL


class AgregarMesNota(View):
    def post(self, request, *args, **kwargs):
        nota=self.request.POST.get("nota")
        mes=self.request.POST.get("mes")
        nota_bool = update_corte_mes(
            self = self,
            mes= self.request.POST.get("mes"),
            nota= self.request.POST.get("nota"),
        )
        if not nota_bool:
            return HttpResponse("Hubo un error en agregar nota, ya que el mes no existe")
        
        #print("nota", nota_bool)
        return HttpResponseRedirect(
                reverse(
                    'admin_app:listar_cierre_mes'
                    )
                )

   

class CierreMesListView(UsuarioPermisoMixin,ListView):
    template_name = "administracion/cierre_mes/listar_cierre_mes.html"
    context_object_name = "cierre_mes"
    def get_queryset(self):

        return Corte_mes.objects.all().exclude(id__in=[1,2]).order_by("mes")
    


#VISTA DE OPCIONES PARA LISTAR O AGREGAR:
class OpcionesView(UsuarioPermisoMixin,DetailView):
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

        context["mes"] = Corte_mes.objects.get(id=self.kwargs['pk'])

        return context
    


class CodigoAcceso(AdminPermisoMixin,View):
 
    def post(self, request, *args, **kwargs):
        #print("guarde")
        #print("=====>",self.request.POST.get("codigo_acceso"))
        #print("=====>",self.request.POST.get("codigo_nombre"))
        codigo = crear_codigo(
            self = self,
            codigo= self.request.POST.get("codigo_acceso"),
            nombre= self.request.POST.get("codigo_nombre"),
        )
        if not codigo:
            return HttpResponse("Hubo un error en agregar codigo de acceso")
        
        return HttpResponseRedirect(
                reverse(
                    'admin_app:egreso-add'
                )
            )


#----------*****EGRESO*****----------------
#VISTA AGREGAR UN INGRESO 
class EgresoCreateView(AdminPermisoMixin,CreateView):
    template_name = "administracion/egreso/egreso_add.html"
    form_class = EgresoForm
    success_url=  '.'

    def form_valid(self, form):
        egreso = form.save(commit = False)
        montoDolar = form.cleaned_data["monto_dolar"] 
        precioDolar = form.cleaned_data["precio_dolar"] 
        if montoDolar !=0 and precioDolar !=0: 
            egreso.monto = montoDolar * precioDolar
            egreso.save()

        #egreso.save()    
        return super(EgresoCreateView, self).form_valid(form)
        

#VISTA DETALLA LOS EGRESO POR MES
class EgresoMesDetailView(UsuarioPermisoMixin,DetailView):
    template_name = "administracion/egreso/detail_egreso_mes.html"
    model = Corte_mes
    
    def get_context_data(self, **kwargs):
        context = super(EgresoMesDetailView, self).get_context_data(**kwargs)
        context["fecha"] = timezone.now()
        context['monto_total']= Egreso.objects.totalizar_gastos_mes(self.kwargs['pk'])
        context["mes"] = Corte_mes.objects.get(id= self.kwargs['pk'])
        context["gastos_mes"] = Egreso.objects.buscar_gasto_por_mes(self.kwargs['pk'])
        
        return context


#VISTA PARA MODIFIAR UN GASTO
class EgresoUpdateView(AdminPermisoMixin,UpdateView):
    template_name = "administracion/egreso/update_egreso.html"
    model = Egreso
    form_class = EgresoForm
    success_url = "."
    def form_valid(self, form):
        egreso = form.save(commit = False)
        montoDolar = form.cleaned_data["monto_dolar"] 
        precioDolar = form.cleaned_data["precio_dolar"] 
        #print("=====>", montoDolar )
       # print("=====>",precioDolar )

        if montoDolar !=0 and precioDolar !=0: 
            egreso.monto = montoDolar * precioDolar
            egreso.save()
        
        #egreso.save()
        return super(EgresoUpdateView, self).form_valid(form)
        

    # def get_success_url(self):
    #     return reverse("admin_app:update_egres", args=(self.object.id,))



#VISTA PARA ELIMINAR UN GASTO
class EgresoDeleteView(AdminPermisoMixin,DeleteView):
    model = Egreso
    success_url = reverse_lazy("admin_app:listar_cierre_mes")



#VISTA QUE GENERA INFORME DEL GASTO DEL MES
class EgresoMesPdf(UsuarioPermisoMixin,View):
    #SE VA A GENERAR EL RECIBO DEL MES CORRESPONDIENTE, se debe actualiza ante de generar el pdf
    #
    def get(self, request, *args, **kwargs):
        pdf = egreso_pdf(self.kwargs['pk'])
        return HttpResponse(pdf, content_type='application/pdf')


class EnviarEgresoPDF(UsuarioPermisoMixin,View):
    #enviar el deudas
    def get(self, request, *args, **kwargs):
        pdf = egreso_pdf(self.kwargs['pk'])
        asunto = "Informe General de Gasto"
        mensaje = "Se adjunta los gastos"
        titulo="gastos.pdf"
        #correo=["mariadelsocorro2108@gmail.com","miguelgonzalez2112@gmail.com"]
        correo = ["mariaf0821@gmail.com","mariaf0821@gmail.com"]
        if enviar_correos(pdf,asunto,mensaje, correo, titulo):
            #print("=========> se envio el correo")
            return HttpResponse("Se envio correo exitosamente")
        else:    
            return HttpResponse("Ocurrio un error al enviar el correo")


#-----------****** FIN VISTA DE EGRESO ********-----------


#----------***** Vista de Ingreso*******--------------

#VISTA AGREGAR UN INGRESO 
class IngresoCreateView(AdminPermisoMixin,CreateView):
    template_name = "administracion/ingreso/ingreso_add.html"
    form_class = IngresoForm
    success_url=  '.'


#VISTA DETALLA LOS INGRESO POR MES
class IngresoMesDetailView(UsuarioPermisoMixin,DetailView):
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
class IngresoMesPdf(UsuarioPermisoMixin,View):
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
class ReporteListView(UsuarioPermisoMixin,FormView):
    template_name = "administracion/reporte/reporte_filter.html"
    form_class = SeleccionForm
    #context_object_name = "reporte"

    def get_context_data(self, **kwargs):
        context = super(ReporteListView, self).get_context_data(**kwargs)
        mes = self.request.GET.get("mes", '') 
        torre = self.request.GET.get("torre", '')  
        if mes == '' or torre == '':
            context["reporte"] = []
            return context

        context["reporte"] = Reporte.objects.buscar_reporte_mes(mes, torre).order_by('apartamento')
        context["mes"] = Corte_mes.objects.filter(id=mes).first() 
        return context

    
#VISTA PARA CREAR REPORTE
class ReporteCreateView(AdminPermisoMixin,View):

    def get(self, request, *args, **kwargs):
        
        x = Corte_mes.objects.get(id= self.kwargs["pk"])

        if x.cerrar_mes:
            #print("=====> Entro al if", x.cerrar_mes)
            apart= Apartamento.objects.all().order_by('apartamento')
            for apart in apart:
                if Reporte.objects.filter(apartamento=apart, corte_mes=x).exists():
                    continue
                    # monto = (x.monto_egreso * apart.alicuota/100)
                    # deuda = RegistroDeudas.objects.filter(apartamento=apart).first()
                    # monto_deuda = deuda.deuda_pagar 
                    # total= monto + deuda.deuda_pagar
                    # instance = Reporte.objects.filter(apartamento=apart, corte_mes=x).first()
                    # instance.monto = monto
                    # instance.deuda = deuda.deuda_pagar
                    # instance.total_pagar = total 
                    # instance.save()
                else:
                    monto = (x.monto_egreso * apart.alicuota/100)
                    deuda = RegistroDeudas.objects.filter(apartamento=apart).first()
                    #monto_deuda = deuda.deuda_pagar 
                    total= monto + deuda.deuda_pagar
                    #total= monto + deuda.deuda_ocumulada

                    z = Reporte(
                        apartamento = apart,
                        monto = monto,
                        fecha = timezone.now(),
                        corte_mes = x,
                        deuda = deuda.deuda_pagar ,
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


#RECIBO POR MES FORMATO PDF
class ReporteVoucherPdf(UsuarioPermisoMixin,View):
    #CREO EL VOUCHER O RECIBO DE EGRESO DEL MES individual
    def get(self, request, *args, **kwargs):
        reporte = Reporte.objects.get(id=self.kwargs['pk'])
        if reporte.apartamento.torre == '3':

            return HttpResponse(reporte_alquiler_pdf(self.kwargs['pk']), content_type='application/pdf')

        return HttpResponse(reporte_vaucher_pdf(self.kwargs['pk']), content_type='application/pdf')


# reportes general se debe enviar a los administradores
class ReporteGeneralPdf(UsuarioPermisoMixin,View):
    #CREO EL VOUCHER O RECIBO DE EGRESO DEL MES individual
    def get(self, request, *args, **kwargs):
        #reportes_pdf(id_mes, id_torre)
        pdf = reportes_general_pdf(self.kwargs['pk'],self.kwargs['torre'])
        
        return HttpResponse(pdf, content_type='application/pdf')


class InformeAlquilerPdf(UsuarioPermisoMixin,View):
    #CREO EL VOUCHER O RECIBO DE EGRESO DEL MES individual
    def get(self, request, *args, **kwargs):
        #reportes_pdf(id_mes, id_torre)
        pdf = informe_alquiler_pdf(self.kwargs["pk"])
        
        return HttpResponse(pdf, content_type='application/pdf')


class EnviarReportePDF(AdminPermisoMixin,View):

    def get(self, request, *args, **kwargs):
        i=0
        reportes = Reporte.objects.filter(corte_mes= self.kwargs['pk']).exclude(apartamento__torre="3").order_by("id")

        if not reportes: 
            return HttpResponseRedirect(reverse ("admin_app:opciones",kwargs={'pk': self.kwargs['pk']},))

        for reporte in reportes:
            i+=1
            correo = reporte.apartamento.propietario.email
            
            print(" ", i)
            if correo is  "":
                print("correo vacio =======>", correo)
                continue
            else:
                pdf = reporte_vaucher_pdf(reporte.id)
                asunto = "Recibo " + '[' + reporte.apartamento.apartamento + ']' + '[ mes ' + reporte.corte_mes.mes + ']'
                mensaje = "Se adjunta nuevamente el recibo del mes." 
                titulo = "recibo.pdf"
                enviar_correos(pdf,asunto,mensaje, correo, titulo)
                print("se envio correo", correo) 
                
        #return HttpResponseRedirect(reverse("admin_app:listar_cierre_mes"))
        return HttpResponse("Se envio  todo los correos adecuadamente")


#enviar de manera independiente
class EnviarPDF(UsuarioPermisoMixin,View):
    def get(self, request, *args, **kwargs):
        pdf = reporte_vaucher_pdf(self.kwargs['pk'])
        x = Reporte.objects.filter(id=self.kwargs['pk']).first()
        correo = x.apartamento.propietario.email
        asunto = "Recibo " + '[' + x.apartamento.apartamento + ']' + '[ mes ' + x.corte_mes.mes + ']'
        mensaje = "Se adjunta el recibo del mes " 
        titulo = "recibo.pdf"
        enviar_correos(pdf, asunto, mensaje, correo, titulo)
        print("se envio correo", correo)
      
        #return HttpResponse(reporte_vaucher_pdf(self.kwargs['pk']), content_type='application/pdf')
        return HttpResponse("Se envio el correo electronico")


# class EnviarReporteGeneralPDF(UsuarioPermisoMixin,View):
#     def get(self, request, *args, **kwargs):
#         pdf = 
#         x = 
#         correo = 
#         asunto = "Reportes General" 
#         mensaje = "Se adjunta el Reportes General del mes " 
#         titulo = "reportes.pdf"
#         enviar_correos(pdf, asunto, mensaje, correo, titulo)
#         print("se envio correo", correo)
      
#         return HttpResponse(, content_type='application/pdf')


#---------**********FIN VISTA DE REPORTE**********-------------- 

#---------********VISTA DE CIERRE MES *******--------------------

#VISTA CREAR CORTE_MES 
class CierreMesCreateView(AdminPermisoMixin, CreateView):
   # model = Corte_mes
    template_name = "administracion/cierre_mes/crear_mes.html"
    form_class = CierreMesForm
    success_url = reverse_lazy("admin_app:listar_cierre_mes")





#VISTA ACTUALIZAR TODO EL MES
class CierreMesUpdateView(UsuarioPermisoMixin,View):
    #actualizar los gastos e ingresos del cierre del mes correspondiente
    def get(self, request, *args, **kwargs):
        
        total_egreso = Egreso.objects.totalizar_gastos_mes(self.kwargs["pk"])
        total_ingreso = Ingreso.objects.totalizar_ingreso_mes(self.kwargs["pk"])
        instance = Corte_mes.objects.get(id = self.kwargs["pk"])
        
        if  total_egreso is not None:
            instance.monto_egreso = total_egreso
        else:
            instance.monto_egreso = 0

        if total_ingreso is not None:
            instance.monto_ingreso = total_ingreso
        else:  
            instance.monto_ingreso = 0

        instance.save()
        #print("====>", total_egreso)   
        return HttpResponseRedirect(
            reverse(
                    'admin_app:listar_cierre_mes'
                )
            )
        

#VISTA CERRAR EL MES COMPLETO 
class CerrarMesUpdateView(AdminPermisoMixin,View):
    #ultima actualizancion de mes 
    def get(self, request, *args, **kwargs):
        instance = Corte_mes.objects.get(id = self.kwargs["pk"])

        if not instance.cerrar_mes:
            
            total_egreso = Egreso.objects.totalizar_gastos_mes(self.kwargs["pk"])
            total_ingreso = Ingreso.objects.totalizar_ingreso_mes(self.kwargs["pk"])
            instance.reserva = total_egreso*0.1
            #print("reserva=====>", instance.reserva)
            codigo = CodigoAcceso.objects.get(id=28)
            x = Egreso.objects.crear_egreso(instance, codigo)

            total_egreso = Egreso.objects.totalizar_gastos_mes(self.kwargs["pk"])
            # aqui verifico que no hallas errores
            if  total_egreso is not None:
                instance.monto_egreso = total_egreso
            else:
                instance.monto_egreso = 0

            if total_ingreso is not None:
                instance.monto_ingreso = total_ingreso
            else:  
                instance.monto_ingreso = 0

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

class ReporteDetailView(UsuarioPermisoMixin,ListView):
    model = Corte_mes
    template_name = "administracion/reporte/generar_reportes.html"

    def get_context_data(self, **kwargs):
        context = super(ReporteDetailView, self).get_context_data(**kwargs)
        context["reportes"] = Reporte.objects.filter(apartamento__torre=self.kwargs["torre"], corte_mes=self.kwargs["pk"]).order_by('apartamento')
        context["mes"] = Corte_mes.objects.get(id= self.kwargs["pk"])
        context["torre"] = Apartamento.objects.filter(torre=self.kwargs["torre"]).first()
        return context


class ReporteTorreA(DetailView):
    model = Corte_mes
    template_name = "administracion/reporte/reporteTorres.html"
    
    def get_context_data(self, **kwargs):
        context = super(ReporteTorreA, self).get_context_data(**kwargs)
        context["reporte"] = Reporte.objects.filter(apartamento__torre=1, corte_mes=self.kwargs["pk"]).order_by('apartamento')
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


