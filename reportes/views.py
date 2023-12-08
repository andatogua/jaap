from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from pagos.models import Pago
from django.utils import timezone
from django.db.models.functions import ExtractMonth, ExtractYear

@login_required(login_url="login")
def dashboard_view(request):
    # Obtener la fecha y hora actual en el timezone configurado en tu aplicación
    now = timezone.now()

    # Filtrar los pagos del día actual
    pagos_del_dia = Pago.objects.filter(fecha_creacion__date=now.date())

    # Calcular la cantidad total recaudada
    cantidad_recaudada = pagos_del_dia.aggregate(Sum('cantidad_total_pago'))['cantidad_total_pago__sum']

    # Si no hay pagos para el día actual, la cantidad_recaudada puede ser None, así que maneja ese caso si es necesario.
    if cantidad_recaudada is None:
        cantidad_recaudada = 0.0  # O cualquier valor predeterminado que desees

    # Filtrar los pagos del mes actual
    pagos_del_mes = Pago.objects.filter(fecha_creacion__month=now.month, fecha_creacion__year=now.year)

    # Calcular la cantidad total recaudada en el mes
    cantidad_recaudada_mes = pagos_del_mes.aggregate(Sum('cantidad_total_pago'))['cantidad_total_pago__sum']

    # Si no hay pagos para el mes actual, la cantidad_recaudada_mes puede ser None, así que maneja ese caso si es necesario.
    if cantidad_recaudada_mes is None:
        cantidad_recaudada_mes = 0.0  # O cualquier valor predeterminado que desees

    # Filtrar los pagos de los últimos 6 meses
    ultimos_6_meses = now - timezone.timedelta(days=180)
    pagos_ultimos_6_meses = Pago.objects.filter(fecha_creacion__gte=ultimos_6_meses)

    # Calcular la cantidad total recaudada para cada mes en los últimos 6 meses
    recaudaciones_ultimos_6_meses = pagos_ultimos_6_meses \
        .annotate(mes=ExtractMonth('fecha_creacion'), year=ExtractYear('fecha_creacion')) \
        .values('year', 'mes') \
        .annotate(total=Sum('cantidad_total_pago')) \
        .order_by('year', 'mes')
    print(recaudaciones_ultimos_6_meses)

    # Convertir los objetos Decimal a números de punto flotante
    for mes in recaudaciones_ultimos_6_meses:
        mes['total'] = float(mes['total']) if mes['total'] else 0.0

    # Obtener los datos para el gráfico
    labels = [f"{mes['year']}-{mes['mes']}" for mes in recaudaciones_ultimos_6_meses]
    data = [mes['total'] for mes in recaudaciones_ultimos_6_meses]


    context = {
        'cantidad_recaudada': round(cantidad_recaudada,2),
        'cantidad_recaudada_mes': round(cantidad_recaudada_mes,2),
        'hoy': now.date(),
        'mes': now.month,
        'labels': labels,
        'data': data,
    }

    return render(request, 'reportes/dashboard.html', context)
