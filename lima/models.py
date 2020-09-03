from django.db import models
from django.utils import timezone

# Create your models here.

class Centro(models.Model):
    id_centro=models.AutoField(primary_key=True, auto_created = True)
    nombre_centro=models.CharField(max_length=50,help_text="Ingrese el nombre del centro")
    propietaria=models.CharField(max_length=50,help_text="Ingrese el nombre de la/el propietari@")
    localizacion=models.CharField(max_length=100,help_text="Ingrese la hubicación del centro")


    class Meta:
        verbose_name_plural = "Centros"

    def __str__(self):
        return self.nombre_centro

class Paciente(models.Model):
    id_paciente=models.AutoField(primary_key=True, auto_created = True)
    nombre_paciente=models.CharField(max_length=50,help_text="Ingrese el nombre de la/el paciente")
    apellidos_paciente=models.CharField(max_length=50,help_text="Ingrese los apellidos de la/el paciente")
    telefono_paciente=models.IntegerField(help_text="Ingrese el teléfono de la/el paciente")
    email=models.EmailField(help_text="Ingrese el correo electronico de la/el paciente")
    autorizacion=models.BooleanField(default=False)
    protec_datos=models.BooleanField(default=False)
    centro=models.ForeignKey(Centro, on_delete=models.CASCADE)
    poblacion=models.CharField(max_length=50,help_text="Ingrese la población del/la paciente",  default='Valencia')
    direccion=models.CharField(max_length=50,help_text="Ingrese la dirección del/la paciente",  default='Valencia')

    class Meta:
        verbose_name_plural = "Pacientes"

    def __str__(self):
        return self.nombre_paciente

class Tecnica(models.Model):
    id_tecnica=models.AutoField(primary_key=True, auto_created = True)
    nombre_tecnica=models.CharField(max_length=50,help_text="Ingrese el nombre de la/el tecnic@")
    apellidos_tecnica=models.CharField(max_length=50,help_text="Ingrese los apellidos de la/el tecnic@")

    class Meta:
        verbose_name_plural = "Tecnicas | Tecnicos"

    def __str__(self):
        return self.nombre_tecnica

class Potencia(models.Model):
    id_potencia=models.AutoField(primary_key=True, auto_created = True)
    hertz=models.IntegerField(help_text="Ingrese la potencia en hertz")
    milisegundos=models.IntegerField(help_text="Ingrese la potencia en milisegundos")
    julios=models.IntegerField( help_text="Ingrese la potencia en julios")

    class Meta:
        verbose_name_plural = "Potencias"

    def __str__(self):

        return f"Potencia : {self.id_potencia}"


class Cita(models.Model):
    id_cita=models.AutoField(primary_key=True, auto_created = True)
    tecnica=models.ForeignKey(Tecnica, on_delete=models.CASCADE)
    potencia=models.ForeignKey(Potencia, on_delete=models.CASCADE)
    paciente=models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fecha=models.DateTimeField()
    zona=models.CharField(max_length=50,help_text="Ingrese la zona tratada o por tratar")
    comentario=models.TextField(help_text="Ingrese los comentarios sobre la cita")


    class Meta:
        verbose_name_plural = "Citas"

    def __str__(self):
        return f"Cita : {self.fecha}"
