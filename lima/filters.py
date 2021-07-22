import django_filters
from .models import *

class ClientFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Paciente
        fields = ['nombre_paciente', 'apellidos_paciente', 'telefono_paciente', 'email', 'dni', 'documento_de_autorizacion','documento_proteccion_de_datos', 'centro','poblacion','direccion', 'autorizacion_envio_informacion_comercial', 'fecha_alta']