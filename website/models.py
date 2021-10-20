from django.db import models
from tinymce import models as tinymce_models
from django.template.defaultfilters import slugify
from colorfield.fields import ColorField
from django_resized import ResizedImageField
from django.core.validators import RegexValidator
from django.utils.timezone import now
from ckeditor.fields import RichTextField
from django_editorjs import EditorJsField

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="El teléfono debe de terner el formato: '+999999999'. Están permitidos hasta 15 dígitos.")

class Blog(models.Model):
    id_post=models.AutoField(primary_key=True, auto_created = True,editable = False)
    imagen=ResizedImageField(size=[500, 500],upload_to='images/website/', default='logo.png')
    titulo=models.CharField(max_length=50,help_text="Ingrese el título del post")
    post=models.TextField()
    autor=models.CharField(max_length=50,help_text="Ingrese el nombre de la/el autor")
    creado_el=models.DateTimeField(null=False, default=now)
    slug_post=models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name_plural = "Blog de la web"

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):
       self.slug_post = slugify(self.titulo)
       super(Blog, self).save(*args, **kwargs)

OPCIONES_PAGINAS = (
    ('I', 'INDEX'),
    ('A', 'CITAS'),
    ('C', 'CONTACTO'),
    ('B', 'BLOG'),
    ('O', 'OTRO')  # hay que ser inclusivos
)

class Pages(models.Model):
    id_pagina=models.AutoField(primary_key=True, auto_created = True,editable = False)
    nombre_pagina=models.CharField(max_length=50,help_text="Ingrese el nombre de la página")
    cuerpo_pagina=models.TextField()
    slug_pagina=models.CharField(max_length=200, blank=True)
    creado_el=models.DateTimeField(null=False, default=now)
    pertenece_a=models.CharField(max_length=1, choices=OPCIONES_PAGINAS, help_text="Ingrese a que catergoria pertecene está página", default="O")

    class Meta:
        verbose_name_plural = "Páginas de la web"

    def __str__(self):
        return self.nombre_pagina

    def save(self, *args, **kwargs):
        self.slug_pagina = slugify(self.nombre_pagina)
        super(Pages, self).save(*args, **kwargs)

class Conctact(models.Model):
    id_contacto=models.AutoField(primary_key=True, auto_created = True,editable = False)
    nombre_contacto=models.CharField(max_length=50,help_text="Ingrese el nombre de la página")
    telefono_contacto=models.CharField(max_length=50,help_text="Ingrese su nombre", default="",validators=[phone_regex] )
    email_contacto=models.EmailField(help_text="Ingrese su correo de contacto", blank=True, default="")
    mensaje_contacto=models.TextField(help_text="Deje su mensaje aquí")
    creado_el=models.DateTimeField(null=False, default=now)

    class Meta:
        verbose_name_plural = "Contactos mediante la web/app"

    def __str__(self):
        return self.nombre_contacto



class ConfiguracionWEB(models.Model):
    id_configuracion=models.AutoField(primary_key=True, auto_created = True,editable = False)
    nombre_web_app=models.CharField(max_length=50,help_text="Ingrese el nombre de la web/app")
    logo_web_app=ResizedImageField(size=[500, 500],upload_to='images/website/', default='logo.png')
    localizacion=models.CharField(max_length=50,help_text="Ingrese la localización de su negocio")
    email_nuevos_contactos=models.EmailField(help_text="Ingrese el correo donde recibir los nuevos contactos", blank=True, default="")
    descripcion_web_app=models.TextField(help_text="Ingrese la descripción de la web / app para SEO")
    politica_privacidad=models.TextField(help_text="Ingrese la política de privacidad de su sitio")
    color_primario=ColorField(default='#FF0000',help_text="Color primario de la web")
    color_secundario=ColorField(default='#FF0000',help_text="Color secundario de la web")

    class Meta:
        verbose_name_plural = "Configuración de la web/app"

    def __str__(self):
        return self.nombre_web_app


