# urls.py
from django.urls import path
from .views import AsignacionList

urlpatterns = [
    path('me/', AsignacionList.as_view(), name='asignacion-me'),
    # Otros patrones de URL aquí...
]
