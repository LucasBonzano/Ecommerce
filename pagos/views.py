from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from Carrito.models import Carrito, CarritoItem
from Ecommerce.utils import get_mercado_pago_client

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
                "success": "http://tusitio.com/pago_exitoso",  # URL de éxito
                "failure": "http://tusitio.com/pago_fallido",  # URL de fallo
                "pending": "http://tusitio.com/pago_pendiente"  # URL de pendiente
            },
            "auto_return": "approved"
        }

        # Inicializar el SDK de Mercado Pago
        sdk = get_mercado_pago_client()
        preference_response = sdk.preference().create(preference_data)
        preference = preference_response["response"]

        # Limpiar el carrito (opcional: hacerlo después de confirmar el pago)
        carrito.items.all().delete()

        # Devolver el punto de inicio para el pago
        if 'init_point' in preference:
            return JsonResponse({'init_point': preference['init_point']})
        else:
            return JsonResponse({'error': 'No se pudo generar la preferencia de pago.', 'detalle': preference_response}, status=400)
