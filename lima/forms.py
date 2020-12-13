from django import forms
from django.forms import ModelForm
from .models import *



class SheachForm(forms.Form):
    shearch = forms.CharField( label="", max_length=100 , widget= forms.TextInput(attrs={'class':'form-control mr-sm-2'}))

class CentroForm(ModelForm):
    class Meta:
        model = Centro
        fields = ('nombre_centro', 'propietaria','localizacion')

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ('nombre_paciente','apellidos_paciente','telefono_paciente','email', 'autorizacion','protec_datos', 'poblacion', 'direccion')

class CitaForm(forms.ModelForm):
    class Meta:
        model=Cita
        fields=('zona', 'comentario', 'hertz', 'milisegundos','julios', 'fecha' )
