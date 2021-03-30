from django.contrib import admin
from django.urls import path, re_path, include
from . import views

app_name = "admin_app"
urlpatterns = [
    path(
        '',
        views.CierreMesListView.as_view(),
        name = "listar_cierre_mes",
    ),

    path(
        'opcion/',
        views.OpcionesView.as_view(),
        name = "opciones",
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
        'detallar-gasto/<pk>', #para detallar un gasto
        views.DetallarEgreso.as_view(),
        name = "detallar_gasto",
    ),
    path(
        'delete-egreso/<pk>', #para eliminar un gasto
        views.EgresoDeleteView.as_view(),
        name = "delete_egreso",
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
        'listar-reporte/<pk>',
        views.ReporteListView.as_view(),
        name = 'listar_reporte',
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


]