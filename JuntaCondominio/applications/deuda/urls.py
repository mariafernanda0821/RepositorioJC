from django.contrib import admin
from django.urls import path, re_path, include
from . import views

app_name = "deuda_app"
urlpatterns = [

    path( 'opcion/', views.OpcionesView.as_view(), name = "opciones",), 
    path( 'crear-referencia/<pk>/', views.CrearReferenciaPago.as_view(), name = "crear_referencia",), 
    path( 'actualizar-referencia/<pk>/', views.ReferenciaPagoUpdateView.as_view(), name = "update_referencia",), 



]