from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from functools import wraps
import mercadopago
from django.conf import settings

def get_mercado_pago_client():
    sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)
    return sdk



def validar_sesion(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            # Redirigir a la página de inicio de sesión personalizada
            return redirect('Login')  # Cambia 'Login' por el nombre de tu vista de inicio de sesión
        return view_func(request, *args, **kwargs)
    return wrapper


def validar_sesion_Admin(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Verifica si el usuario está autenticado
        if not request.user.is_authenticated:
            return redirect('LoginAdmin')  # Redirige al login de administradores
        # Verifica si el usuario es superusuario
        if not request.user.is_superuser:
            raise PermissionDenied("No tienes permisos para acceder a esta página.")
        # Llama a la vista original si pasa las validaciones
        return view_func(request, *args, **kwargs)
    return login_required(wrapper)



