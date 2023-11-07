from rest_framework import generics
from .models import Parameter
from .serializers import ParameterSerializer

class ParameterList(generics.ListAPIView):
    queryset = Parameter.objects.all()
    serializer_class = ParameterSerializer
