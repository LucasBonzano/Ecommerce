from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password


class CompradorManager(BaseUserManager):
    """Manager personalizado para el modelo Comprador."""

    def create_user(self, usuario, contraseña, gmail, link_foto=None, **extra_fields):
        if not usuario:
            raise ValueError("El nombre de usuario es obligatorio.")
        if not gmail:
            raise ValueError("El Gmail es obligatorio.")
        
        # Normaliza el Gmail y cifra la contraseña
        gmail = self.normalize_email(gmail)
        extra_fields.setdefault('is_active', True)
        user = self.model(
            usuario=usuario,
            gmail=gmail,
            link_foto=link_foto,
            **extra_fields
        )
        user.set_password(contraseña)
        user.save(using=self._db)
        return user

    def create_superuser(self, usuario, password, gmail, link_foto=None, **extra_fields):
        """Crear un superusuario con permisos adicionales."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')

        return self.create_user(usuario, password, gmail, link_foto, **extra_fields)


class Comprador(AbstractBaseUser, PermissionsMixin):
    """Modelo de usuario personalizado para Comprador."""
    id = models.AutoField(primary_key=True)
    usuario = models.CharField(max_length=150, unique=True)
    gmail = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    link_foto = models.URLField(blank=True, null=True)

    # Campos requeridos para autenticación
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Manager personalizado
    objects = CompradorManager()

    # Configuración del modelo de usuario
    USERNAME_FIELD = 'gmail'  # Campo principal para autenticación
    REQUIRED_FIELDS = ['usuario']  # Campos obligatorios al crear un superusuario

    def __str__(self):
        return self.usuario


class Perfumes(models.Model):
    """Modelo para productos de Perfumes."""
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    notas = models.TextField()
    categoria = models.CharField(max_length=100)
    precio = models.IntegerField()
    imagen = models.URLField(blank=True, null=True)
    id_admin = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Relación con el modelo de usuarios
        on_delete=models.CASCADE,
        related_name="productos",
        default=1
    )
    cantidad = models.PositiveIntegerField()
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
