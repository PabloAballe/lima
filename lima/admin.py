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
    list_display= ['nombre_paciente', 'apellidos_paciente', 'telefono_paciente', 'email', 'documento_de_autorizacion','estado','documento_proteccion_de_datos','autorizacion_envio_informacion_comercial', 'poblacion', 'direccion' ]
    search_fields =['nombre_paciente', 'apellidos_paciente', 'telefono_paciente', 'email', 'documento_de_autorizacion','estado', 'documento_proteccion_de_datos','autorizacion_envio_informacion_comercial', 'poblacion', 'direccion' ]
    list_filter = ['centro__nombre_centro','fecha_alta','estado__nombre_estado','documento_de_autorizacion', 'documento_proteccion_de_datos','autorizacion_envio_informacion_comercial', 'poblacion' ]

class TecnicaAdmin(ImportExportModelAdmin):
    list_display= ['nombre_tecnica', 'apellidos_tecnica']
    search_fields = ['nombre_tecnica', 'apellidos_tecnica']
    list_filter =  ['nombre_tecnica', 'apellidos_tecnica']


class CitaAdmin(ImportExportModelAdmin):
    list_display= ['tecnica','fecha', 'zona']
    search_fields =  ['tecnica__nombre_tecnica','fecha', 'zona']
    list_filter =   ['tecnica__nombre_tecnica','fecha', 'zona']

class AnuncioAdmin(ImportExportModelAdmin):
    list_display= ['cuerpo_anuncio','centro']
    search_fields = ['cuerpo_anuncio','centro__nombre_centro']
    list_filter =  ['cuerpo_anuncio','centro__nombre_centro']

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



class TurnosAdmin(ImportExportModelAdmin):
    list_display= ['tecnica','centro',  'turno_inicio', 'turno_fin']
    search_fields =  ['tecnica__nombre_tecnica','centro__nombre_centro', 'turno_inicio', 'turno_fin']
    list_filter =   ['tecnica__nombre_tecnica','centro__nombre_centro', 'turno_inicio', 'turno_fin']

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

class ImagenesClientesAdmin(ImportExportModelAdmin):
    list_display= ['cliente', 'tecnica', 'comentario', 'fecha']
    search_fields = ['cliente__nombre_paciente', 'tecnica__nombre_tecnica', 'comentario', 'fecha']
    list_filter =  ['cliente__nombre_paciente', 'tecnica__nombre_tecnica', 'comentario', 'fecha']

class CajasAdmin(ImportExportModelAdmin):
    list_display= ['centro', 'tecnica','porcentaje', 'cantidad_total', 'cantidad_total_centro']
    search_fields = ['centro__nombre_centro','tecnica','porcentaje', 'cantidad_total', 'cantidad_total_centro']
    list_filter =   ['centro__nombre_centro', 'tecnica','porcentaje', 'cantidad_total', 'cantidad_total_centro']

class EstadosClientesAdmin(ImportExportModelAdmin):
    list_display= ['nombre_estado', 'color']
    search_fields = ['nombre_estado', 'color']
    list_filter = ['nombre_estado', 'color']

class PanelesAdmin(ImportExportModelAdmin):
    list_display= ['nombre_panel', 'descripcion_panel']
    search_fields = ['nombre_panel', 'descripcion_panel']
    list_filter = ['nombre_panel', 'descripcion_panel']

class EstadosAdmin(ImportExportModelAdmin):
    list_display= ['nombre_estado', 'orden_del_estado','panel','centro']
    search_fields = ['nombre_estado','orden_del_estado', 'panel__nombre_panel','centro__nombre_centro']
    list_filter =  ['nombre_estado', 'panel__nombre_panel','centro__nombre_centro']

class TareasAdmin(ImportExportModelAdmin):
    list_display= ['nombre_tarea', 'fecha_creacion','estado', 'propietario']
    search_fields = ['nombre_tarea', 'fecha_creacion','estado__nombre_estado', 'propietario__nombre_tecnica']
    list_filter =  ['nombre_tarea', 'fecha_creacion','estado__nombre_estado', 'propietario__nombre_tecnica']

class TagsAdmin(ImportExportModelAdmin):
    list_display= ['nombre_etiqueta']
    search_fields = ['nombre_etiqueta']
    list_filter =  ['nombre_etiqueta']

admin.site.site_header = "My Manager"
admin.site.site_title = "My Manager"
admin.site.index_title = "My Manager"



admin.site.register(EstadosClientes, EstadosClientesAdmin)
admin.site.register(Paneles, PanelesAdmin)
admin.site.register(Anuncios, AnuncioAdmin)
admin.site.register(Estados, EstadosAdmin)
admin.site.register(Tareas, TareasAdmin)
admin.site.register(Tags, TagsAdmin)
admin.site.register(ImagenesClientes, ImagenesClientesAdmin)
admin.site.register(Lista, ListaAdmin)
admin.site.register(Cajas, CajasAdmin)
admin.site.register(Servicios, ServiciosAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(Centro, CentroAdmin)
admin.site.register(Tratamientos, TratamientosAdmin)
admin.site.register(Turnos, TurnosAdmin)
admin.site.register(Paciente, PacienteAdmin)
admin.site.register(Tecnica, TecnicaAdmin)
admin.site.register(Cita, CitaAdmin)
admin.site.register(ControlHorario, HorariosAdmin)
