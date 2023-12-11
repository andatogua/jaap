# tu_proyecto/tu_app/signals/lectura.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .models import Lectura

def enviar_correo_lectura(lectura):
    subject = 'Nueva Lectura Registrada'
    message = render_to_string('correo_lectura.html', {'lectura': lectura})
    from_email = settings.EMAIL_HOST_USER
    to_email = ['andrestogua@gmail.com']  # Reemplaza con la dirección de correo a la que deseas enviar el correo
    print("ENVIANDO EMAIL")
    send_mail(subject, message, from_email, to_email, fail_silently=False)

@receiver(post_save, sender=Lectura)
def lectura_post_save(sender, instance, **kwargs):
    print("Señal de post_save ejecutada para Lectura")
    enviar_correo_lectura(instance)
