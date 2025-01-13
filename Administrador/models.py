from django.db import models

class Administrador(models.Model):
    usuario = models.CharField(max_length=150, unique=True)  # Nombre de usuario único
    contraseña = models.CharField(max_length=128)  # Contraseña cifrada
    gmail = models.EmailField(unique=True)  # Gmail único
    productos_cargados = models.PositiveIntegerField(default=0)  # Cantidad de productos cargados

    def __str__(self):
        return self.usuario