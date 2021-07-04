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

# Create your models here.

class Centro(models.Model):
    id_centro=models.AutoField(primary_key=True, auto_created = True)
    nombre_centro=models.CharField(max_length=50,help_text="Ingrese el nombre del centro", null=False)
    propietaria=models.CharField(max_length=50,help_text="Ingrese el nombre de la/el propietari@")
    localizacion=models.CharField(max_length=100,help_text="Ingrese la hubicación del centro")
    habilitado=models.BooleanField(default=True)
    history = HistoricalRecords()


    class Meta:
        verbose_name_plural = "Centros"

    def __str__(self):
        return self.nombre_centro



class Paciente(models.Model):
    id_paciente=models.AutoField(primary_key=True, auto_created = True, null=False)
    nombre_paciente=models.CharField(max_length=50,help_text="Ingrese el nombre de la/el paciente", null=False)
    apellidos_paciente=models.CharField(max_length=50,help_text="Ingrese los apellidos de la/el paciente", null=False)
    telefono_paciente=models.IntegerField(help_text="Ingrese el teléfono de la/el paciente")
    email=models.EmailField(help_text="Ingrese el correo electronico de la/el paciente")
    dni=models.CharField(max_length=50,help_text="Ingrese el DNI del cliente", default="")
    autorizacion=models.BooleanField(default=False)
    protec_datos=models.BooleanField(default=False)
    centro=models.ForeignKey(Centro, on_delete=models.RESTRICT)
    poblacion=models.CharField(max_length=50,help_text="Ingrese la población del/la paciente",  default='Valencia')
    direccion=models.CharField(max_length=50,help_text="Ingrese la dirección del/la paciente",  default='Valencia')
    history = HistoricalRecords()

    class Meta:
        verbose_name_plural = "Clientes"

    def __str__(self):
        return self.nombre_paciente

class Tecnica(models.Model):
    id_tecnica=models.AutoField(primary_key=True, auto_created = True)
    imagen=models.ImageField(upload_to='images/', default='img/porfile.png')
    nombre_tecnica=models.CharField(max_length=50,help_text="Ingrese el nombre de la/el tecnic@")
    apellidos_tecnica=models.CharField(max_length=50,help_text="Ingrese los apellidos de la/el técnic@")
    color = ColorField(default='#FF0000')
    habilitado=models.BooleanField(default=True)
    history = HistoricalRecords()
    user = models.OneToOneField(User, on_delete=models.RESTRICT)

    class Meta:
        verbose_name_plural = "Técnicas | Técnicos"

    def __str__(self):
        return self.nombre_tecnica

def create_user_profile(sender, instance, created, **kwargs):
    if created:
       profile, created = Tecnica.objects.get_or_create(user=instance, nombre_tecnica=instance.username)

post_save.connect(create_user_profile, sender=User)

class Cita(models.Model):
    id_cita=models.AutoField(primary_key=True, auto_created = True)
    tecnica=models.ForeignKey(Tecnica, on_delete=models.RESTRICT, null=False)
    paciente=models.ForeignKey(Paciente, on_delete=models.RESTRICT , null=False)
    fecha=models.DateTimeField(null=False)
    zona=models.CharField(max_length=50,help_text="Ingrese la zona tratada o por tratar" , null=False)
    hertz=models.IntegerField(help_text="Ingrese la potencia en hertz", default=0 , null=False)
    milisegundos=models.IntegerField(help_text="Ingrese la potencia en milisegundos",  default=0, null=False)
    julios=models.IntegerField( help_text="Ingrese la potencia en julios",  default=0, null=False)
    history = HistoricalRecords()


    class Meta:
        verbose_name_plural = "Zonas"

    def __str__(self):
        return f"Zona : {self.fecha}"

class ControlHorario(models.Model):
    tecnica=models.ForeignKey(Tecnica, on_delete=models.RESTRICT,auto_created = True, default="lima")
    fecha=models.DateField()
    entrada=models.TimeField()
    salida=models.TimeField(default=None, blank=True, null=True)
    history = HistoricalRecords()
    trabajado=models.TimeField(default="00:00")

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

class Turnos(models.Model):
    id_turno=models.AutoField(primary_key=True, auto_created = True)
    tecnica=models.ForeignKey(Tecnica, on_delete=models.RESTRICT,auto_created = True, default="lima")
    centro=models.ForeignKey(Centro, on_delete=models.RESTRICT)
    turno=models.DateTimeField(null=False)
    history = HistoricalRecords()

    class Meta:
        verbose_name_plural = "Turnos de trabajo"

    def __str__(self):
        return f"Turno de la técnica : {self.tecnica}"

class EmailTemplates(models.Model):
    id=models.AutoField(primary_key=True, auto_created = True)
    nombre=models.CharField(max_length=100,help_text="Ingrese el nombre de la plantilla" )
    plantilla=models.TextField(help_text="Confifure su plantilla")
    history = HistoricalRecords()

    class Meta:
        verbose_name_plural = "Plantillas de email"

    def __str__(self):
        return f"Plantilla : {self.nombre}"

class DocTemplate(models.Model):
    id=models.AutoField(primary_key=True, auto_created = True)
    nombre_doc=models.CharField(max_length=100,help_text="Ingrese el nombre de la plantilla" )
    plantilla_doc=models.TextField(help_text="Confifure su plantilla")
    creado_el=models.DateTimeField(null=False, auto_now_add=True,)
    history = HistoricalRecords()

    class Meta:
        verbose_name_plural = "Plantillas de documentos"

    def __str__(self):
        return f"Plantilla Documento : {self.nombre_doc}"

class DocSings(models.Model):
    id=models.AutoField(primary_key=True, auto_created = True)
    plantilla_doc=models.ForeignKey(DocTemplate, on_delete=models.RESTRICT)
    plantilla_render=models.TextField(default="")
    cliente=models.ForeignKey(Paciente, on_delete=models.RESTRICT , null=False)
    firmado_el=models.DateTimeField(null=False, auto_now_add=True)
    firma=JSignatureField(null=True , blank=True)
    firma_imagen=models.CharField(max_length=100,help_text="Ingrese la url de la firma" )

    class Meta:
        verbose_name_plural = "Documentos firmados"

    def __str__(self):
        return f"Firmado el : {self.firmado_el}"

class Configuracion(models.Model):
    id=models.AutoField(primary_key=True, auto_created = True)
    nombre_comercial=models.CharField(max_length=100,help_text="Ingrese el nombre comercial del negocio" , null=False)
    propietario=models.CharField(max_length=100,help_text="Ingrese el nombre del propietario del negocio" , null=False)
    telefono=models.CharField(max_length=100,help_text="Ingrese el telefono del negocio", default="00000000" )
    email=models.CharField(max_length=100,help_text="Ingrese el Email del negocio", default="hola@minegocio.com" )
    logo=models.ImageField(upload_to='images/', default='img/login.png')
    slots=models.IntegerField(default='15', help_text="Ingrese el tamaño de los slots")
    politica=models.TextField(help_text="Ingrese la política  de la empresa que aparecera en la parte inferior de los textos")
    email_nuevos_clientes=models.BooleanField(default=True)
    plantilla_email=models.ForeignKey(EmailTemplates, on_delete=models.RESTRICT , blank=True, default="1")
    history = HistoricalRecords()

    class Meta:
        verbose_name_plural = "Configuración del sistema"

    def __str__(self):
        return f"Configuración {self.nombre_comercial}"



class Tratamientos(models.Model):
    id_tratamiento=models.AutoField(primary_key=True, auto_created = True)
    cliente=models.ForeignKey(Paciente, on_delete=models.RESTRICT)
    fecha=models.DateField()
    js=models.CharField(max_length=100,help_text="Ingrese los J/S" )
    jl=models.CharField(max_length=100,help_text="Ingrese los J/L" )
    tecnica=models.ForeignKey(Tecnica, on_delete=models.RESTRICT)
    comentario=models.CharField(max_length=100,help_text="Ingrese el comentario del tratamiento" )

    class Meta:
        verbose_name_plural = "Tratamientos agendados"

    def __str__(self):
        return f"Tratamiento con fecha : {self.fecha}"


class Suscription(models.Model):
    OPCIONES_SUSCRIPTIONS = (
    ('S', 'Suscripción'),
    ('E', 'Extras'),
    ('O', 'Otras')  # hay que ser inclusivos
)
    id_sicription=models.AutoField(primary_key=True, auto_created = True)
    nombre_suscription=models.CharField(max_length=100,help_text="Ingrese el nombre de la suscripción" )
    type=models.CharField(max_length=1, choices=OPCIONES_SUSCRIPTIONS, default="S")
    coments_suscription=models.TextField(help_text="Comentarios de la suscripción")
    stardate=models.DateTimeField(null=False, auto_now_add=True)
    enddate=models.DateTimeField(null=False, auto_now_add=True)
    pagada=models.BooleanField(default=False)
