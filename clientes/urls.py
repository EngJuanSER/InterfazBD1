"""
URLs para el Sistema de Gestion Legal
"""
from django.urls import path
from . import views
# from .debug_views import debug_data

app_name = 'clientes'

urlpatterns = [
    # DEBUG (temporal)
    # path('debug/', debug_data, name='debug_data'),
    
    # Registro de Clientes
    path('', views.registro_cliente, name='registro_cliente'),
    path('buscar/', views.buscar_cliente, name='buscar_cliente'),
    path('guardar/', views.guardar_cliente, name='guardar_cliente'),
    path('eliminar/', views.eliminar_cliente, name='eliminar_cliente'),
    
    # Gestion de Casos
    path('caso/', views.gestion_caso, name='gestion_caso'),
    path('caso/buscar-cliente/', views.buscar_cliente_caso, name='buscar_cliente_caso'),
    path('caso/obtener-casos/', views.obtener_casos_cliente, name='obtener_casos_cliente'),
    path('caso/detalle/', views.obtener_detalle_caso, name='obtener_detalle_caso'),
    path('caso/siguiente-numero/', views.obtener_siguiente_nocaso, name='obtener_siguiente_nocaso'),
    path('caso/crear/', views.crear_caso, name='crear_caso'),
    path('caso/imprimir/', views.imprimir_caso, name='imprimir_caso'),
    
    # Gestion de Expedientes
    path('expediente/', views.gestion_expediente, name='gestion_expediente'),
    path('expediente/obtener-caso/', views.obtener_caso_expediente, name='obtener_caso_expediente'),
    path('expediente/obtener-expedientes/', views.obtener_expedientes_caso, name='obtener_expedientes_caso'),
    path('expediente/abogados/', views.obtener_abogados_especializacion, name='obtener_abogados_especializacion'),
    path('expediente/entidades/', views.obtener_entidades_ciudad, name='obtener_entidades_ciudad'),
    path('expediente/primera-etapa/', views.obtener_primera_etapa, name='obtener_primera_etapa'),
    path('expediente/siguiente-etapa/', views.obtener_siguiente_etapa, name='obtener_siguiente_etapa'),
    path('expediente/proximo-consecutivo/', views.obtener_proximo_consecutivo, name='obtener_proximo_consecutivo'),
    path('expediente/crear/', views.crear_expediente, name='crear_expediente'),
    path('expediente/detalle/', views.obtener_expediente_detalle, name='obtener_expediente_detalle'),
    path('expediente/guardar-suceso/', views.guardar_suceso, name='guardar_suceso'),
    path('expediente/guardar-resultado/', views.guardar_resultado, name='guardar_resultado'),

    # Impugnaciones válidas según especialización e instancia
    path('expediente/impugnaciones_validas/', views.impugnaciones_validas, name='impugnaciones_validas'),
]

