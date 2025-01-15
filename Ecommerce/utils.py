from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

def validar_sesion(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_id'):  # Verifica si hay un ID de usuario en la sesión
            return redirect('Login')  # Cambia 'Login' al nombre de tu vista de inicio de sesión
        return view_func(request, *args, **kwargs)
    return wrapper

def validar_sesion_Admin(view_func):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_superuser:  # Verifica si es superusuario
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied  # Lanza un error si no tiene permiso
    return _wrapped_view