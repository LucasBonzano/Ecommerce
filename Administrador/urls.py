from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    #path('', admin.site.urls),
    path('Login/', views.LoginAdmin, name="LoginAdmin"),
    path('ProductosAdmin/', views.ProductosAdmin, name="ProductosAdmin"),
    path('ProductosAdmin/agregar/', views.agregar_perfume, name='agregar_producto'),
    path('ProductosAdmin/editar/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('ProductosAdmin/eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    path('ProductosAdmin/pausar/<int:producto_id>/', views.pausar_producto, name='pausar_producto'),
    path('Estadisticas/', views.EstadisticasAdmin, name="EstadisticasAdmin"),
]