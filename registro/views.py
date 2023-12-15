from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated,IsAdminUser

from registro.models import Lectura, Servicio
from registro.serializers import LecturaSerializer, ServicioSerializer, LecturaDiaSerializer
from django.utils import timezone

class CrearServicio(generics.CreateAPIView):
    permission_classes =[IsAuthenticated,IsAdminUser]
    authentication_classes = (TokenAuthentication,)
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer

class CrearLectura(generics.CreateAPIView):
    permission_classes =[IsAuthenticated,IsAdminUser]
    authentication_classes = (TokenAuthentication,)
    queryset = Lectura.objects.all()
    serializer_class = LecturaSerializer

class ListaRegistrosDelDia(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    authentication_classes = (TokenAuthentication,)
    serializer_class = LecturaDiaSerializer

    def get_queryset(self):
        # Filtra los registros del día actual
        fecha_hoy = timezone.now().date()
        queryset = Lectura.objects.filter(fecha__date=fecha_hoy)
        return queryset