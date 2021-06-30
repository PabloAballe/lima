from django.contrib import admin
from .models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin
import datetime as dt



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
    list_display= ['tecnica','fecha', 'zona']
    search_fields =  ['tecnica__nombre_tecnica','fecha', 'zona']
    list_filter =   ['tecnica__nombre_tecnica','fecha', 'zona']


class HorariosAdmin(ImportExportModelAdmin):
    list_display= ['tecnica','fecha', 'entrada', 'salida','trabajado']
    search_fields =  ['tecnica__nombre_tecnica','fecha', 'entrada', 'salida','trabajado']
    list_filter =   ['tecnica__nombre_tecnica','fecha', 'entrada', 'salida','trabajado']
    readonly_fields = ['trabajado']

    def horas_trabajadas(self, obj):
        entrada = dt.datetime.strptime(str(obj.entrada), '%H:%M:%S')
        salida = dt.datetime.strptime(str(obj.salida), '%H:%M:%S')
        result = (salida -  datetime.timedelta(hours=entrada.hour , minutes=entrada.minute, seconds=entrada.second)).time()
        return result

class ConfiguracionAdmin(ImportExportModelAdmin):
    list_display= ['nombre_comercial','propietario', 'logo', 'politica', 'email_nuevos_clientes']
    search_fields =  ['nombre_comercial','propietario']
    list_filter =   ['nombre_comercial','propietario']

class TurnosAdmin(ImportExportModelAdmin):
    list_display= ['tecnica','centro', 'turno']
    search_fields =  ['tecnica','centro', 'turno']
    list_filter =   ['tecnica','centro', 'turno']

class TratamientosAdmin(ImportExportModelAdmin):
    list_display= ['fecha', 'cliente','js', 'jl', 'tecnica','comentario']
    search_fields =  ['fecha','tecnica', 'cliente']
    list_filter =   ['fecha','tecnica', 'cliente']

admin.site.site_header = "Lima y Neon"
admin.site.site_title = "Portal Lima y Neon"
admin.site.index_title = "Portal Lima y Neon"


admin.site.register(Centro, CentroAdmin)
admin.site.register(Configuracion, ConfiguracionAdmin)
admin.site.register(Tratamientos, TratamientosAdmin)
admin.site.register(Turnos, TurnosAdmin)
admin.site.register(Paciente, PacienteAdmin)
admin.site.register(Tecnica, TecnicaAdmin)
admin.site.register(Cita, CitaAdmin)
admin.site.register(ControlHorario, HorariosAdmin)
