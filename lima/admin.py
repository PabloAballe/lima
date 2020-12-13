from django.contrib import admin
from .models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin





class CentroAdmin(ImportExportModelAdmin):
    list_display= ['nombre_centro', 'propietaria', 'localizacion']
    search_fields = ['nombre_centro', 'propietaria', 'localizacion']
    list_filter =  ['nombre_centro', 'propietaria', 'localizacion']

class PacienteAdmin(ImportExportModelAdmin):
    list_display= ['nombre_paciente', 'apellidos_paciente', 'telefono_paciente', 'email', 'autorizacion', 'protec_datos','poblacion', 'direccion' ]
    search_fields =['nombre_paciente', 'apellidos_paciente', 'telefono_paciente', 'email', 'autorizacion', 'protec_datos','poblacion', 'direccion' ]
    list_filter =  ['nombre_paciente', 'apellidos_paciente', 'telefono_paciente', 'email', 'autorizacion', 'protec_datos','poblacion', 'direccion' ]

class TecnicaAdmin(ImportExportModelAdmin):
    list_display= ['id_tecnica','nombre_tecnica', 'apellidos_tecnica']
    search_fields = ['id_tecnica','nombre_tecnica', 'apellidos_tecnica']
    list_filter =  ['id_tecnica','nombre_tecnica', 'apellidos_tecnica']


class CitaAdmin(ImportExportModelAdmin):
    list_display= ['tecnica','fecha', 'zona', 'comentario']
    search_fields =  ['tecnica__nombre_tecnica','fecha', 'zona', 'comentario']
    list_filter =   ['tecnica__nombre_tecnica','fecha', 'zona', 'comentario']


class HorariosAdmin(ImportExportModelAdmin):
    list_display= ['tecnica','fecha', 'entrada', 'salida']
    search_fields =  ['tecnica__nombre_tecnica','fecha', 'entrada', 'salida']
    list_filter =   ['tecnica__nombre_tecnica','fecha', 'entrada', 'salida']

admin.site.site_header = "Lima y Neon"
admin.site.site_title = "Portal Lima y Neon"
admin.site.index_title = "Portal Lima y Neon"


admin.site.register(Centro, CentroAdmin)
admin.site.register(Paciente, PacienteAdmin)
admin.site.register(Tecnica, TecnicaAdmin)
admin.site.register(Cita, CitaAdmin)
admin.site.register(ControlHorario, HorariosAdmin)
