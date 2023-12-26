from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F, ExpressionWrapper, DecimalField, Value
from pagos.models import Pago
from django.utils import timezone
from django.db.models.functions import ExtractMonth, ExtractYear, Coalesce
from registro.models  import Lectura

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
    # print(recaudaciones_ultimos_6_meses)

    # Convertir los objetos Decimal a números de punto flotante
    for mes in recaudaciones_ultimos_6_meses:
        mes['total'] = float(mes['total']) if mes['total'] else 0.0

    # Obtener los datos para el gráfico
    labels = [f"{mes['year']}-{mes['mes']}" for mes in recaudaciones_ultimos_6_meses]
    data = [mes['total'] for mes in recaudaciones_ultimos_6_meses]


    # Filtra las lecturas realizadas durante los últimos 6 meses
    lecturas_ultimos_6_meses = Lectura.objects.filter(
        fecha__gte=ultimos_6_meses
    )
    # Calcula el consumo total para cada mes
    # print(lecturas_ultimos_6_meses)
    consumo_por_mes = {}
    for lectura in lecturas_ultimos_6_meses:
        mes_anio = lectura.fecha.strftime('%b %Y')
        consumo_por_mes[mes_anio] = consumo_por_mes.get(mes_anio, 0) + (lectura.lectura_actual - lectura.lectura_anterior)

    # Formatea los datos para el gráfico
    labelsLec = list(consumo_por_mes.keys())
    valuesLec = list(consumo_por_mes.values())

    # Calcula la fecha hace 1 mes desde hoy
    fecha_hace_1_mes = now - timezone.timedelta(days=30)

    # Filtra las lecturas realizadas durante el último mes
    lecturas_ultimo_mes = Lectura.objects.filter(
        fecha__gte=fecha_hace_1_mes
    )

    # Calcula la suma de registros por empleado
    # registros_por_empleado = lecturas_ultimo_mes.values('empleado__username').annotate(total_registros=Sum(1))
    registros_por_empleado = lecturas_ultimo_mes.values('empleado__username','empleado__primer_nombre', 'empleado__primer_apellido').annotate(total_registros=Sum('abonado'))


    # Realiza una expresión para calcular el saldo pendiente
    saldo_pendiente_expr = ExpressionWrapper(
        F('cantidad_total_pago') - F('total_abonado'),
        output_field=DecimalField(max_digits=10, decimal_places=2)
    )

    # Realiza la consulta para obtener las tres personas con más saldo pendiente
    personas_con_saldo_pendiente = (
        Pago.objects
        .values('abonado__id_persona', 'abonado__primer_nombre', 'abonado__primer_apellido')
        .annotate(saldo_pendiente=Coalesce(Sum(saldo_pendiente_expr), Value(0)))
        .order_by('-saldo_pendiente')[:3]
    )

    print("personas_con_saldo_pendiente--> ",personas_con_saldo_pendiente)

    context = {
        'cantidad_recaudada': round(cantidad_recaudada,2),
        'cantidad_recaudada_mes': round(cantidad_recaudada_mes,2),
        'hoy': now.date(),
        'mes': now.month,
        'labels': labels,
        'data': data,
        'labelsLec': labelsLec,
        'valuesLec': valuesLec,
        'registros_por_empleado': registros_por_empleado,
        "personas_con_saldo_pendiente": personas_con_saldo_pendiente
    }

    return render(request, 'reportes/dashboard.html', context)
