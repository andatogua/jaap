from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import PagoCreateView, ObtenerInfoAbonadoView

urlpatterns = [
    path('', PagoCreateView.as_view(), name="realizar_pago"),
    path('obtener-info-abonado/', ObtenerInfoAbonadoView.as_view(), name='obtener_info'),
]

urlpatterns = format_suffix_patterns(urlpatterns)