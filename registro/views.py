from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated,IsAdminUser

from registro.models import Lectura, Servicio
from registro.serializers import LecturaSerializer, ServicioSerializer

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
