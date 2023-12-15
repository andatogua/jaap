from dataclasses import fields
from rest_framework import serializers
from .models import Lectura, Servicio
from autenticacion.serializers import AbonadoSerializer

class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields='__all__'

class LecturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lectura
        fields='__all__'

class LecturaDiaSerializer(serializers.ModelSerializer):
    abonado = AbonadoSerializer()

    class Meta:
        model= Lectura
        fields= '__all__'