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
    def _wrapped_view(request, *args, **kwargs):
        # Verifica si hay una sesión activa
        if not request.user.is_authenticated:
            return redirect('LoginAdmin')  # Redirige a la página de login de administradores

        # Verifica si el usuario es superusuario (administrador)
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            # Opcional: Redirigir o lanzar error
            raise PermissionDenied  # También podrías usar redirect('otra_vista') si prefieres
    return _wrapped_view