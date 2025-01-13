from django.db import models
from django.conf import settings
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib import admin

class CompradorManager(BaseUserManager):
    def create_user(self, usuario, contraseña, gmail, link_foto=None):
        if not usuario:
            raise ValueError("El nombre de usuario es obligatorio.")
        if not gmail:
            raise ValueError("El Gmail es obligatorio.")
        
        # Cifrar la contraseña antes de guardar
        hashed_password = make_password(contraseña)
        
        user = self.model(
            usuario=usuario,
            contraseña=hashed_password,
            gmail=gmail,
            link_foto=link_foto
        )
        user.save(using=self._db)
        return user

    def create_superuser(self, usuario, contraseña, gmail, link_foto=None):
        user = self.create_user(usuario, contraseña, gmail, link_foto)
        # Aquí puedes añadir atributos específicos para superusuarios si es necesario
        return user


class Comprador(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.CharField(max_length=150, unique=True)
    contraseña = models.CharField(max_length=128)
    gmail = models.EmailField(unique=True)
    link_foto = models.URLField(blank=True, null=True)

    objects = CompradorManager()  # Usar el administrador personalizado

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
