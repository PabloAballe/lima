from django import forms
from django.forms import ModelForm
from .models import *
from ckeditor.widgets import CKEditorWidget


class ConfigWebAdmin(forms.ModelForm):
    class Meta:
        model=ConfiguracionWEB
        fields=('__all__' )
        exclude = ['id_configuracion']

class ContactForm(forms.ModelForm):
    class Meta:
        model=Conctact
        fields=('__all__' )
        exclude = ['id_contacto', 'creado_el']