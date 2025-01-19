from django.urls import path
from . import views

urlpatterns = [
    path("create_preference/", views.procesar_pago, name="create_preference"),
]
