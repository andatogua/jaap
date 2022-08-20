from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from autenticacion.models import Abonado, Empleado
from autenticacion.serializers import AbonadoSerializer, EmpleadoSerializer


class AbonadoLista(generics.ListAPIView):
    permission_classes =[IsAuthenticated,IsAdminUser]
    authentication_classes = (TokenAuthentication,)
    queryset = Abonado.objects.all()
    serializer_class = AbonadoSerializer

class AbonadoDetalle(generics.RetrieveAPIView):
    permission_classes =[IsAuthenticated,IsAdminUser]
    authentication_classes = (TokenAuthentication,)
    queryset = Abonado.objects.all()
    serializer_class = AbonadoSerializer

class EmpleadoLista(generics.ListAPIView):
    permission_classes =[IsAuthenticated,IsAdminUser]
    authentication_classes = (TokenAuthentication,)
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoSerializer

class EmpleadoDetalle(generics.RetrieveAPIView):
    permission_classes =[IsAuthenticated,IsAdminUser]
    authentication_classes = (TokenAuthentication,)
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoSerializer

class EmpleadoActivoDetalle(generics.RetrieveUpdateAPIView):
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoSerializer
    permission_classes =[IsAuthenticated,IsAdminUser]
    authentication_classes = (TokenAuthentication,)

    def get_object(self):
        print(self.request.auth)
        return self.request.user

from django.dispatch import receiver
from django.db.models.signals import post_save
from autenticacion.models import Empleado
from registro.models import Lectura

@receiver(post_save,sender=Lectura)
def post_save_lectura(sender, **kwargs):
    #empleado = Empleado.objects.get(username = kwargs['instance'].empleado)
    #print(empleado.primer_nombre)
    print(kwargs['instance'].empleado)
