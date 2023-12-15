from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from registro.views import CrearLectura, CrearServicio, ListaRegistrosDelDia

urlpatterns = [
    path('servicios/crear/', CrearServicio.as_view()),
    path('lecturas/crear/', CrearLectura.as_view()),
    path('lecturas/listardia/', ListaRegistrosDelDia.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)