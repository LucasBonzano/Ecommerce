from django.shortcuts import render

# views.py
from django.shortcuts import render
from django.http import JsonResponse
from Ecommerce.utils import get_mercado_pago_client

def create_preference(request):
    if request.method == "POST":
        sdk = get_mercado_pago_client()
        # Define los datos del pago
        preference_data = {
            "items": [
                {
                    "title": "Producto 1",
                    "quantity": 1,
                    "unit_price": 100.0,
                    "currency_id": "ARS",  # Cambia según tu moneda
                }
            ],
            "payer": {
                "email": "comprador@correo.com",  # Cambia por el correo del usuario
            },
            "back_urls": {
                "success": "http://localhost:8000/pago-exitoso/",  # Cambia por tu URL de éxito
                "failure": "http://localhost:8000/pago-fallido/",  # Cambia por tu URL de fallo
                "pending": "http://localhost:8000/pago-pendiente/",  # Cambia por tu URL de pendiente
            },
            "auto_return": "approved",
        }

        # Crea la preferencia
        preference_response = sdk.preference().create(preference_data)
        preference = preference_response["response"]
        return JsonResponse({
            "id": preference["id"],
            "init_point": preference["init_point"],
        })

    return JsonResponse({"error": "Método no permitido"}, status=405)

from django.conf import settings

def pago(request):
    return render(request, "pago.html", {"public_key": settings.MERCADO_PAGO_PUBLIC_KEY})
