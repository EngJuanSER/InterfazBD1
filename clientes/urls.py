from django.urls import path
from . import views

urlpatterns = [
    path('', views.registro_cliente, name='registro_cliente'),
    path('buscar/', views.buscar_cliente, name='buscar_cliente'),
]
