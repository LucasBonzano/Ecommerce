from django.db import models
from django.conf import settings

class Comprador(models.Model):
    id = models.AutoField(primary_key=True)  # ID único y auto incremental
    usuario = models.CharField(max_length=150, unique=True)  # Nombre de usuario único
    contraseña = models.CharField(max_length=128)  # Almacena contraseñas cifradas
    gmail = models.EmailField(unique=True)  # Gmail único para cada usuario
    link_foto = models.URLField(blank=True, null=True)  # Enlace opcional a una foto alojada (ej. Cloudflare)

    def __str__(self):
        return self.usuario

class Perfumes(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    notas = models.TextField()
    categoria = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.URLField(blank=True, null=True)
    id_vendedor = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Relación con el modelo de usuarios
        on_delete=models.CASCADE,
        related_name="productos"
    )
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return self.nombre


