# pagos/models.py
from django.db import models
from autenticacion.models import Empleado, Abonado
from registro.models import Lectura

class Pago(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    abonado = models.ForeignKey(Abonado, on_delete=models.CASCADE)
    registro_consumo = models.ForeignKey(Lectura, on_delete=models.CASCADE)
    cantidad_total_pago = models.DecimalField(max_digits=10, decimal_places=2)
    total_abonado = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.empleado} - {self.abonado} - {self.fecha_creacion}"
