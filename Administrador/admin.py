from django.contrib import admin
from Tienda.models import Comprador, Perfumes


admin.site.register(Comprador)
admin.site.register(Perfumes)

class Perfumes(admin.ModelAdmin):
    list_display = ('id_producto', 'nombre', 'descripcion', 'notas', 'categoria', 'precio', 'imagen', 'id_vendedor', 'cantidad')  # Campos visibles en la lista
    list_editable = ('nombre', 'descripcion', 'notas', 'categoria', 'precio', 'imagen', 'id_vendedor', 'cantidad')  # Campos visibles en la lista
