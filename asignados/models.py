from django.db import models
from autenticacion.models import Empleado, Localidad

# Create your models here.
class Asignacion(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    localidad = models.ForeignKey(Localidad, on_delete=models.CASCADE)
    dia_del_mes = models.PositiveIntegerField()

    def __str__(self):
        return f"Asignación para {self.empleado.username} en {self.localidad.nombre} el día {self.dia_del_mes}"