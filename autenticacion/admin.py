from dataclasses import fields
from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Permission
from autenticacion.models import Abonado, Empleado, Localidad, Oficina, Persona, Rol
from django import forms

from registro.models import Lectura

# Register your models here.
admin.site.site_title = "J.A.A.P"
admin.site.site_header = "J.A.A.P"

class PersonaForm(UserCreationForm):
    password = None
    user_permissions = forms.ModelMultipleChoiceField(
        Permission.objects.exclude(content_type__app_label__in=['auth','admin','sessions','users','contenttypes']),
    )
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].required = False
        self.fields['password2'].required = False
        self.fields['user_permissions'].required = False
        self.fields['user_permissions'].help_text = """Presione "Control" o "Command" si usa Mac, para seleccionar varias opciones. """
        self.fields['user_permissions'].label = 'Lista de Permisos'

    def clean(self):
        try:
            # here you want to maybe send a signal which can be picked up or something
            password = self.cleaned_data['username']
            self.cleaned_data['password'] = password
        except KeyError:
            return
        return super().clean()


class PersonaAdmin(UserAdmin):
    add_form = PersonaForm
    form = PersonaForm
    list_display = ( 'username', 'primer_nombre',
                    'primer_apellido', 'email',
                    'last_login')
    search_fields = ('email', 'username', 'primer_apellido')
    readonly_fields = ('id', 'date_joined', 'last_login',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = (
        ('Datos personales', 
            {
                'fields': (
                    'username', 
                    'primer_nombre', 'segundo_nombre', 
                    'primer_apellido','segundo_apellido',
                )
            }
        ),
        ('Información de contacto', 
            {
                'fields': (
                    'email', 'direccion', 'telefono'
                )
            }
        )
    )
    add_fieldsets = (
        ('Datos personales', 
            {
                'fields': (
                    'username', 
                    'primer_nombre', 'segundo_nombre', 
                    'primer_apellido','segundo_apellido',
                )
            }
        ),
        ('Información de contacto', 
            {
                'fields': (
                    'email', 'direccion', 'telefono'
                )
            }
        )
    )

    def save_model(self, request, obj, form, change):

        obj.id_persona = form.cleaned_data['username']
        obj.set_password(form.cleaned_data['password'])
        super(PersonaAdmin, self).save_model(request, obj, form, change)


class AbonadoAdmin(PersonaAdmin):
    list_display = PersonaAdmin.list_display + ('localidad',)
    fieldsets= PersonaAdmin.fieldsets + (
        ('Datos Consumidor', 
            {
                'fields': (
                    'num_medidor','localidad','latitud','longitud'
                )
            }
        ),
        
    )
    add_fieldsets= PersonaAdmin.add_fieldsets + (
        ('Datos Consumidor', 
            {
                'fields': (
                    'num_medidor', 'localidad'
                )
            }
        ),
    )

class EmpleadoAdmin(PersonaAdmin):
    list_display = PersonaAdmin.list_display + ('is_staff','rol','oficina')
    fieldsets= PersonaAdmin.fieldsets + (
        ('Datos Empresariales', 
            {
                'fields': (
                    'rol','oficina'
                )
            }
        ),
        ('Permisos de usuario', 
            {
                'fields': (
                    'user_permissions',
                )
            }
        ),
        
    )
    add_fieldsets= PersonaAdmin.add_fieldsets + (
        ('Datos de empleado', 
            {
                'fields': (
                    'rol','oficina'
                )
            }
        ),
        
    )

    def save_model(self, request, obj, form, change):
        obj.is_staff = True
        super(EmpleadoAdmin, self).save_model(request, obj, form, change)

admin.site.register(Persona, PersonaAdmin)
admin.site.register(Abonado, AbonadoAdmin)
admin.site.register(Localidad)
admin.site.register(Oficina)
admin.site.register(Rol)
admin.site.register(Empleado,EmpleadoAdmin)

