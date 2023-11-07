from django.contrib import admin
from .models import Parameter

# Register your models here.
class ParameterAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descripcion', 'valor', 'estado')  # Define las columnas que se mostrarán en la lista de parámetros
    list_filter = ('estado',)  # Agrega un filtro por estado

admin.site.register(Parameter, ParameterAdmin)
