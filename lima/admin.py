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
    list_display= ['nombre_paciente', 'apellidos_paciente', 'telefono_paciente', 'email', 'documento_de_autorizacion', 'documento_proteccion_de_datos','autorizacion_envio_informacion_comercial', 'poblacion', 'direccion' ]
    search_fields =['nombre_paciente', 'apellidos_paciente', 'telefono_paciente', 'email', 'documento_de_autorizacion', 'documento_proteccion_de_datos','autorizacion_envio_informacion_comercial', 'poblacion', 'direccion' ]
    list_filter = ['centro__nombre_centro','fecha_alta','documento_de_autorizacion', 'documento_proteccion_de_datos','autorizacion_envio_informacion_comercial', 'poblacion' ]

class TecnicaAdmin(ImportExportModelAdmin):
    list_display= ['nombre_tecnica', 'apellidos_tecnica']
    search_fields = ['nombre_tecnica', 'apellidos_tecnica']
    list_filter =  ['nombre_tecnica', 'apellidos_tecnica']


class CitaAdmin(ImportExportModelAdmin):
    list_display= ['tecnica','fecha', 'zona']
    search_fields =  ['tecnica__nombre_tecnica','fecha', 'zona']
    list_filter =   ['tecnica__nombre_tecnica','fecha', 'zona']


class HorariosAdmin(ImportExportModelAdmin):
    list_display= ['tecnica','fecha', 'entrada', 'salida','trabajado']
    search_fields =  ['tecnica__nombre_tecnica','fecha', 'entrada', 'salida','trabajado']
    list_filter =   ['tecnica__nombre_tecnica','fecha', 'entrada', 'salida','trabajado']
    readonly_fields = ['tecnica','fecha', 'entrada', 'salida','trabajado']

    def horas_trabajadas(self, obj):
        entrada = dt.datetime.strptime(str(obj.entrada), '%H:%M:%S')
        salida = dt.datetime.strptime(str(obj.salida), '%H:%M:%S')
        result = (salida -  datetime.timedelta(hours=entrada.hour , minutes=entrada.minute, seconds=entrada.second)).time()
        return result

class ConfiguracionAdmin(ImportExportModelAdmin):
    list_display= ['nombre_comercial','propietario']
    search_fields =  ['nombre_comercial','propietario']
    list_filter =   ['nombre_comercial','propietario']

class TurnosAdmin(ImportExportModelAdmin):
    list_display= ['tecnica','centro', 'turno']
    search_fields =  ['tecnica__nombre_tecnica','centro__nombre_centro', 'turno']
    list_filter =   ['tecnica__nombre_tecnica','centro__nombre_centro', 'turno']

class TratamientosAdmin(ImportExportModelAdmin):
    list_display= ['fecha', 'cliente','js', 'jl', 'tecnica','comentario']
    search_fields =  ['fecha','tecnica', 'cliente']
    list_filter =   ['fecha','tecnica', 'cliente']

class ServiciosAdmin(ImportExportModelAdmin):
    list_display= ['nombre_servicio', 'duracion_sevicio']
    search_fields = ['nombre_servicio', 'duracion_sevicio']
    list_filter =   ['nombre_servicio', 'duracion_sevicio']

class StockAdmin(ImportExportModelAdmin):
    list_display= ['nombre_stock', 'cantidad']
    search_fields = ['nombre_stock', 'cantidad']
    list_filter =   ['nombre_stock', 'cantidad']

class ListaAdmin(ImportExportModelAdmin):
    list_display= ['centro', 'cliente', 'tecnica', 'hora_inicio', 'hora_fin' ]
    search_fields = [ 'cliente', 'tecnica', 'hora_inicio', 'hora_fin']
    list_filter =   ['centro__nombre_centro', 'cliente', 'tecnica', 'hora_inicio', 'hora_fin']

class EmailTemplatesAdmin(ImportExportModelAdmin):
    list_display= ['nombre', 'plantilla']
    search_fields =['nombre', 'plantilla']
    list_filter =   ['nombre', 'plantilla']

class CajasAdmin(ImportExportModelAdmin):
    list_display= ['centro', 'tecnica','porcentaje', 'cantidad_total', 'cantidad_total_centro']
    search_fields = ['centro__nombre_centro','tecnica','porcentaje', 'cantidad_total', 'cantidad_total_centro']
    list_filter =   ['centro__nombre_centro', 'tecnica','porcentaje', 'cantidad_total', 'cantidad_total_centro']




admin.site.site_header = "My Manager"
admin.site.site_title = "My Manager"
admin.site.index_title = "My Manager"

admin.site.register(EmailTemplates, EmailTemplatesAdmin)
admin.site.register(Lista, ListaAdmin)
admin.site.register(Cajas, CajasAdmin)
admin.site.register(Servicios, ServiciosAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(Centro, CentroAdmin)
admin.site.register(Configuracion, ConfiguracionAdmin)
admin.site.register(Tratamientos, TratamientosAdmin)
admin.site.register(Turnos, TurnosAdmin)
admin.site.register(Paciente, PacienteAdmin)
admin.site.register(DocTemplate)
admin.site.register(DocSings)
admin.site.register(Tecnica, TecnicaAdmin)
admin.site.register(Cita, CitaAdmin)
admin.site.register(ControlHorario, HorariosAdmin)
