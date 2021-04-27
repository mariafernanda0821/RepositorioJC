from django.contrib import admin
from django.urls import path, re_path, include
from . import views

app_name = "edificio_app"
urlpatterns = [
    path("apart-torres/<torre>/", views.AparTorresView.as_view(), name = "apart_torres"), 
    path("apart-torreB/", views.AparTorreBView.as_view(), name = "apart_torreB"), 
    path("alquiler/", views.AlquilerView.as_view(), name = "alquilers"),  

    path("detail-apart/<pk>/",views.RegistroPagoApar.as_view(), name = "detail_apart"),  
    path("detail-repote/<pk>/",views.RegistroReporte.as_view(), name = "detail_reporte"), 

    path("apartamento-pdf/",views.ApartamentoPDF.as_view(), name = "apartamento_pdf"),  


    

]