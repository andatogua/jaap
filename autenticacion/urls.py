from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from autenticacion import views

urlpatterns = [
    path('autenticacion/abonados/', views.AbonadoLista.as_view()),
    path('autenticacion/empleados/', views.EmpleadoLista.as_view()),
    path('autenticacion/empleados/<int:pk>/', views.EmpleadoDetalle.as_view()),
    path('autenticacion/abonados/<int:pk>/', views.AbonadoDetalle.as_view()),
    path('autenticacion/me/', views.EmpleadoActivoDetalle.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)