from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render
from Ecommerce.utils import validar_sesion
from django.contrib.auth import authenticate, login
from Tienda.models import Perfumes



def LoginAdmin(request):
    if request.method == "POST":
        name = request.POST['name']
        password = request.POST['password']
        user = authenticate(request, username=name, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            messages.success(request, "¡Bienvenido al panel de administración!")
            return redirect('ProductosAdmin')  # Redirige al panel de control
        else:
            messages.error(request, "Credenciales inválidas o no tienes permisos de administrador.")
    return render(request, 'Login.html')

def ProductosAdmin(request):
    productos = Perfumes.objects.all()
    return  render(request, 'ProductosAdmin.html',  {'productos': productos})

def agregar_producto(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        descripcion = request.POST.get('descripcion', '')
        precio = request.POST['precio']
        Perfumes.objects.create(nombre=nombre, descripcion=descripcion, precio=precio, disponible=True)
        messages.success(request, "Producto agregado exitosamente.")
        return redirect('ProductosAdmin')
    return render(request, 'agregar_producto.html')

def editar_producto(request, producto_id):
    producto = get_object_or_404(Perfumes, id=producto_id)
    if request.method == 'POST':
        producto.nombre = request.POST['nombre']
        producto.descripcion = request.POST.get('descripcion', '')
        producto.precio = request.POST['precio']
        producto.save()
        messages.success(request, "Producto editado exitosamente.")
        return redirect('ProductosAdmin')
    return render(request, 'editar_producto.html', {'producto': producto})

def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Perfumes, id_producto=producto_id)
    producto.delete()
    messages.success(request, "Producto eliminado exitosamente.")
    return redirect('ProductosAdmin')

def pausar_producto(request, producto_id):
    producto = get_object_or_404(Perfumes, id_producto=producto_id)
    producto.disponible = not producto.disponible
    producto.save()
    estado = "activado" if producto.disponible else "pausado"
    messages.success(request, f"Producto {estado} exitosamente.")
    return redirect('ProductosAdmin')

def EstadisticasAdmin(request):
    return  render(request, 'EstadisticasAdmin.html')

