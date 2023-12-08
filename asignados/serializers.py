from rest_framework import serializers
from .models import Asignacion
from autenticacion.models import Empleado, Localidad

class EmpleadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empleado
        fields = '__all__'

class LocalidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Localidad
        fields = '__all__'

class AsignacionSerializer(serializers.ModelSerializer):
    empleado = EmpleadoSerializer()
    localidad = LocalidadSerializer()

    class Meta:
        model = Asignacion
        fields = '__all__'