from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *
from tinymce.widgets import TinyMCE

# Register your models here.
class HelpClasesAdmin(ImportExportModelAdmin):
    list_display= ['nombre_catogoria', 'creada_el', ]
    search_fields = ['nombre_catogoria', 'creada_el', ]
    list_filter =  ['nombre_catogoria', 'creada_el', ]

class HelpAdmin(ImportExportModelAdmin):
    list_display= ['titulo', 'autor', 'creado_el']
    search_fields = ['titulo', 'autor', 'creado_el']
    list_filter = ['titulo', 'autor', 'creado_el']




admin.site.register(HelpPost, HelpAdmin)
admin.site.register(HelpClases, HelpClasesAdmin)