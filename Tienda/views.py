
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Comprador
from django.contrib.auth.hashers import check_password

def Productos(request):
    return render(request, 'Productos.html', {})

def Iniciar_Sesion(request):
    if request.method == "POST":
        gmail = request.POST['gmail']
        password = request.POST['password']
        
        try:
            user = Comprador.objects.get(gmail=gmail)  # Busca al usuario por Gmail
        except Comprador.DoesNotExist:
            messages.error(request, "El Gmail ingresado no está registrado.")
            return render(request, 'Iniciar_sesion.html')
        
        # Comparar la contraseña ingresada con la almacenada
        if check_password(password, user.contraseña):
            # Iniciar sesión: guarda datos en la sesión
            request.session['user_id'] = user.id
            messages.success(request, f"Bienvenido, {user.usuario}!")
            return redirect('Productos')  # Redirige a la página deseada
        else:
            messages.error(request, "Contraseña incorrecta.")

    return render(request, 'Iniciar_sesion.html')

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