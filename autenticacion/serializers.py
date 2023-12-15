from dataclasses import fields
from rest_framework import serializers
from .models import Abonado, Empleado, Persona

class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields=[
                'id','username',
                'primer_nombre','segundo_nombre',
                'primer_apellido','segundo_apellido',
                'direccion','telefono',
                'email','is_staff',
                ] 
        read_only_fields = ('is_staff', )



class AbonadoSerializer(PersonaSerializer):
    localidad = serializers.StringRelatedField()
    class Meta:
        model = Abonado
        fields=[
                'id','username',
                'primer_nombre','primer_apellido',
                'direccion','telefono',
                'email',
                'longitud','latitud','localidad'
                ]

class EmpleadoSerializer(PersonaSerializer):
    rol         = serializers.StringRelatedField()
    oficina     = serializers.StringRelatedField()

    class Meta:
        model = Empleado
        fields= PersonaSerializer.Meta.fields + ['rol','oficina']

        read_only_fields = ('is_staff', )