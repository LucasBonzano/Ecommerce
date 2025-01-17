
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from Carrito.models import Carrito, CarritoItem
from Tienda.models import Perfumes as Producto  # Ajusta según tu modelo

def inicializar_carrito(request):
    if request.user.is_authenticated:
        # Obtener el carrito del usuario o crearlo si no existe
        carrito, creado = Carrito.objects.get_or_create(usuario=request.user)
        request.session['carrito'] = cargar_carrito_desde_bd(carrito)
    elif 'carrito' not in request.session:
        request.session['carrito'] = {}

def sincronizar_carrito_con_bd(request):
    """Sincroniza el carrito de la sesión con la base de datos para el usuario autenticado."""
    if not request.user.is_authenticated:
        # No hacer nada si el usuario no está autenticado
        return

    carrito, creado = Carrito.objects.get_or_create(usuario=request.user)

    # Limpia los ítems actuales en el carrito del usuario
    carrito.items.all().delete()

    # Agrega los ítems desde la sesión
    if 'carrito' in request.session:
        for producto_id, datos in request.session['carrito'].items():
            producto = Producto.objects.get(id_producto=producto_id)
            CarritoItem.objects.create(
                carrito=carrito,
                producto=producto,
                cantidad=datos['cantidad'],
                precio_unitario=producto.precio,
            )

        # Limpia el carrito en la sesión para evitar duplicados
        del request.session['carrito']

def cargar_carrito_desde_bd(carrito):
    carrito_session = {}
    for item in carrito.items.all():
        carrito_session[str(item.producto.id_producto)] = {
            'nombre': item.producto.nombre,
            'precio': float(item.precio_unitario),
            'cantidad': item.cantidad,
            'imagen': item.producto.imagen,
        }
    return carrito_session


def agregar_al_carrito(request, producto_id):
    inicializar_carrito(request)
    producto = get_object_or_404(Producto, id_producto=producto_id)

    carrito = request.session.get('carrito', {})
    if str(producto_id) in carrito:
        carrito[str(producto_id)]['cantidad'] += 1
    else:
        carrito[str(producto_id)] = {
            'nombre': producto.nombre,
            'precio': float(producto.precio),
            'cantidad': 1,
            'imagen': producto.imagen,
        }

    request.session['carrito'] = carrito
    sincronizar_carrito_con_bd(request)  # Sincroniza con la base de datos
    return redirect('ver_carrito')

def ver_carrito(request):
    inicializar_carrito(request)
    carrito = request.session.get('carrito', {})
    total = sum(item['precio'] * item['cantidad'] for item in carrito.values())
    return render(request, 'carrito.html', {'carrito': carrito, 'total': total})



def eliminar_del_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})
    
    # Verifica si el producto está en el carrito de la sesión
    if str(producto_id) in carrito:
        del carrito[str(producto_id)]
        request.session['carrito'] = carrito
        
        # Si el usuario está autenticado, elimina también de la base de datos
        if request.user.is_authenticated:
            try:
                carrito_bd = Carrito.objects.get(usuario=request.user)
                carrito_item = CarritoItem.objects.get(carrito=carrito_bd, producto__id_producto=producto_id)
                carrito_item.delete()
            except (Carrito.DoesNotExist, CarritoItem.DoesNotExist):
                # Ignorar si el carrito o el ítem no existe en la base de datos
                pass

    return redirect('ver_carrito')


def vaciar_carrito(request):
    # Limpia el carrito en la sesión
    request.session['carrito'] = {}
    
    # Si el usuario está autenticado, elimina todos los ítems del carrito en la base de datos
    if request.user.is_authenticated:
        try:
            carrito_bd = Carrito.objects.get(usuario=request.user)
            # Elimina todos los ítems asociados al carrito
            carrito_bd.items.all().delete()
        except Carrito.DoesNotExist:
            # Ignorar si el carrito no existe en la base de datos
            pass

    return redirect('ver_carrito')



def sincronizar_carrito_generico(request, user):
    if 'carrito' in request.session:
        # Obtén o crea el carrito del usuario
        carrito, _ = Carrito.objects.get_or_create(usuario=user)
        # Limpia los ítems actuales en el carrito del usuario
        carrito.items.all().delete()
        # Agrega los ítems desde la sesión
        for producto_id, datos in request.session['carrito'].items():
            producto = Producto.objects.get(id_producto=producto_id)
            CarritoItem.objects.create(
                carrito=carrito,
                producto=producto,
                cantidad=datos['cantidad'],
                precio_unitario=producto.precio,
            )
        # Limpia el carrito en la sesión para evitar duplicados
        del request.session['carrito']


@receiver(user_logged_in)
def sincronizar_carrito_post_login(sender, request, user, **kwargs):
    """Sincroniza automáticamente el carrito después de iniciar sesión."""
    sincronizar_carrito_generico(request, user)
