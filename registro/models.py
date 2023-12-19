from django.db import models
from autenticacion.models import Abonado, Empleado
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.core.mail import send_mail
from datetime import datetime, timedelta
import locale

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
        if registro_anterior != None:
            print(registro_anterior.lectura_anterior,registro_anterior.lectura_actual,self.lectura_anterior)

        if registro_anterior == None:
            self.lectura_anterior = 0
        elif registro_anterior.lectura_anterior==self.lectura_anterior and registro_anterior.lectura_anterior > 0:
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

def enviar_correo_lectura(lectura):
    from parameters.models import Parameter
    from pagos.models import Pago
    abonado = lectura.abonado
    print(abonado.email)
    m3 = Parameter.objects.filter(codigo="PR-AG").first()
    total_a_pagar = 0
    total_a_pagar += (float(lectura.lectura_actual - lectura.lectura_anterior) * float(m3.valor))

    # Obtener el último pago para el abonado
    ultimo_pago = Pago.objects.filter(abonado=abonado).order_by('-fecha_creacion').first()
    pago = 'No hay registros de pago.' if not ultimo_pago else str(ultimo_pago.cantidad_total_pago)

    if ultimo_pago:
        total_a_pagar += round(float(ultimo_pago.cantidad_total_pago) - float(ultimo_pago.total_abonado),2)

    # Obtener las opciones actualizadas para el campo registro_consumo
    # opciones_registro_consumo = Lectura.objects.filter(abonado=abonado).values('id', 'lectura_actual')
    
    # Establecer la configuración regional a español
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

    # Obtener la fecha actual
    fecha_actual = datetime.now()

    # Calcular el primer día del mes actual
    primer_dia_del_mes_actual = fecha_actual.replace(day=1)

    # Calcular el último día del mes anterior
    ultimo_dia_del_mes_anterior = primer_dia_del_mes_actual - timedelta(days=1)

    # Obtener el mes y el año del mes anterior
    mes_anterior = ultimo_dia_del_mes_anterior.strftime('%B')
    anio_anterior = ultimo_dia_del_mes_anterior.year

    data = {
        'ultimo_consumo': lectura.lectura_actual - lectura.lectura_anterior,
        'ultimo_pago': pago,
        'cantidad_total_pago': total_a_pagar,
        "lectura": lectura,
        "mes" : mes_anterior,
        "anio" : anio_anterior
    }

    subject = 'Nueva Lectura Registrada'
    message = render_to_string('correo_lectura.html', data)
    from_email = settings.EMAIL_HOST_USER
    to_email = [lectura.abonado.email]  # Reemplaza con la dirección de correo a la que deseas enviar el correo
    print("ENVIANDO EMAIL")
    send_mail(subject, message, from_email, to_email, fail_silently=False)

@receiver(post_save, sender=Lectura)
def lectura_post_save(sender, instance, **kwargs):
    print("Señal de post_save ejecutada para Lectura")
    enviar_correo_lectura(instance)