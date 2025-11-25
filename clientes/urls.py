from django.urls import path
from . import views

urlpatterns = [
    path('', views.registro_cliente, name='registro_cliente'),
    path('clientes/', views.registro_cliente, name='registro_cliente_root'),
    path('eliminar_cliente/<str:cod_cliente>/', views.eliminar_cliente, name='eliminar_cliente'),
    
    # Gestion Caso
    path('gestion_caso/', views.gestion_caso, name='gestion_caso'),
    path('api/buscar_cliente/', views.buscar_cliente_api, name='buscar_cliente_api'),
    path('api/listar_casos/', views.listar_casos_api, name='listar_casos_api'),
    path('crear_caso/', views.crear_caso, name='crear_caso'),
    
    # Gestion Expediente
    path('gestion_expediente/', views.gestion_expediente, name='gestion_expediente'),
    path('crear_etapa/', views.crear_etapa, name='crear_etapa'),
]
