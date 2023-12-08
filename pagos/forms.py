# pagos/forms.py
from django import forms
from .models import Pago
from autenticacion.models import Abonado
from registro.models import Lectura

class PagoForm(forms.ModelForm):
    abonado = forms.ModelChoiceField(queryset=Abonado.objects.all())
    ultima_info_consumo = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    ultima_info_pago = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    cantidad_total_pago = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = Pago
        fields = ['empleado', 'abonado', 'registro_consumo', 'cantidad_total_pago', 'total_abonado']
