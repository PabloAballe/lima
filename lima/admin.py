from django.contrib import admin

from .models import *

admin.site.register(Centro)
admin.site.register(Paciente)
admin.site.register(Tecnica)
admin.site.register(Potencia)
admin.site.register(Cita)

admin.site.site_header = "Lima y Neon"
admin.site.site_title = "Portal Lima y Neon"
admin.site.index_title = "Portal Lima y Neon"
