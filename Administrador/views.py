from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render
from Ecommerce.utils import validar_sesion_Admin
from django.contrib.auth import authenticate, login
from Tienda.models import Perfumes
from .Form import PerfumeForm



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

@validar_sesion_Admin
def ProductosAdmin(request):
    productos = Perfumes.objects.all()
    return  render(request, 'ProductosAdmin.html',  {'productos': productos})

@validar_sesion_Admin
def agregar_perfume(request):
    if request.method == 'POST':
        # Capturar los datos enviados desde el formulario
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        notas = request.POST.get('notas')
        categoria = request.POST.get('categoria')
        precio = request.POST.get('precio')
        cantidad = request.POST.get('cantidad')
        disponible = 'disponible' in request.POST  # Checkbox devuelve True si está marcado
        imagen = request.POST.get('imagen')
        
        # Validar datos si es necesario (opcional)
        if not nombre or not descripcion or not categoria or not precio or not cantidad:
            messages.error(request, "Todos los campos son obligatorios.")
            return redirect('cargar_perfume')
        
        try:
            # Crear un nuevo objeto Perfume
            perfume = Perfumes(
                nombre=nombre,
                descripcion=descripcion,
                notas=notas,
                categoria=categoria,
                precio=precio,
                cantidad=cantidad,
                disponible=disponible,
                imagen=imagen
            )
            perfume.save()  # Guardar en la base de datos
            messages.success(request, "El perfume ha sido cargado exitosamente.")
            return redirect('ProductosAdmin')  # Redirigir después de guardar
        except Exception as e:
            messages.error(request, f"Hubo un error al cargar el perfume: {str(e)}")
            return redirect('agregar_producto')

    return render(request, 'AgregarProducto.html')

@validar_sesion_Admin
def editar_producto(request, producto_id):
    perfume = get_object_or_404(Perfumes, id_producto=producto_id)

    if request.method == 'POST':
        # Capturar los datos enviados desde el formulario
        perfume.nombre = request.POST.get('nombre')
        perfume.descripcion = request.POST.get('descripcion')
        perfume.notas = request.POST.get('notas')
        perfume.categoria = request.POST.get('categoria')
        perfume.precio = request.POST.get('precio')
        perfume.cantidad = request.POST.get('cantidad')
        perfume.disponible = 'disponible' in request.POST  # Checkbox devuelve True si está marcado
        perfume.imagen = request.POST.get['imagen']
        
        try:
            # Guardar los cambios
            perfume.save()
            messages.success(request, "El perfume se ha actualizado correctamente.")
            return redirect('ProductosAdmin')  # Cambia la redirección según sea necesario
        except Exception as e:
            messages.error(request, f"Error al actualizar el perfume: {str(e)}")
    
    return render(request, 'EditarProductos.html', {'perfume': perfume})

@validar_sesion_Admin
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Perfumes, id_producto=producto_id)
    producto.delete()
    messages.success(request, "Producto eliminado exitosamente.")
    return redirect('ProductosAdmin')

@validar_sesion_Admin
def pausar_producto(request, producto_id):
    producto = get_object_or_404(Perfumes, id_producto=producto_id)
    producto.disponible = not producto.disponible
    producto.save()
    estado = "activado" if producto.disponible else "pausado"
    messages.success(request, f"Producto {estado} exitosamente.")
    return redirect('ProductosAdmin')

@validar_sesion_Admin
def EstadisticasAdmin(request):
    return  render(request, 'EstadisticasAdmin.html')

