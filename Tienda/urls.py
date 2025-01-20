from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('Productos/', views.Productos, name="Productos"),
    path('Login/', views.Iniciar_Sesion, name="Login"),
    path('Register/', views.Register, name="Register"),
    path('Logout/', views.logout_view, name="Logout"),
    path('AboutUs/', views.Nosotros, name="AboutUs"),
    path('HistorialCompras/', views.listar_compras, name='HistorialCompras'),
    path('DetalleCompra/<str:id_compra>/', views.detalle_compra, name='DetalleCompra'),
    path('', views.Inicio, name="Home")
]