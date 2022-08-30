from dataclasses import fields
from django import forms
from django.conf import settings
from django.contrib import admin
from .models import Lectura, Servicio, TipoServicio

# Register your models here.
class LecturaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
    def clean(self):
        registro_anterior = Lectura.objects.filter(abonado = self.cleaned_data['abonado']).last()
        if registro_anterior and self.cleaned_data['lectura_actual'] < registro_anterior.lectura_actual:
            #raise forms.ValidationError('Lectura actual menor que la anterior')
            return self.add_error('lectura_actual',forms.ValidationError('Lectura actual menor que la anterior'))
        return super().clean()


class LecturaAdmin(admin.ModelAdmin):
    form = LecturaForm
    list_display =  (
        "abonado","empleado","lectura_anterior",
        "lectura_actual","fecha","valor_consumo"
    )

    readonly_fields =   (
        "lectura_anterior","valor_consumo"
    )

    add_fieldsets = (
        ("Registro de lecturas de consumno",
            {
                'fields':(
                    "abonado","empleado",
                    "lectura_actual","valor_consumo",
                    "observacion"
                )
            }
        ),
    )

    fieldsets = (
        ("Registro de lecturas de consumno",
            {
                'fields':(
                    "abonado","empleado",
                    "lectura_actual","observacion"
                )
            }
        ),
    )

    filter_horizontal = ()
    list_filter = ()
    search_fields = ("abonado__username","empleado__username",)


    """
    def save_model(self, request, obj, form, change):

        registro_anterior = Lectura.objects.filter(abonado = form.cleaned_data['abonado']).last()
        if registro_anterior == None:
            obj.lectura_anterior = 0
        else:
            obj.lectura_anterior = registro_anterior.lectura_actual

        consumo = obj.lectura_actual - obj.lectura_anterior
        if consumo > settings.LIMITEM3:
            obj.valor_consumo = (settings.LIMITEM3 * settings.VALORM3) + ((consumo - settings.LIMITEM3)*settings.VALOREXM3)
        elif consumo <= settings.MINIMO:
            obj.valor_consumo = 2
        else:
            obj.valor_consumo = round(consumo * settings.VALORM3,2)




        super(LecturaAdmin, self).save_model(request, obj, form, change)
    """

class ServicioAdmin(admin.ModelAdmin):
    list_display =  (
        "abonado","empleado","tipo_servicio",
        "fecha","valor_servicio"
    )

    readonly_fields =   (
        "fecha",
    )

    add_fieldsets = (
        ("Registro de servicios realizados",
            {
                'fields':(
                    "abonado","empleado","tipo_servicio",
                    "valor_servicio","observacion"
                )
            }
        ),
    )

    fieldsets = (
        ("Registro de servicios realizados",
            {
                'fields':(
                    "abonado","empleado","tipo_servicio",
                    "valor_servicio","observacion"
                )
            }
        ),
    )

    filter_horizontal = ()
    list_filter = ()
    search_fields = ("abonado__username","empleado__username",)

admin.site.register(Lectura, LecturaAdmin)
admin.site.register(Servicio,ServicioAdmin)
admin.site.register(TipoServicio)