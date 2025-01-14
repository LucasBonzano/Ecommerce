from django.shortcuts import redirect

def validar_sesion(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_id'):  # Verifica si hay un ID de usuario en la sesión
            return redirect('Login')  # Cambia 'Login' al nombre de tu vista de inicio de sesión
        return view_func(request, *args, **kwargs)
    return wrapper
