from django.contrib import admin
from .models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin
import datetime as dt
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class UserAdmin(UserAdmin):
    list_display = ('username','first_name', 'last_name','email',)
    fieldsets = (
        (None, {
            'fields': ('username','first_name', 'last_name','email','last_login','date_joined')
        }),
        ('Opciones Avanzadas', {
            'classes': ('collapse',),
            'fields': ('password', 'groups','user_permissions','is_staff','is_active',),
        }),
    )
    list_filter = ('is_staff', 'last_login','date_joined')
    search_fields = ['first_name', 'last_name','email' ]
    readonly_fields = ['password','is_active','date_joined', 'last_login']

class OrigenesAdmin(ImportExportModelAdmin):
    list_display= ['origen', 'fecha_creacion',]
    search_fields = ['origen', ]
    list_filter =  ['origen', 'fecha_creacion',]


class CentroAdmin(ImportExportModelAdmin):
    list_display= ['image_tag','nombre_centro', 'propietaria', 'localizacion']
    search_fields = ['nombre_centro', 'propietaria', 'localizacion']
    list_filter =  ['nombre_centro', 'propietaria', 'localizacion']
    readonly_fields = ['image_tag',]

class PacienteAdmin(ImportExportModelAdmin):
    list_display= ['id_paciente','image_tag','nombre_paciente', 'apellidos_paciente', 'telefono_paciente', 'email', 'documento_de_autorizacion','estado','documento_proteccion_de_datos','autorizacion_envio_informacion_comercial', 'poblacion', 'direccion' ]
    search_fields =['id_paciente','nombre_paciente', 'apellidos_paciente', 'telefono_paciente', 'email', 'poblacion', 'direccion' ]
    list_filter = ['centro__nombre_centro','fecha_alta','estado__nombre_estado','documento_de_autorizacion', 'documento_proteccion_de_datos','autorizacion_envio_informacion_comercial', 'poblacion', 'origen' ]
    readonly_fields = ['image_tag']

class TecnicaAdmin(ImportExportModelAdmin):
    list_display= ['image_tag','nombre_tecnica', 'apellidos_tecnica']
    search_fields = ['nombre_tecnica', 'apellidos_tecnica']
    list_filter =  ['nombre_tecnica', 'apellidos_tecnica']
    readonly_fields = ['image_tag']

class CitaAdmin(ImportExportModelAdmin):
    list_display= ['tecnica','fecha', 'zona']
    search_fields =  ['tecnica__nombre_tecnica','fecha', 'zona']
    list_filter =   ['tecnica__nombre_tecnica','fecha', 'zona']

class AnuncioAdmin(ImportExportModelAdmin):
    list_display= ['image_tag','cuerpo_anuncio','centro']
    search_fields = ['cuerpo_anuncio','centro__nombre_centro']
    list_filter =  ['activo','cuerpo_anuncio','centro__nombre_centro','todos_los_centros']
    readonly_fields = ['image_tag']

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
    list_display= ['image_tag','fecha', 'cliente','js', 'jl', 'tecnica','comentario']
    search_fields =  ['fecha','tecnica', 'cliente']
    list_filter =   ['fecha','tecnica', 'cliente']
    readonly_fields = ['image_tag']

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
    list_display= ['cliente', 'image_tag','tecnica', 'comentario', 'fecha']
    search_fields = ['cliente__nombre_paciente', 'tecnica__nombre_tecnica', 'comentario', 'fecha']
    list_filter =  ['cliente__nombre_paciente', 'tecnica__nombre_tecnica', 'comentario', 'fecha']
    readonly_fields=('fecha','image_tag',)

class CajasAdmin(ImportExportModelAdmin):
    list_display= ['centro', 'tecnica','porcentaje', 'cantidad_total', 'cantidad_total_centro']
    search_fields = ['centro__nombre_centro','tecnica','porcentaje', 'cantidad_total', 'cantidad_total_centro']
    list_filter =   ['centro__nombre_centro', 'tecnica','porcentaje', 'cantidad_total', 'cantidad_total_centro']
    readonly_fields=('cantidad_total_centro', 'cantidad_total_sistema', 'fecha')

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

class DocTemplateAdmin(ImportExportModelAdmin):
    list_display= ['nombre_doc','creado_el']
    search_fields =  ['nombre_doc','creado_el']
    list_filter =  ['nombre_doc','creado_el']

class DocSingsAdmin(ImportExportModelAdmin):
    list_display= ['cliente','image_tag','firmado_el']
    search_fields =  ['cliente__nombre_paciente','firmado_el']
    list_filter =  ['cliente__nombre_paciente','firmado_el']
    readonly_fields = ['image_tag']

admin.site.site_header = "WaveSense"
admin.site.site_title = "WaveSense"
admin.site.index_title = "WaveSense"

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Origenes, OrigenesAdmin)
admin.site.register(DocTemplate, DocTemplateAdmin)
admin.site.register(DocSings, DocSingsAdmin)
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
