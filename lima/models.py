from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords
from django.dispatch import receiver
from django.db.models.signals import post_save
from datetime import date
import datetime
from django.utils import timezone

# Create your models here.

class Centro(models.Model):
    id_centro=models.AutoField(primary_key=True, auto_created = True)
    nombre_centro=models.CharField(max_length=50,help_text="Ingrese el nombre del centro", null=False)
    propietaria=models.CharField(max_length=50,help_text="Ingrese el nombre de la/el propietari@")
    localizacion=models.CharField(max_length=100,help_text="Ingrese la hubicación del centro")
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
    autorizacion=models.BooleanField(default=False)
    protec_datos=models.BooleanField(default=False)
    centro=models.ForeignKey(Centro, on_delete=models.CASCADE)
    poblacion=models.CharField(max_length=50,help_text="Ingrese la población del/la paciente",  default='Valencia')
    direccion=models.CharField(max_length=50,help_text="Ingrese la dirección del/la paciente",  default='Valencia')
    history = HistoricalRecords()

    class Meta:
        verbose_name_plural = "Pacientes"

    def __str__(self):
        return self.nombre_paciente

class Tecnica(models.Model):
    id_tecnica=models.AutoField(primary_key=True, auto_created = True)
    imagen=models.ImageField(upload_to='images/', default='img/porfile.png')
    nombre_tecnica=models.CharField(max_length=50,help_text="Ingrese el nombre de la/el tecnic@")
    apellidos_tecnica=models.CharField(max_length=50,help_text="Ingrese los apellidos de la/el tecnic@")
    history = HistoricalRecords()
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Tecnicas | Tecnicos"

    def __str__(self):
        return self.nombre_tecnica

def create_user_profile(sender, instance, created, **kwargs):
    if created:
       profile, created = Tecnica.objects.get_or_create(user=instance)

post_save.connect(create_user_profile, sender=User)

class Cita(models.Model):
    id_cita=models.AutoField(primary_key=True, auto_created = True)
    tecnica=models.ForeignKey(Tecnica, on_delete=models.CASCADE, null=False)
    paciente=models.ForeignKey(Paciente, on_delete=models.CASCADE , null=False)
    fecha=models.DateTimeField(null=False)
    zona=models.CharField(max_length=50,help_text="Ingrese la zona tratada o por tratar" , null=False)
    comentario=models.TextField(help_text="Ingrese los comentarios sobre la cita")
    hertz=models.IntegerField(help_text="Ingrese la potencia en hertz", default=0 , null=False)
    milisegundos=models.IntegerField(help_text="Ingrese la potencia en milisegundos",  default=0, null=False)
    julios=models.IntegerField( help_text="Ingrese la potencia en julios",  default=0, null=False)
    history = HistoricalRecords()


    class Meta:
        verbose_name_plural = "Citas"

    def __str__(self):
        return f"Cita : {self.fecha}"

class ControlHorario(models.Model):
    tecnica=models.ForeignKey(Tecnica, on_delete=models.CASCADE,auto_created = True, default="lima")
    fecha=models.DateField()
    entrada=models.TimeField()
    salida=models.TimeField(default=None, blank=True, null=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name_plural = "Control Horario"

    def __str__(self):
        return f"Fichages : {self.fecha}"
