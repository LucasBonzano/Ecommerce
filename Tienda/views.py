from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login, logout
from django.contrib.sessions.models import Session
from django.utils.timezone import now
from .models import Comprador, Perfumes
from django.shortcuts import render
from Ecommerce.utils import validar_sesion
from Carrito.views import sincronizar_carrito_post_login
from django.contrib.auth import authenticate, login

def Iniciar_Sesion(request):
    if request.method == "POST":
        gmail = request.POST.get('gmail')
        password = request.POST.get('password')

        try:
            user = Comprador.objects.get(gmail=gmail)
        except Comprador.DoesNotExist:
            return render(request, 'Iniciar_sesion.html')
        
        if check_password(password, user.password):
            login(request, user)
            request.session['last_login'] = now().isoformat()
            return redirect('Productos')
        else:
            return render(request, 'Iniciar_sesion.html')

    return render(request, 'Iniciar_sesion.html')


@validar_sesion
def logout_view(request):
    logout(request)
    return redirect('Login')

def Register(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        photo = request.POST.get('photo')  # Si es un archivo, usa request.FILES
        
        # Verificar si el correo o el usuario ya existe
        if Comprador.objects.filter(gmail=email).exists():
            messages.error(request, "El correo ya está registrado. Intenta con otro.")
            return render(request, 'Register.html')

        if Comprador.objects.filter(usuario=username).exists():
            messages.error(request, "El nombre de usuario ya está en uso. Intenta con otro.")
            return render(request, 'Register.html')
        
        # Crear usuario
        user = Comprador.objects.create_user(
            usuario=username,
            contraseña=password,
            gmail=email,
            link_foto=photo
        )
        
        messages.success(request, "Usuario registrado exitosamente.")
        return redirect('Login')  # Cambia esta URL según sea necesario
    
    return render(request, 'Register.html')

@validar_sesion

def Productos(request):
    perfumes = Perfumes.objects.filter(disponible = True)
    return render(request, 'Productos.html', {'perfumes' : perfumes})

def Inicio(request):
    return render(request, 'Inicio.html', {})

def Nosotros(request):
    return render(request, 'Nosotros.html', {})

