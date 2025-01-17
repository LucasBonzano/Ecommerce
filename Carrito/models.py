from django.db import models
from Tienda.models import Perfumes, Comprador  # Cambia según el nombre de tu app de productos

class Carrito(models.Model):
    usuario = models.OneToOneField(Comprador, on_delete=models.CASCADE, related_name="carrito")
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

class CarritoItem(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name="items")
    producto = models.ForeignKey(Perfumes, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)  # Guarda el precio del producto

