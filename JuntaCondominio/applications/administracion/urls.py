from django.contrib import admin
from django.urls import path, re_path, include
from . import views

app_name = "admin_app"
urlpatterns = [
    path(
        'corte-mes/',
        views.CierreMesListView.as_view(),
        name = "listar_cierre_mes",
    ),
    path(
        'agregar-anotacion/',
        views.AgregarMesNota.as_view(),
        name="agregar_nota",
    ),
    path(
        'opcion/<pk>/',
        views.OpcionesView.as_view(),
        name = "opciones",
    ),
    path(
        'codigo-egreso-add/', 
        views.CodigoAcceso.as_view(), 
        name="codigo_egreso_add",
    ),
    path(
        'egreso-add/', 
        views.EgresoCreateView.as_view(), 
        name="egreso-add",
    ), 

    path(
        'detail-egreso/<pk>/', 
        views.EgresoMesDetailView.as_view(), 
        name="detail_egreso_mes",
    ), 
    path(
        'update-egreso/<pk>/', #actualizar un gasto
        views.EgresoUpdateView.as_view(),
        name = 'update_egres',
    ),

    path(
        'delete-egreso/<pk>', #para eliminar un gasto
        views.EgresoDeleteView.as_view(),
        name = "delete_egreso",
    ),
    path(
        'enviar-egreso/<pk>', #para eliminar un gasto
        views.EnviarEgresoPDF.as_view(),
        name = "enviar_egreso",
    ),
    path(
        'generar-recibo-egreso-mes/<pk>', 
        views.EgresoMesPdf.as_view(), 
        name="recibo_egreso_mes",
    ), 
    path(
        'actualizar-egresos/<pk>',
        views.CierreMesUpdateView.as_view(),
        name= "update_mes",
    ),
    path(
        'listar-reporte/',
        views.ReporteListView.as_view(),
        name = 'listar_reporte',
    ),
    path(
        'enviar-reporte-general/<pk>/<torre>/',
        views.ReporteGeneralPdf.as_view(),
        name = "reporte_general_pdf",
    ),

    path(
        'crear-reporte/<pk>/',
        views.ReporteCreateView.as_view(),
        name = "crear_reporte",
    ),
    path(
        'recibo-pdf/<pk>/',
        views.ReporteVoucherPdf.as_view(),
        name = "recibo_pdf",
    ),
    path(
        'enviar-pdf/<pk>/',
        views.EnviarReportePDF.as_view(),
        name = "enviar_pdf",
    ),

    path(
        'enviar-pdf-individual/<pk>/',
        views.EnviarPDF.as_view(),
        name = "enviar_individual_pdf",
    ),

    path(
        'reporte-mes-torreA/<pk>/',
        views.ReporteTorreA.as_view(),
        name = "reporte_torreA",
    ),
    path(
        'reporte-mes-torreB/<pk>/',
        views.ReporteTorreB.as_view(),
        name = "reporte_torreB",
    ),
    path(
        'reporte-alquiler/<pk>/',
        views.ReporteAlquiler.as_view(),
        name = "reporte_alquiler",
    ),

    path(
        "informe-alquiler-pdf/<int:pk>",
        views.InformeAlquilerPdf.as_view(),
        name="informe_alquiler_pdf"
    ),


    # corte de mes 
    path(
        'cerrar-mes/<pk>/',
        views.CerrarMesUpdateView.as_view(),
        name= "cerrar_mes",
    ),
    
    path(
        'crear-mes/',
        views.CierreMesCreateView.as_view(),
        name= "crear_mes",
    ),

    #URL DE INGRESOS
    path(
        'ingreso-add/',
        views.IngresoCreateView.as_view(),
        name="ingreso_add",
    ),
    path(
        'ingreso-mes/<pk>/', 
        views.IngresoMesDetailView.as_view(),
        name="detail_ingreso_mes",
    ),
    path(
        'ingreso-pdf/<pk>/', 
        views.IngresoMesPdf.as_view(),
        name="recibo_ingreso",
    ),

    path('generar-reportes/<int:pk>/<torre>/',
    views.ReporteDetailView.as_view(),
    name="generar_reportes",
    )

]