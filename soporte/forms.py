from django import forms
from django.contrib.auth.models import User
from .models import Caso

class CasoForm(forms.ModelForm):
    class Meta:
        model = Caso
        fields = ['titulo', 'descripcion', 'soporte']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # AQUÍ ESTÁ LA MAGIA:
        # Filtramos para que solo aparezcan usuarios del grupo 'Soporte'
        # o que sean Staff.
        self.fields['soporte'].queryset = User.objects.filter(groups__name='Soporte')
        self.fields['soporte'].label = "Seleccione el Técnico de su preferencia"
        # Hacemos el campo obligatorio si es requisito del negocio
        self.fields['soporte'].required = True