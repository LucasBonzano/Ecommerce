from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('Productos/', views.Productos, name="Productos"),
    path('Login/', views.Iniciar_Sesion, name="Login"),
    path('Register/', views.Register, name="Register"),
]