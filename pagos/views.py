from django.shortcuts import get_object_or_404, render, HttpResponse, redirect
from django.http import JsonResponse
from Carrito.models import Carrito, CarritoItem
from Ecommerce.utils import get_mercado_pago_client
from .models import Compra, CompraItem
from Ecommerce.utils import validar_sesion

@validar_sesion
def procesar_pago(request):
    if request.method == 'POST':
        # Obtener el carrito del usuario actual
        carrito = get_object_or_404(Carrito, usuario=request.user)  # Ajusta si usas autenticación personalizada
        
        # Verificar si el carrito tiene ítems
        items_carrito = carrito.items.all()
        if not items_carrito.exists():
            return JsonResponse({'error': 'El carrito está vacío.'}, status=400)

        # Generar los datos de la preferencia
        preference_data = {
            "items": [
                {
                    "title": item.producto.nombre,          # Nombre del producto
                    "quantity": item.cantidad,             # Cantidad del producto
                    "unit_price": float(item.precio_unitario),  # Precio unitario del producto
                }
                for item in items_carrito
            ],
            "payer": {
                "email": request.user.gmail  # Email del comprador (si está disponible)
            },
            "back_urls": {
                "success": "http://localhost:8000/Pago/PagoExitoso/",
                "failure": "http://localhost:8000/Pago/PagoFallido/",  # URL de fallo
                "pending": "http://localhost:8000/Pago/PagoPendiente/"  # URL de pendiente
            },
            "auto_return": "approved"
        }

        # Inicializar el SDK de Mercado Pago
        sdk = get_mercado_pago_client()
        preference_response = sdk.preference().create(preference_data)
        preference = preference_response["response"]

        # Devolver el punto de inicio para el pago
        if 'init_point' in preference:
            return redirect(preference['init_point'])
        else:
            return redirect('PagoFallido')

@validar_sesion
def PagoExitoso(request):
    """
    Vista que procesa el pago exitoso y registra la compra.
    """
    try:
        # Obtener datos de la redirección
        id_compra = request.GET.get("payment_id")  # ID del pago en Mercado Pago
        estado_pago = request.GET.get("status")  # Estado del pago
        usuario = request.user

        if not id_compra or estado_pago != "approved":
            return HttpResponse("Error al procesar el pago.", status=400)

        # Registrar la compra
        registrar_compra(usuario, id_compra, estado_pago)

        # Mostrar una página de confirmación
        return render(request, "PagoExitoso.html", {"id_compra": id_compra})

    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)

@validar_sesion
def registrar_compra(usuario, id_compra, estado_pago):
    
    # Verificar si la compra ya existe
    compra, creada = Compra.objects.get_or_create(
        usuario=usuario,
        id_compra=id_compra,
        defaults={'estado_pago': estado_pago}
    )

    if not creada:
        # Si la compra ya existe, solo actualizamos el estado del pago
        compra.estado_pago = estado_pago
        compra.save()
        return compra

    # Si la compra es nueva, registrar los productos del carrito
    carrito = Carrito.objects.get(usuario=usuario)
    items_carrito = carrito.items.all()

    for item in items_carrito:
        # Crear el registro del producto en la compra
        CompraItem.objects.create(
            compra=compra,
            producto=item.producto,
            cantidad=item.cantidad,
            precio_unitario=item.precio_unitario
        )

        # Actualizar el stock del producto
        producto = item.producto
        if producto.cantidad >= item.cantidad:
            producto.cantidad -= item.cantidad  # Restar la cantidad comprada
            producto.save()
        else:
            # Si no hay suficiente stock, lanzar una excepción
            raise ValueError(f"No hay suficiente stock para el producto {producto.nombre}.")

    # Limpiar el carrito después de registrar la compra
    carrito.items.all().delete()

    return compra

@validar_sesion
def PagoPendiente(request):
    return render(request, 'PagoPendiente.html')

@validar_sesion
def PagoFallido(request):
    return render(request, 'PagoFallido.html')