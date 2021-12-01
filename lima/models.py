from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords
from django.dispatch import receiver
from django.db.models.signals import post_save
from datetime import date
import datetime
from django.utils import timezone
from colorfield.fields import ColorField
import datetime as dt
from jsignature.fields import JSignatureField
from jsignature.mixins import JSignatureFieldsMixin
from django_base64field.fields import Base64Field
from django.utils.timezone import now
from faicon.fields import FAIconField
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django_resized import ResizedImageField
import sys
from django.core.validators import RegexValidator
from multiselectfield import MultiSelectField
from django.utils.html import mark_safe
phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="El teléfono debe tener el siguiente formato: '+999999999'. Están permidos hasta 15 dígitos.")



class Servicios(models.Model):
    id_servicio=models.AutoField(primary_key=True, auto_created = True,editable = False)
    nombre_servicio=models.CharField(max_length=100,help_text="Ingrese el nombre del servicio" )
    duracion_sevicio=models.IntegerField(default="15")
    icon = FAIconField(default="", blank=True)

    class Meta:
        verbose_name_plural = "Servicios"

    def __str__(self):
        return self.nombre_servicio


DAYS_OF_WEEK = (('lunes', 'Lunes'),
              ('martes', 'Martes'),
              ('miercoles', 'Miercoles'),
              ('jueves', 'Jueves'),
              ('viernes', 'Viernes'),
              ('sabado', 'Sabado'),
              ('domingo', 'Domingo'))

class Centro(models.Model):
    id_centro=models.AutoField(primary_key=True, auto_created = True,editable = False)
    nombre_centro=models.CharField(max_length=50,help_text="Ingrese el nombre del centro", null=False)
    propietaria=models.CharField(max_length=50,help_text="Ingrese el nombre de la/el propietari@")
    imagen=ResizedImageField(size=[500, 500],upload_to='images/', default='img/porfile.png')
    horario_apertura=models.TimeField(auto_now=False, auto_now_add=False,help_text="Ingrese la hora de apertura de la clínica entre semana",default="09:00:00")
    horario_cierre=models.TimeField(auto_now=False, auto_now_add=False,help_text="Ingrese la hora de cierre de la clínica entre semana",default="21:00:00")
    telefono_centro=models.IntegerField(help_text="Ingrese el teléfono del centro", null=True, default=0, blank=True)
    localizacion=models.CharField(max_length=100,help_text="Ingrese la hubicación del centro")
    dias_abre_centro = MultiSelectField(choices=DAYS_OF_WEEK, default="lunes")
    habilitado=models.BooleanField(default=True)
    icon = FAIconField(default="", blank=True)

    class Meta:
        verbose_name_plural = "Centros"

    def __str__(self):
        return self.nombre_centro

    def image_tag(self):
        return mark_safe(f'<img src="{self.imagen.url}" width="50rem" height="50rem" style="border-radius:25%" />')

    image_tag.short_description = 'Imagen'



class EstadosClientes(models.Model):
    id_estado=models.AutoField(primary_key=True, auto_created = True,editable = False)
    nombre_estado=models.CharField(max_length=50,help_text="Ingrese el nombre del estado", null=False, default="Nuevo")
    color = ColorField(default='#FF0000',help_text="Color del estado")
    icon = FAIconField(default="", blank=True)

    class Meta:
        verbose_name_plural = "Estados de clientes"

    def __str__(self):
        return self.nombre_estado








def create_user_profile(sender, instance, created, **kwargs):
    if created:
       profile, created = Tecnica.objects.get_or_create(user=instance, nombre_tecnica=instance.username)

post_save.connect(create_user_profile, sender=User)

class Paneles(models.Model):
    id_panel=models.AutoField(primary_key=True, auto_created = True,editable = False)
    nombre_panel=models.CharField(max_length=50,help_text="Ingrese el nombre del estado", null=False)
    descripcion_panel=models.TextField(help_text="Ingrese la descripción del panel")
    icon = FAIconField(default="", blank=True)

    class Meta:
        verbose_name_plural = "Paneles del sistema"

    def __str__(self):
        return self.nombre_panel





class Estados(models.Model):
    id_estado=models.AutoField(primary_key=True, auto_created = True,editable = False)
    nombre_estado=models.CharField(max_length=50,help_text="Ingrese el nombre del estado", null=False)
    color = ColorField(default='#FF0000',help_text="Color del estado")
    panel=models.ForeignKey(Paneles, on_delete=models.RESTRICT, null=False, default="1")
    orden_del_estado=models.IntegerField(help_text="Ingrese el orden a aplicar", default=0 , null=False)
    centro=models.ForeignKey(Centro, on_delete=models.RESTRICT, null=False, default="1")
    icon = FAIconField(default="", blank=True)

    class Meta:
        verbose_name_plural = "Estados del sistema"

    def __str__(self):
        return self.nombre_estado



THEMES = [
    ('light', 'light'),
    ('dark', 'dark'),
    ('retro', 'retro'),
    ('cyberpunk', 'cyberpunk'),
    ('valentine', 'valentine'),
    ('garden', 'garden'),
    ('lofi', 'lofi')
]

class Tecnica(models.Model):
    id_tecnica=models.AutoField(primary_key=True, auto_created = True,editable = False)
    imagen=ResizedImageField(size=[500, 500],upload_to='images/', default='img/porfile.png')
    nombre_tecnica=models.CharField(max_length=50,help_text="Ingrese el nombre de la/el tecnic@")
    apellidos_tecnica=models.CharField(max_length=50,help_text="Ingrese los apellidos de la/el técnic@")
    centros=models.ManyToManyField(Centro, default="1")
    portales=models.ManyToManyField(Paneles, default="1",blank=True,related_name="portales")
    color = ColorField(default='#FF0000')
    tema=models.CharField(max_length=20, choices=THEMES, default='light')
    habilitado=models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.RESTRICT)
    icon = FAIconField(default="", blank=True)

    class Meta:
        verbose_name_plural = "Técnicas | Técnicos"

    def __str__(self):
        return self.nombre_tecnica

    def image_tag(self):
        return mark_safe(f'<img src="{self.imagen.url}" width="50rem" height="50rem" style="border-radius:25%" />')

    image_tag.short_description = 'Imagen'

class Tags(models.Model):
    id_tag=models.AutoField(primary_key=True, auto_created = True,editable = False)
    nombre_etiqueta=models.CharField(max_length=50,help_text="Ingrese el nombre de la etiqueta", null=False)
    color = ColorField(default='#FF0000',help_text="Color de la etiqueta")
    icon = FAIconField(default="", blank=True)

    class Meta:
        verbose_name_plural = "Etiquetas del sistema"

    def __str__(self):
        return self.nombre_etiqueta

class Tareas(models.Model):
    id_tarea=models.AutoField(primary_key=True, auto_created = True,editable = False)
    nombre_tarea=models.CharField(max_length=50,help_text="Ingrese el nombre del estado", null=False)
    color = ColorField(default='#FF0000',help_text="Color del estado")
    descripcion_tarea=models.TextField(help_text="Ingrese la descripción de la tarea", blank=True, default="")
    fecha_creacion=models.DateTimeField(null=False, default=now)
    estado=models.ForeignKey(Estados, on_delete=models.RESTRICT, null=False, default="1")
    etiquetas=models.ManyToManyField(Tags, default="1", blank=True)
    propietario=models.ForeignKey(Tecnica, on_delete=models.RESTRICT, null=False, default="1")
    icon = FAIconField(default="", blank=True)

    class Meta:
        verbose_name_plural = "Tareas del sistema"

    def __str__(self):
        return self.nombre_tarea


class Anuncios(models.Model):
    id_anuncio=models.AutoField(primary_key=True, auto_created = True,editable = False)
    cuerpo_anuncio=models.CharField(max_length=100,help_text="Ingrese el anuncio", null=False)
    link_anuncio=models.CharField(help_text="Ingrese el link del anuncio",  default="", blank=True,max_length=10000)
    centro=models.ForeignKey(Centro, on_delete=models.RESTRICT, default="1")
    todos_los_centros=models.BooleanField(default=False,help_text="Enviar anuncio a todos los centro")
    imagen=ResizedImageField(size=[500, 500],upload_to='images/')
    activo=models.BooleanField(default=True,help_text="Determina si el auncio está activo")
    fecha_creacion=models.DateTimeField(null=False, default=now)

    class Meta:
        verbose_name_plural = "Anúncios del sistema"

    def __str__(self):
        return self.cuerpo_anuncio

    def image_tag(self):
        return mark_safe(f'<img src="{self.imagen.url}" width="50rem" height="50rem" style="border-radius:25%" />')

    image_tag.short_description = 'Imagen'

def allEstados():
    estados = EstadosClientes.objects.all()
    return estados


class Origenes(models.Model):
    id=models.AutoField(primary_key=True, auto_created = True,editable = False)
    origen=models.CharField(max_length=100,help_text="Ingrese el nombre del servicio" )
    fecha_creacion=models.DateTimeField(null=False, default=now)

    class Meta:
        verbose_name_plural = "Origenes"

    def __str__(self):
        return self.origen

class Paciente(models.Model):
    id_paciente=models.AutoField(primary_key=True, auto_created = True, null=False,editable = False)
    nombre_paciente=models.CharField(max_length=50,help_text="Ingrese el nombre de la/el paciente", null=False)
    apellidos_paciente=models.CharField(max_length=50,help_text="Ingrese los apellidos de la/el paciente", blank=True, default="")
    imagen=ResizedImageField(size=[500, 500],upload_to='images/', default='img/porfile.png',blank=True)
    telefono_paciente=models.CharField(max_length=17,help_text="Ingrese el teléfono de la/el paciente", default=0,validators=[phone_regex], blank=True )
    email=models.EmailField(help_text="Ingrese el correo electronico de la/el paciente", blank=True, default="")
    dni=models.CharField(max_length=50,help_text="Ingrese el DNI del cliente", default="", blank=True)
    documento_de_autorizacion=models.BooleanField(default=False)
    documento_proteccion_de_datos=models.BooleanField(default=False)
    centro=models.ForeignKey(Centro, on_delete=models.RESTRICT)
    poblacion=models.CharField(max_length=50,help_text="Ingrese la población del/la paciente",  default='Valencia',blank=True,null=True)
    direccion=models.CharField(max_length=50,help_text="Ingrese la dirección del/la paciente",  default='Valencia',blank=True,null=True)
    notas_paciente=models.TextField(help_text="Ingrese notas sobre el cliente aquí", default="", blank=True,null=True)
    fecha_nacimiento=models.DateTimeField( default='2000-01-01',blank=True,null=True)
    estado=models.ForeignKey(EstadosClientes, default="1",  on_delete=models.RESTRICT,blank=True,null=True)
    etiqueta=models.ManyToManyField(Tags, default="1", blank=True,null=True)
    autorizacion_envio_informacion_comercial=models.BooleanField(default=False,null=True)
    fecha_alta=models.DateTimeField(null=False, default=now)
    origen=models.ForeignKey(Origenes, on_delete=models.RESTRICT, blank=True,null=True)
    icon = FAIconField(default="", blank=True)

    class Meta:
        verbose_name_plural = "Clientes"

    def __str__(self):
        return self.nombre_paciente

    def image_tag(self):
        return mark_safe(f'<img src="{self.imagen.url}" width="50rem" height="50rem" style="border-radius:25%" />')

    image_tag.short_description = 'Imagen'



class Mensajes(models.Model):
    id_mensaje=models.AutoField(primary_key=True, auto_created = True,editable = False)
    enviado_por=models.ForeignKey(Tecnica, on_delete=models.RESTRICT, null=False)
    tarea=models.ForeignKey(Tareas, on_delete=models.RESTRICT, null=False, default="1")
    cuerpo_mensaje=models.TextField(help_text="Ingrese la descripción aquí")
    fecha_creacion=models.DateTimeField(null=False, default=now)

    class Meta:
        verbose_name_plural = "Paneles del sistema"

    def __str__(self):
        return self.nombre_panel

class Cita(models.Model):
    id_cita=models.AutoField(primary_key=True, auto_created = True,editable = False)
    tecnica=models.ForeignKey(Tecnica, on_delete=models.RESTRICT, null=False)
    paciente=models.ForeignKey(Paciente, on_delete=models.RESTRICT , null=False)
    fecha=models.DateTimeField(null=False)
    horafin=models.DateTimeField(null=False,default=now )
    zona=models.ForeignKey(Servicios, on_delete=models.RESTRICT, default="1")
    hertz=models.IntegerField(help_text="Ingrese la potencia en hertz", default=0 , null=False)
    milisegundos=models.IntegerField(help_text="Ingrese la potencia en milisegundos",  default=0, null=False)
    julios=models.IntegerField( help_text="Ingrese la potencia en julios",  default=0, null=False)
    icon = FAIconField(default="", blank=True)

    def save(self):
        entrada = dt.datetime.strptime(str(self.zona.duracion_sevicio), '%M')
        salida = dt.datetime.strptime(str(self.fecha), '%Y-%m-%d %H:%M:%S')
        self.horafin = (salida +  datetime.timedelta(hours=entrada.hour , minutes=entrada.minute, seconds=entrada.second)).time().strftime("%Y-%m-%d %H:%M:%S")
        return super(Cita, self).save()


    class Meta:
        verbose_name_plural = "Zonas de tratamientos"

    def __str__(self):
        return f"Zona : {self.fecha}"

class ControlHorario(models.Model):
    tecnica=models.ForeignKey(Tecnica, on_delete=models.RESTRICT,auto_created = True, default="lima",editable = False)
    fecha=models.DateField()
    entrada=models.TimeField()
    salida=models.TimeField(default=None, blank=True, null=True)
    trabajado=models.TimeField(default="00:00")
    icon = FAIconField(default="", blank=True)

    def save(self):
        if self.salida:
            entrada = dt.datetime.strptime(str(self.entrada), '%H:%M:%S.%f')
            salida = dt.datetime.strptime(str(self.salida), '%H:%M:%S.%f')
            self.trabajado = (salida -  datetime.timedelta(hours=entrada.hour , minutes=entrada.minute, seconds=entrada.second)).time()
            return super(ControlHorario, self).save()
        else:
            return super(ControlHorario, self).save()

    class Meta:
        verbose_name_plural = "Control Horario"

    def __str__(self):
        return f"Fichages : {self.fecha}"

your_date = datetime.datetime.now()
class Turnos(models.Model):
    id_turno=models.AutoField(primary_key=True, auto_created = True,editable = False)
    tecnica=models.ForeignKey(Tecnica, on_delete=models.RESTRICT,auto_created = True, default="lima")
    centro=models.ForeignKey(Centro, on_delete=models.RESTRICT)
    turno_inicio=models.DateTimeField(null=False, default=timezone.now)
    turno_fin=models.DateTimeField(null=False, default=timezone.now)
    icon = FAIconField(default="", blank=True)

    class Meta:
        verbose_name_plural = "Turnos de trabajo"

    def __str__(self):
        return f"Turno de la técnica : {self.tecnica}"

class EmailTemplates(models.Model):
    id=models.AutoField(primary_key=True, auto_created = True,editable = False)
    nombre=models.CharField(max_length=100,help_text="Ingrese el nombre de la plantilla" )
    plantilla=models.TextField(help_text="Confifure su plantilla")

    class Meta:
        verbose_name_plural = "Plantillas de email"

    def __str__(self):
        return f"Plantilla : {self.nombre}"

class DocTemplate(models.Model):
    id=models.AutoField(primary_key=True, auto_created = True,editable = False)
    nombre_doc=models.CharField(max_length=100,help_text="Ingrese el nombre de la plantilla" )
    plantilla_doc=models.TextField(help_text="Configure su plantilla")
    creado_el=models.DateTimeField(null=False, auto_now_add=True,)


    class Meta:
        verbose_name_plural = "Plantillas de documentos"

    def __str__(self):
        return f"Plantilla Documento : {self.nombre_doc}"

class DocSings(models.Model):
    id=models.AutoField(primary_key=True, auto_created = True,editable = False)
    plantilla_doc=models.ForeignKey(DocTemplate, on_delete=models.RESTRICT)
    cliente=models.ForeignKey(Paciente, on_delete=models.RESTRICT , null=False)
    plantilla_document=models.TextField(help_text="Configure su plantilla",default='')
    firma=ResizedImageField(size=[500, 500],upload_to='images/signatures/', default='')
    firmado_el=models.DateTimeField(null=False, auto_now_add=True)


    class Meta:
        verbose_name_plural = "Documentos firmados"

    def __str__(self):
        return f"Firmado el : {self.firmado_el}"

    def image_tag(self):
        return mark_safe(f'<img src="{self.firma.url}" width="50rem" height="50rem" style="border-radius:25%" />')

    image_tag.short_description = 'Imagen'

class Configuracion(models.Model):
    id=models.AutoField(primary_key=True, auto_created = True,editable = False)
    nombre_comercial=models.CharField(max_length=100,help_text="Ingrese el nombre comercial del negocio" , null=False)
    propietario=models.CharField(max_length=100,help_text="Ingrese el nombre del propietario del negocio" , null=False)
    telefono=models.CharField(max_length=100,help_text="Ingrese el telefono del negocio", default="00000000" )
    email_sistema=models.EmailField(max_length=100,help_text="Ingrese el Email del negocio", default="hola@minegocio.com" )
    email_nueva_caja=models.EmailField(max_length=100,help_text="Ingrese el Email donde se enviarán los correos de nueva caja", default="hola@me.com" )
    email_nuevo_fichaje=models.EmailField(max_length=100,help_text="Ingrese el Email donde se enviarán los correos de nuevos fichajes", default="hola@me.com" )
    logo=ResizedImageField(size=[500, 500],upload_to='images/', default='img/login.png')
    slots=models.IntegerField(default='15', help_text="Ingrese el tamaño de los slots")
    tiempo_expira_caja=models.IntegerField(default='15', help_text="Ingrese el tamaño de los slots")
    numero_citas=models.IntegerField(default='1', help_text="Ingrese la cantidad de citas que se pueden agendar por el módulo online")
    politica=models.TextField(help_text="Ingrese la política  de la empresa que aparecera en la parte inferior de los textos", blank=True)
    twilio_SENDGRID_API_KEY=models.CharField(max_length=500,help_text="Ingrese la SENDGRID API KEY de Twilio", default="" , blank=True)
    twilio_ACCOUNT_SID=models.CharField(max_length=500,help_text="Ingrese la ACCOUNT SID de Twilio", default="" , blank=True)
    twilio_AUTH_TOKEN=models.CharField(max_length=500,help_text="Ingrese el AUTH TOKEN de Twilio", default="" , blank=True)
    twilio_NUMBER=models.CharField(max_length=17,help_text="Ingrese el Número verificado en Twilio", default=0,validators=[phone_regex], blank=True )
    enviar_email_nuevos_clientes=models.BooleanField(default=False)
    enviar_email_nuevo_fichaje=models.BooleanField(default=False)
    enviar_email_nueva_caja=models.BooleanField(default=False)
    enviar_email_nuevas_listas=models.BooleanField(default=False)
    plantilla_email=models.ForeignKey(EmailTemplates, on_delete=models.RESTRICT ,default="1",related_name ="plantilla_email" )
    plantilla_lista=models.ForeignKey(EmailTemplates, on_delete=models.RESTRICT ,default="1",related_name ="plantilla_lista")
    icon = FAIconField(default="", blank=True)

    class Meta:
        verbose_name_plural = "Configuración del sistema"

    def __str__(self):
        return f"Configuración {self.nombre_comercial}"

    def image_tag(self):
        return mark_safe(f'<img src="{self.logo.url}" width="50rem" height="50rem" style="border-radius:25%" />')

    image_tag.short_description = 'Imagen'


class Tratamientos(models.Model):
    id_tratamiento=models.AutoField(primary_key=True, auto_created = True,editable = False)
    numero_de_sesion=models.IntegerField(help_text="Ingrese el número de sesión del tratamiento" , default=1)
    zona=models.ForeignKey(Servicios, on_delete=models.RESTRICT, default="1")
    hora_fin=models.DateTimeField(null=False,default=now)
    cliente=models.ForeignKey(Paciente, on_delete=models.RESTRICT)
    fecha=models.DateTimeField(default="2000-01-01")
    js=models.IntegerField(help_text="Ingrese los J/S" )
    jl=models.IntegerField(help_text="Ingrese los J/L" )
    tecnica=models.ForeignKey(Tecnica, on_delete=models.RESTRICT)
    comentario=models.CharField(max_length=100,help_text="Ingrese el comentario del tratamiento", blank=True, default="" )
    firma=ResizedImageField(size=[500, 500],upload_to='images/signatures/', default='',blank=True)
    icon = FAIconField(default="", blank=True)

    def save(self):
        self.hora_fin = (self.fecha +  dt.timedelta(minutes=self.zona.duracion_sevicio))
        return super(Tratamientos, self).save()

    class Meta:
        verbose_name_plural = "Sesiones de Tratamientos agendados"

    def __str__(self):
        return f"Sesión de tratamiento con fecha : {self.fecha}"

    def image_tag(self):
        if self.firma:
            return mark_safe(f'<img src="{self.firma.url}" width="50rem" height="50rem" style="border-radius:25%" />')
        else:
            return mark_safe(f'&nbsp;')


    image_tag.short_description = 'Imagen'

class Suscription(models.Model):
    OPCIONES_SUSCRIPTIONS = (
    ('S', 'Suscripción'),
    ('E', 'Extras'),
    ('O', 'Otras')  # hay que ser inclusivos
)
    id_sicription=models.AutoField(primary_key=True, auto_created = True,editable = False)
    nombre_suscription=models.CharField(max_length=100,help_text="Ingrese el nombre de la suscripción" )
    clinicas_max=models.IntegerField(default='0', help_text="Ingrese el número máximo de clínicas en la suscripción")
    type=models.CharField(max_length=1, choices=OPCIONES_SUSCRIPTIONS, default="S")
    precio=models.DecimalField(help_text="Ingrese la cantidad pagada por la suscripción", default=0,max_digits=20, decimal_places=2)
    coments_suscription=models.TextField(help_text="Comentarios de la suscripción")
    stardate=models.DateTimeField(null=False, auto_now_add=True)
    enddate=models.DateTimeField(null=False, auto_now_add=True)
    pagada=models.BooleanField(default=False)



class Stock(models.Model):
    id_stock=models.AutoField(primary_key=True, auto_created = True,editable = False)
    nombre_stock=models.CharField(max_length=100,help_text="Ingrese el producto" )
    tecnica=models.ForeignKey(Tecnica, on_delete=models.RESTRICT, default="1")
    cantidad=models.IntegerField(help_text="Ingrese la cantidad de stock del producto")
    creado_el=models.DateTimeField(null=False, auto_now_add=True,)
    icon = FAIconField(default="", blank=True)

    class Meta:
        verbose_name_plural = "Stock de productos"

    def __str__(self):
        return f"Stock del producto : {self.nombre_stock}"

class Cajas(models.Model):
    id_caja=models.AutoField(primary_key=True, auto_created = True,editable = False)
    centro=models.ForeignKey(Centro, on_delete=models.RESTRICT)
    tecnica=models.ForeignKey(Tecnica, on_delete=models.RESTRICT)
    porcentaje=models.IntegerField(help_text="Ingrese el porcentaje del centro")
    cantidad_efectivo=models.DecimalField(help_text="Ingrese la cantidad de efectivo", default=0.00,max_digits=20, decimal_places=2)
    cantidad_tarjeta=models.DecimalField(help_text="Ingrese la cantidad en tarjeta", default=0,max_digits=20, decimal_places=2,)
    cantidad_total=models.DecimalField(help_text="Cantidad total", default=0,max_digits=20, decimal_places=2,)
    cantidad_total_centro=models.DecimalField(help_text="Total Centro", default=0,max_digits=20, decimal_places=2,)
    cantidad_total_sistema=models.DecimalField(help_text="Total Sistema", default=0,max_digits=20, decimal_places=2,)
    comentario=models.CharField(max_length=100,help_text="Ingrese el comentario de la caja", default="", blank=True )
    fecha=models.DateTimeField(null=False, auto_now_add=True)
    icon = FAIconField(default="", blank=True)

    def save(self):
        self.cantidad_total=self.cantidad_efectivo+self.cantidad_tarjeta
        self.cantidad_total_centro=(self.porcentaje * self.cantidad_total) / 100
        self.cantidad_total_sistema=self.cantidad_total - self.cantidad_total_centro
        return super(Cajas, self).save()

    class Meta:
        verbose_name_plural = "Cajas del día"

    def __str__(self):
        return f"Caja del día : {self.fecha}"

class Lista(models.Model):
    id_lista=models.AutoField(primary_key=True, auto_created = True,editable = False)
    centro=models.ForeignKey(Centro, on_delete=models.RESTRICT)
    cliente=models.ForeignKey(Paciente, on_delete=models.RESTRICT)
    tecnica=models.ForeignKey(Tecnica, on_delete=models.RESTRICT, default="1")
    servicios=models.ForeignKey(Servicios, on_delete=models.RESTRICT, default="1")
    hora_inicio=models.DateTimeField(null=False,default=now)
    hora_fin=models.DateTimeField(null=False,default=now)
    is_app=models.BooleanField(default=False)
    icon = FAIconField(default="", blank=True)

    def clean_date(self):
        date = self.cleaned_data['hora_inicio']
        if date < datetime.now():
            raise forms.ValidationError("Debe ingresar una fecha a futuro para la cita")
        return date

    class Meta:
        verbose_name_plural = "Listas de clientes"

    def __str__(self):
        return f"Lista de cliente  : {self.centro.nombre_centro}"

class ImagenesClientes(models.Model):
    id_image_cliente=models.AutoField(primary_key=True, auto_created = True,editable = False)
    #imagen=models.ImageField(upload_to='images/clientes/')
    imagen=ResizedImageField(size=[500, 500], upload_to='images/clientes/')
    cliente=models.ForeignKey(Paciente, on_delete=models.RESTRICT , null=False)
    comentario=models.CharField(max_length=100,help_text="Ingrese el comentario de la imágen", default="", blank=True )
    tecnica=models.ForeignKey(Tecnica, on_delete=models.RESTRICT, default="1")
    fecha=models.DateTimeField(null=False, auto_now_add=True)
    icon = FAIconField(default="", blank=True)

    def image_tag(self):
        return mark_safe(f'<img src="{self.imagen.url}" width="50rem" height="50rem" style="border-radius:25%" />')

    image_tag.short_description = 'Imagen'

    class Meta:
        verbose_name_plural = "Listas de imágenes de clientes"

    def __str__(self):
        return f"Imágen del cliente  : {self.cliente.nombre_paciente}"
