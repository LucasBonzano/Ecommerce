from django import forms
from Tienda.models import Perfumes

class PerfumeForm(forms.ModelForm):
    class Meta:
        model = Perfumes
        fields = ['nombre', 'descripcion', 'notas', 'categoria', 'precio', 'imagen', 'cantidad', 'disponible']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
            'notas': forms.Textarea(attrs={'rows': 3}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'nombre': 'Nombre del Perfume',
            'descripcion': 'Descripción',
            'notas': 'Notas del Perfume',
            'categoria': 'Categoría',
            'precio': 'Precio',
            'imagen': 'Imagen',
            'cantidad': 'Cantidad Disponible',
            'disponible': '¿Está Disponible?',
        }
