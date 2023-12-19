# pagos/models.py
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
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

def enviar_correo_pago(pago):

    data = {
        "registro_consumo": pago.registro_consumo,
        "cantidad_total_pago": pago.cantidad_total_pago,
        "total_abonado": pago.total_abonado,
        "fecha_creacion": pago.fecha_creacion
    }
    subject = 'Nuevo Pago Registrado'
    message = render_to_string('correo_pago.html', data)
    from_email = settings.EMAIL_HOST_USER
    to_email = [pago.abonado.email]  # Reemplaza con la dirección de correo a la que deseas enviar el correo
    print("ENVIANDO EMAIL PAGO")
    send_mail(subject, message, from_email, to_email, fail_silently=False)

@receiver(post_save, sender=Pago)
def lectura_post_save(sender, instance, **kwargs):
    print("Señal de post_save ejecutada para Lectura")
    enviar_correo_pago(instance)