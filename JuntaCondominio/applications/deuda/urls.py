from django.contrib import admin
from django.urls import path, re_path, include
from . import views

app_name = "deuda_app"
urlpatterns = [
    path( 'crear-tabla-deuda/', views.CrearDeudasTabla.as_view(), name = "crear_deuda",), 


    path( 'listar_referencia/', views.ReferenciaView.as_view(), name = "referencia",), 
    path( 'crear-referencia/<pk>/', views.CrearReferenciaPago.as_view(), name = "crear_referencia",), 
    path( 'actualizar-referencia/<pk>/', views.ReferenciaPagoUpdateView.as_view(), name = "update_referencia",), 
    path( 'listar-deudas/', views.RegistroDeudasListView.as_view(), name = "listar_deudas",), 



]