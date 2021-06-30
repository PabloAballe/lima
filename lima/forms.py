from django import forms
from django.forms import ModelForm
from .models import *
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from django_summernote.fields import SummernoteTextFormField, SummernoteTextField
from ckeditor.widgets import CKEditorWidget

class SheachForm(forms.Form):
    shearch = forms.CharField( label="", max_length=1000 , widget= forms.TextInput(attrs={'class':'form-control mr-sm-2'}))

class CentroForm(ModelForm):
    class Meta:
        model = Centro
        fields = ('nombre_centro', 'propietaria','localizacion')

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ('nombre_paciente','apellidos_paciente','telefono_paciente','dni','email', 'autorizacion','protec_datos', 'poblacion', 'direccion')

class CitaFormAdmin(forms.ModelForm):
    class Meta:
        model=Cita
        fields=('zona', 'hertz', 'milisegundos','julios', 'fecha', 'tecnica' )

class CitaForm(forms.ModelForm):
    class Meta:
        model=Cita
        fields=('zona', 'hertz', 'milisegundos','julios', 'fecha')

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ('nombre_paciente','apellidos_paciente','telefono_paciente','dni','email', 'autorizacion','protec_datos', 'poblacion', 'direccion')

class TratamientoFormAdmin(forms.ModelForm):
    class Meta:
        model=Tratamientos
        fields=('fecha', 'js', 'jl','tecnica', 'comentario' )

class TratamientoForm(forms.ModelForm):
    class Meta:
        model=Tratamientos
        fields=('fecha', 'js', 'jl', 'comentario' )

class EmailTemplateEditForm(forms.ModelForm):
    class Meta:
        model=EmailTemplates
        widgets = {
            'plantilla': forms.Textarea(attrs={'class':'some_class', 'id':'summernote'}),
        }
        fields=('nombre', 'plantilla' )


class EmailTemplateNewForm(forms.ModelForm):
    class Meta:
        model=EmailTemplates
        widgets = {
            'plantilla': forms.Textarea(attrs={'class':'some_class', 'id':'summernote'} ),
        }
        fields=('nombre', 'plantilla' )


class EmailForm(forms.Form):
    asunto=forms.CharField(label='Asunto del Email:', max_length=100)
    destinatario=forms.CharField(label='Destinatario del Email:', max_length=100)
    emails=forms.ModelMultipleChoiceField(queryset=Paciente.objects.exclude(email='').filter( autorizacion=True , protec_datos=True), label='Selecciona los emails a enviar:')
    #mensaje=forms.CharField(widget=forms.Textarea(attrs={'class':'some_class', 'id':'summernote'}), label='Cuerpo del email:' )
    plantilla=forms.ModelChoiceField(queryset=EmailTemplates.objects.all().order_by("nombre"))

