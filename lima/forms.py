from django import forms
from django.forms import ModelForm
from .models import *
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from django_summernote.fields import SummernoteTextFormField, SummernoteTextField
from ckeditor.widgets import CKEditorWidget
from django.template import Context, Template
from jsignature.forms import JSignatureField

class SheachForm(forms.Form):
    shearch = forms.CharField( label="", max_length=1000 , widget= forms.TextInput(attrs={'class':'form-control mr-sm-2'}))

class CentroForm(ModelForm):
    class Meta:
        model = Centro
        fields = ('nombre_centro', 'propietaria','localizacion')


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
        fields = ('nombre_paciente','apellidos_paciente','telefono_paciente','dni','email', 'documento_de_autorizacion','documento_proteccion_de_datos', 'autorizacion_envio_informacion_comercial','poblacion', 'direccion', )

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

class DocTemplateEditForm(forms.ModelForm):
    class Meta:
        model=DocTemplate
        widgets = {
            'plantilla_doc': forms.Textarea(attrs={'class':'some_class', 'id':'summernote'}),
        }
        fields=('nombre_doc', 'plantilla_doc' )

class DocTemplateNewForm(forms.ModelForm):
    class Meta:
        model=DocTemplate
        widgets = {
            'plantilla_doc': forms.Textarea(attrs={'class':'some_class', 'id':'summernote'}),
        }
        fields=('nombre_doc', 'plantilla_doc' )

class SingForm(forms.ModelForm):
    class Meta:
        model=DocSings
        fields=('firma', )


class CajaFormAdmin(forms.ModelForm):
    class Meta:
        model=Cajas
        fields=('centro','tecnica','porcentaje','cantidad_efectivo', 'comentario')

class CajaForm(forms.ModelForm):
    class Meta:
        model=Cajas
        fields=('centro','porcentaje','cantidad_efectivo', 'comentario')

class StockForm(forms.ModelForm):
    cantidad_retirar=forms.IntegerField(label='Ingrese cantidad a retirar:')
    class Meta:
        model=Stock
        fields=('nombre_stock','cantidad_retirar' )

class StockNewForm(forms.ModelForm):
    class Meta:
        model=Stock
        fields=('nombre_stock','cantidad' )


class ListaForm(forms.ModelForm):
    class Meta:
        model=Lista
        fields=('hora_inicio' , 'tecnica','servicios')


class SingForm__(forms.Form):
    signature = JSignatureField()


class PrerenderForm(forms.ModelForm):

    class Meta:
        model=DocSings
        widgets = {
            'plantilla_render': forms.Textarea(attrs={'class':'some_class', 'id':'summernote'}),
        }
        fields=('plantilla_render', )

class EmailForm(forms.Form):
    asunto=forms.CharField(label='Asunto del Email:', max_length=100)
    destinatario=forms.CharField(label='Destinatario del Email:', max_length=100)
    #emails=forms.ModelMultipleChoiceField(queryset=Paciente.objects.exclude(email='').filter( autorizacion_envio_informacion_comercial=True), label='Selecciona los emails a enviar:')
    plantilla=forms.ModelChoiceField(queryset=EmailTemplates.objects.all().order_by("nombre"))

class EstadisticasAdminForm(forms.Form):
    fecha_inico=forms.DateTimeField(label='Fecha de inicio')
    fecha_fin=forms.DateTimeField(label='Fecha de fin')
    centro=forms.ModelChoiceField(queryset=Centro.objects.exclude(habilitado=False), label='Selecciona las clínicas:')
    tecnicas=forms.ModelChoiceField(queryset=Tecnica.objects.exclude(habilitado=False), label='Selecciona las técnicas:')

class EstadisticasTecnicaForm(forms.Form):
    fecha_inico=forms.DateTimeField(label='Fecha de inicio')
    fecha_fin=forms.DateTimeField(label='Fecha de fin')

