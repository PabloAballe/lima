from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *
from tinymce.widgets import TinyMCE

# Register your models here.
class BlogAdmin(ImportExportModelAdmin):
    list_display= ['titulo', 'autor', 'creado_el']
    search_fields = ['titulo', 'autor', 'creado_el']
    list_filter =  ['titulo', 'autor', 'creado_el']

class PagesAdmin(ImportExportModelAdmin):
    list_display= ['nombre_pagina', 'pertenece_a', 'creado_el']
    search_fields = ['nombre_pagina', 'pertenece_a', 'creado_el']
    list_filter =  ['nombre_pagina', 'pertenece_a', 'creado_el']


class ConctactAdmin(ImportExportModelAdmin):
    list_display= ['nombre_contacto', 'telefono_contacto', 'email_contacto','creado_el']
    search_fields = ['nombre_contacto', 'telefono_contacto', 'email_contacto','creado_el']
    list_filter =  ['nombre_contacto', 'telefono_contacto', 'email_contacto','creado_el']


admin.site.register(Blog, BlogAdmin)
admin.site.register(Conctact, ConctactAdmin)
admin.site.register(Pages, PagesAdmin)