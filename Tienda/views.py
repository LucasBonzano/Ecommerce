from django.shortcuts import render

# Create your views here.

def Productos(request):
    return render(request, 'Productos.html', {})

def Iniciar_Sesion(request):
    return render(request, 'Iniciar_sesion.html', {})