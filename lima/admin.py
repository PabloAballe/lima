from django.contrib import admin

from .models import *





class CentroAdmin(admin.ModelAdmin):
    list_display= ['nombre_centro', 'propietaria', 'localizacion']
    search_fields = ['nombre_centro', 'propietaria', 'localizacion']
    list_filter =  ['nombre_centro', 'propietaria', 'localizacion']

class PacienteAdmin(admin.ModelAdmin):
    list_display= ['nombre_paciente', 'apellidos_paciente', 'telefono_paciente', 'email', 'autorizacion', 'protec_datos','poblacion', 'direccion' ]
    search_fields =['nombre_paciente', 'apellidos_paciente', 'telefono_paciente', 'email', 'autorizacion', 'protec_datos','poblacion', 'direccion' ]
    list_filter =  ['nombre_paciente', 'apellidos_paciente', 'telefono_paciente', 'email', 'autorizacion', 'protec_datos','poblacion', 'direccion' ]

class TecnicaAdmin(admin.ModelAdmin):
    list_display= ['nombre_tecnica', 'apellidos_tecnica']
    search_fields = ['nombre_tecnica', 'apellidos_tecnica']
    list_filter =  ['nombre_tecnica', 'apellidos_tecnica']

class PotenciaAdmin(admin.ModelAdmin):
    list_display= ['hertz', 'milisegundos', 'julios']
    search_fields = ['hertz', 'milisegundos', 'julios']
    list_filter =  ['hertz', 'milisegundos', 'julios']

class CitaAdmin(admin.ModelAdmin):
    list_display= ['fecha', 'zona', 'comentario']
    search_fields =  ['fecha', 'zona', 'comentario']
    list_filter =   ['fecha', 'zona', 'comentario']



admin.site.site_header = "Lima y Neon"
admin.site.site_title = "Portal Lima y Neon"
admin.site.index_title = "Portal Lima y Neon"




admin.site.register(Centro, CentroAdmin)
admin.site.register(Paciente, PacienteAdmin)
admin.site.register(Tecnica, TecnicaAdmin)
admin.site.register(Potencia, PotenciaAdmin)
admin.site.register(Cita, CitaAdmin)
