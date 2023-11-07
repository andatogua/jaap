from django.db import models

# Create your models here.
class Parameter(models.Model):
    codigo = models.CharField(max_length=255)  # Campo para el código
    descripcion = models.TextField()           # Campo para la descripción (texto largo)
    valor = models.DecimalField(max_digits=10, decimal_places=2)  # Campo para el valor numérico
    estado = models.BooleanField(default=True)  # Campo para el estado (activo o inactivo)

    def __str__(self):
        return self.codigo