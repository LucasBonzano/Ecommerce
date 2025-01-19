from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from Tienda.models import Perfumes
from Ecommerce import settings

class Compra(models.Model):
    class EstadoPago(models.TextChoices):
        APROBADO = 'approved', _('Aprobado')
        PENDIENTE = 'pending', _('Pendiente')
        RECHAZADO = 'rejected', _('Rechazado')

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="compras")
    id_compra = models.CharField(max_length=100, unique=True)  # ID de la transacción de Mercado Pago
    estado_pago = models.CharField(
        max_length=20,
        choices=EstadoPago.choices,
        default=EstadoPago.PENDIENTE,
    )
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Compra {self.id_compra} - {self.estado_pago}"

class CompraItem(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name="items")
    producto = models.ForeignKey(Perfumes, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad}"
