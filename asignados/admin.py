from django.contrib import admin
from .models import Asignacion

# Register your models here.
class AsignacionAdmin(admin.ModelAdmin):
    list_display = ('empleado', 'localidad', 'dia_del_mes','fecha_asignacion')
    search_fields = ('empleado__username', 'localidad__nombre')

# Registra el modelo y la clase del administrador
admin.site.register(Asignacion, AsignacionAdmin)