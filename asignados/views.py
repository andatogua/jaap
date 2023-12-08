# views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Asignacion
from .serializers import AsignacionSerializer

class AsignacionList(generics.ListAPIView):
    serializer_class = AsignacionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filtrar asignaciones por el usuario logeado
        return Asignacion.objects.filter(empleado=self.request.user)
