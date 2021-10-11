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

# Create your models here.
class HelpClases(models.Model):
    id=models.AutoField(primary_key=True, auto_created = True)
    nombre_catogoria=models.CharField(max_length=100,help_text="Ingrese el nombre de la catergoria" )
    creada_el=models.DateTimeField(null=False, auto_now_add=True,)
    icon= FAIconField(default="", blank=True)

    class Meta:
        verbose_name_plural = "Categorias de ayuda del sistema"

    def __str__(self):
        return f"Categoria : {self.nombre_catogoria}"


class HelpPost(models.Model):
    id_post=models.AutoField(primary_key=True, auto_created = True)
    imagen=ResizedImageField(size=[500, 500],upload_to='images/website/', default='logo.png')
    titulo=models.CharField(max_length=50,help_text="Ingrese el título del post")
    categoria=models.ForeignKey(HelpClases, on_delete=models.RESTRICT, null=False, default="1")
    post=models.TextField()
    autor=models.CharField(max_length=50,help_text="Ingrese el nombre de la/el autor")
    creado_el=models.DateTimeField(null=False, default=now)
    slug_post=models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name_plural = "Ayuda del sistema"

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):
       self.slug_post = slugify(self.titulo)
       super(Blog, self).save(*args, **kwargs)