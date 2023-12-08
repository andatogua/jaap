# tu_app/views.py
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Sum, Func, CharField
from django.db.models.functions import ExtractMonth, ExtractYear
from datetime import datetime, timedelta
from registro.models import Lectura, Servicio
from autenticacion.models import Abonado
from pagos.models import Pago
from .forms import BuscarAbonadoForm
from parameters.models import Parameter

class CustomLoginView(LoginView):
    def get_success_url(self):
        # Personaliza esta URL según tus necesidades
        return '/reportes/dashboard/'


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')

def home_view(request):
    form = BuscarAbonadoForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        cedula = form.cleaned_data['cedula']

        try:
            param_agua = Parameter.objects.get(codigo="PR-AG")
            abonado = Abonado.objects.get(username=cedula)
            ultimo_pago = Pago.objects.filter(abonado=abonado).order_by('-fecha_creacion').first()
            ultima_lectura = Lectura.objects.filter(abonado=abonado).order_by('-fecha').first()

            # Calcula la fecha hace 6 meses desde hoy
            fecha_hace_6_meses = timezone.now() - timezone.timedelta(days=240)
            print(fecha_hace_6_meses)

            # Obtener los últimos 12 registros de Lectura
            ultimas_lecturas = Lectura.objects.order_by('-fecha')[:12]

            # Formatear los datos para el gráfico
            labels = [lectura.fecha.strftime('%b %Y') for lectura in ultimas_lecturas]
            values = [lectura.valor_consumo for lectura in ultimas_lecturas]
            print(labels, values)

            return render(request, 'index.html', {
                'form': form,
                'abonado': abonado,
                'ultimo_pago': ultimo_pago,
                'ultima_lectura': ultima_lectura,
                'total': (float(ultima_lectura.lectura_actual - ultima_lectura.lectura_anterior) * float(param_agua.valor) ) + float(ultimo_pago.cantidad_total_pago - ultimo_pago.total_abonado),
                'consumo' : ultima_lectura.lectura_actual - ultima_lectura.lectura_anterior,
                'deuda': ultimo_pago.cantidad_total_pago - ultimo_pago.total_abonado,
                'lecturas_data': {
                    'labels': labels,
                    'values': values,
                }
            })

        except Abonado.DoesNotExist:
            error_message = 'No se encontró ningún abonado con la cédula proporcionada.'
            return render(request, 'index.html', {
                'form': form,
                'error_message': error_message,
            })

    return render(request, 'index.html', {'form': form})
