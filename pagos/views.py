# pagos/views.py
from django.views.generic.edit import CreateView
from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404
from .models import Pago
from .forms import PagoForm
from registro.models import Lectura
from parameters.models import Parameter
from autenticacion.models import Abonado

class PagoCreateView(CreateView):
    model = Pago
    form_class = PagoForm
    template_name = 'pagos/pago_form.html'
    success_url = '/reportes/dashboard/'

class ObtenerInfoAbonadoView(View):
    def get(self, request, *args, **kwargs):
        abonado_id = request.GET.get('abonado_id')
        abonado = get_object_or_404(Abonado, pk=abonado_id)
        m3 = Parameter.objects.filter(codigo="PR-AG").first()

        total_a_pagar = 0

        # Obtener el último registro de consumo para el abonado
        ultimo_consumo = Lectura.objects.filter(abonado=abonado).order_by('fecha').last()
        consumo = 'No hay registros de consumo.' if not ultimo_consumo else str(ultimo_consumo.lectura_actual)

        if ultimo_consumo:
            total_a_pagar += (float(ultimo_consumo.lectura_actual - ultimo_consumo.lectura_anterior) * float(m3.valor))

        # Obtener el último pago para el abonado
        ultimo_pago = Pago.objects.filter(abonado=abonado).order_by('-fecha_creacion').first()
        pago = 'No hay registros de pago.' if not ultimo_pago else str(ultimo_pago.cantidad_total_pago)

        if ultimo_pago:
            total_a_pagar += round(float(ultimo_pago.cantidad_total_pago) - float(ultimo_pago.total_abonado),2)

        # Obtener las opciones actualizadas para el campo registro_consumo
        # opciones_registro_consumo = Lectura.objects.filter(abonado=abonado).values('id', 'lectura_actual')

        return JsonResponse({
            'ultimo_consumo': consumo,
            'ultimo_pago': pago,
            'opciones_registro_consumo':[
                {
                        'id': ultimo_consumo.id,
                        'str': ultimo_consumo.lectura_actual
                }
            ],
            'cantidad_total_pago': total_a_pagar
        })