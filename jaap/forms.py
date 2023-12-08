# En forms.py

from django import forms

class BuscarAbonadoForm(forms.Form):
    cedula = forms.CharField(label='Cédula del Abonado', max_length=10)
