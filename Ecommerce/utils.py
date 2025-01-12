from django.shortcuts import redirect

def validar_sesion(view_func):
    """
    Decorador para validar si un usuario tiene una sesión activa.
    Redirige a la página de inicio de sesión si no está logueado.
    """
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_id'):  # Verifica si hay un ID de usuario en la sesión
            return redirect('Login')  # Cambia 'Login' al nombre de tu vista de inicio de sesión
        return view_func(request, *args, **kwargs)
    return wrapper
