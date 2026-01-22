from django.contrib import admin
from .models import Caso, Intervencion, Tarea

# Configuración opcional para ver mejor los datos en el admin
class IntervencionInline(admin.TabularInline):
    model = Intervencion
    extra = 0 # No muestra filas vacías extra

class CasoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'cliente', 'estado', 'fecha_creacion')
    list_filter = ('estado', 'fecha_creacion')
    search_fields = ('titulo', 'cliente__username')
    inlines = [IntervencionInline] # Permite ver intervenciones dentro del Caso

admin.site.register(Caso, CasoAdmin)
admin.site.register(Intervencion)
admin.site.register(Tarea)