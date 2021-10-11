import django_filters
from .models import *
from django import forms

class DateInput(forms.DateInput):
    input_type = 'date'

class ClientFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Paciente
        widgets = {
            'fecha_nacimiento':  forms.DateField(
            widget=forms.TextInput(
                attrs={'type': 'date'}
            )
        ),
            'fecha_alta':  forms.DateField(
            widget=forms.TextInput(
                attrs={'type': 'date'}
            )
        ),
        }
        fields = ['id_paciente','nombre_paciente','apellidos_paciente','telefono_paciente','email','dni','documento_de_autorizacion','documento_proteccion_de_datos','centro','poblacion','direccion','notas_paciente','fecha_nacimiento','estado','etiqueta','autorizacion_envio_informacion_comercial','fecha_alta']