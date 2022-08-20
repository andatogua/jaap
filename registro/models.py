from django.db import models
from autenticacion.models import Abonado, Empleado
from django.conf import settings

# Create your models here.


class Lectura(models.Model):
    abonado             = models.ForeignKey(Abonado, on_delete=models.CASCADE)
    empleado            = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    lectura_anterior    = models.FloatField(blank=True,default=0)
    lectura_actual      = models.FloatField()
    fecha               = models.DateTimeField(auto_now_add=True)
    valor_consumo       = models.FloatField(null=True)
    observacion         = models.CharField(max_length=200,blank=True)
    
    def save(self, *args, **kwargs):
        registro_anterior = Lectura.objects.filter(abonado = self.abonado).last()
        print(registro_anterior.lectura_anterior,self.lectura_anterior)
        if registro_anterior == None:
            self.lectura_anterior = 0
        elif registro_anterior.lectura_anterior==self.lectura_anterior:
            pass
        else:
            self.lectura_anterior = registro_anterior.lectura_actual
        consumo = self.lectura_actual - self.lectura_anterior

        if consumo > settings.LIMITEM3:
            self.valor_consumo = (settings.LIMITEM3 * settings.VALORM3) + ((consumo - settings.LIMITEM3)*settings.VALOREXM3)
        elif consumo <= settings.MINIMO:
            self.valor_consumo = 2
        else:
            self.valor_consumo = round(consumo * settings.VALORM3,2)

        return super().save(*args, **kwargs)
    

    def __str__(self):
        return "Lectura {}".format(self.id)

class TipoServicio(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Servicio(models.Model):
    abonado             = models.ForeignKey(Abonado, on_delete=models.CASCADE)
    empleado            = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    tipo_servicio       = models.ForeignKey(TipoServicio, on_delete=models.CASCADE)
    valor_servicio      = models.FloatField()
    fecha               = models.DateTimeField(auto_now_add=True)
    observacion         = models.CharField(max_length=200,blank=True)

    def __str__(self):
        return "{} : {}".format(self.abonado,self.tipo_servicio)

