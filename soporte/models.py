from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Opciones para el estado del caso
ESTADO_CHOICES = [
    ('ABIERTO', 'Abierto'),
    ('CERRADO', 'Cerrado'),
]

class Caso(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    # Relación: Un caso pertenece a un usuario (Cliente)
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='casos')
    soporte = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='casos_asignados',
        verbose_name="Técnico Asignado"
    )
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='ABIERTO')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Caso #{self.id} - {self.titulo}"

class Intervencion(models.Model):
    caso = models.ForeignKey(Caso, on_delete=models.CASCADE, related_name='intervenciones')
    tecnico = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='intervenciones_tecnicas')
    fecha = models.DateTimeField(auto_now_add=True)
    notas = models.TextField()

    def clean(self):
        # REGLA DE NEGOCIO: Solo se pueden registrar intervenciones en casos abiertos.
        if self.caso.estado == 'CERRADO':
            raise ValidationError("No se pueden agregar intervenciones a un caso cerrado.")

    def save(self, *args, **kwargs):
        self.clean() # Forzamos la validación antes de guardar
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Intervención en {self.caso} por {self.tecnico}"

class Tarea(models.Model):
    intervencion = models.ForeignKey(Intervencion, on_delete=models.CASCADE, related_name='tareas')
    descripcion = models.CharField(max_length=255)
    costo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.descripcion