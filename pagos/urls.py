from django.urls import path
from . import views

urlpatterns = [
    path("create_preference/", views.procesar_pago, name="create_preference"),
    path("PagoPendiente/", views.PagoPendiente, name="PagoPendiente"),
    path("PagoFallido/", views.PagoFallido, name="PagoFallido"),
    path("PagoExitoso/", views.PagoExitoso, name="PagoExitoso"),
]
