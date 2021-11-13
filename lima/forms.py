from django import forms
from django.forms import ModelForm
from .models import *
from ckeditor.widgets import CKEditorWidget
from django.template import Context, Template
from jsignature.forms import JSignatureField

class SheachForm(forms.Form):
    shearch = forms.CharField( label="Buscar",help_text="Ingrese su termino de busqueda", max_length=1000 , widget= forms.TextInput(attrs={'class':''}))

class CentroForm(ModelForm):
    class Meta:
        model = Centro
        widgets = {
            'nombre_centro': forms.TextInput(attrs={'class':'input', 'id':''}),
            'horario_apertura': forms.TextInput(attrs={'class':'some_class', 'id':'datepicker'}),
            'horario_cierre': forms.TextInput(attrs={'class':'some_class', 'id':'datepicker1'}),
        }
        fields=('__all__' )
        exclude = ['id_centro', 'history']


class CitaFormAdmin(forms.ModelForm):
    class Meta:
        model=Cita
        fields=('zona', 'hertz', 'milisegundos','julios', 'fecha', 'tecnica' )

class TareaForm(forms.ModelForm):
    class Meta:
        model=Tareas
        fields=('nombre_tarea', 'descripcion_tarea', 'estado','etiquetas' )



class MensajeForm(forms.ModelForm):
    class Meta:
        model=Mensajes
        # widgets = {
        #     'cuerpo_mensaje': forms.TextInput(attrs={'class':'textarea h-24', 'id':''}),
        # }
        fields=('cuerpo_mensaje',)

class CitaForm(forms.ModelForm):
    class Meta:
        model=Cita
        fields=('zona', 'hertz', 'milisegundos','julios', 'fecha')

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields=('__all__' )
        exclude = ['id_paciente', 'history', 'fecha_alta']

class TratamientoFormAdmin(forms.ModelForm):
    class Meta:
        model=Tratamientos
        fields=('__all__' )
        exclude = ['id_tratamiento', 'icon','cliente', 'hora_fin']

class TratamientoForm(forms.ModelForm):
    class Meta:
        model=Tratamientos
        fields=('__all__' )
        exclude = ['id_tratamiento', 'icon','cliente', 'tecnica', 'hora_fin']

class EmailTemplateEditForm(forms.ModelForm):
    class Meta:
        model=EmailTemplates
        widgets = {
            'plantilla': forms.Textarea(attrs={'class':'some_class', 'id':'editor'}),
        }
        fields=('nombre', 'plantilla' )



class EmailTemplateNewForm(forms.ModelForm):
    class Meta:
        model=EmailTemplates
        widgets = {
            'plantilla': forms.Textarea(attrs={'class':'some_class', 'id':'editor'} ),
        }
        fields=('nombre', 'plantilla' )

class DocTemplateEditForm(forms.ModelForm):
    class Meta:
        model=DocTemplate

        widgets = {
            'plantilla_doc': forms.Textarea(attrs={'class':'some_class', 'id':'editor'}),
        }
        fields=('nombre_doc', 'plantilla_doc' )

class DocTemplateNewForm(forms.ModelForm):
    class Meta:
        model=DocTemplate
        widgets = {
            'plantilla_doc': forms.Textarea(attrs={'class':'some_class', 'id':'editor'}),
        }
        fields=('nombre_doc', 'plantilla_doc' )

class SingForm(forms.ModelForm):
    class Meta:
        model=DocSings
        fields=('plantilla_document','firma', )


class SingForm_(forms.Form):
    firma=forms.ImageField(label='Firma', required=False)


class CajaFormAdmin(forms.ModelForm):
    class Meta:
        model=Cajas
        fields=('centro','tecnica','porcentaje','cantidad_efectivo', 'comentario')

class ConfigAdmin(forms.ModelForm):
    class Meta:
        model=Configuracion
        fields = '__all__'

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

class AppointmentWEBForm(forms.ModelForm):
    class Meta:
        model=Lista
        fields=('hora_inicio' ,'servicios')

class FotoForm(forms.ModelForm):
    class Meta:
        model=ImagenesClientes
        fields=('imagen' , 'comentario')

class SingForm__(forms.Form):
    signature = JSignatureField()


class PrerenderForm(forms.Form):
    plantilla_doc=forms.CharField(help_text="Documento a firmar", required=False,widget=forms.Textarea(attrs={'readonly':'readonly'}))

class EmailForm(forms.Form):
    asunto=forms.CharField(label='Asunto del Email:', max_length=100)
    destinatario=forms.CharField(label='Destinatario del Email:', max_length=100)
    plantilla=forms.ModelChoiceField(queryset=EmailTemplates.objects.all().order_by("nombre"))
    enviar_a_las=forms.DateTimeField()



class WhatsappForm(forms.Form):
    # widgets = {
    #         'mensaje': forms.Textarea(attrs={'class':'some_class', 'id':'editor'}),
    #     }
    mensaje=forms.CharField(label='Mensaje a enviar:', max_length=500,)

    def __init__(self, *args, **kwargs):
        super(WhatsappForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
        self.fields['mensaje'].widget.attrs['style'] = 'height:10rem;'

class EstadisticasAdminForm(forms.Form):
    fecha_inico=forms.DateTimeField(label='Fecha de inicio')
    fecha_fin=forms.DateTimeField(label='Fecha de fin')
    centro=forms.ModelChoiceField(queryset=Centro.objects.exclude(habilitado=False), label='Selecciona las clínicas:')
    tecnicas=forms.ModelChoiceField(queryset=Tecnica.objects.exclude(habilitado=False), label='Selecciona las técnicas:')

class EstadisticasTecnicaForm(forms.Form):
    fecha_inico=forms.DateTimeField(label='Fecha de inicio')
    fecha_fin=forms.DateTimeField(label='Fecha de fin')

