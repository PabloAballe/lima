# Generated by Django 3.1.3 on 2021-09-10 22:52

from django.db import migrations, models
import django.utils.timezone
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('lima', '0044_auto_20210910_2236'),
    ]

    operations = [
        migrations.CreateModel(
            name='Anuncios',
            fields=[
                ('id_anuncio', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('cuerpo_anuncio', models.CharField(help_text='Ingrese el nombre del estado', max_length=30)),
                ('imagen', django_resized.forms.ResizedImageField(crop=None, force_format='PNG', keep_meta=True, quality=75, size=[500, 500], upload_to='images/')),
                ('fecha_creacion', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name_plural': 'Anúncios del sistema',
            },
        ),
    ]
