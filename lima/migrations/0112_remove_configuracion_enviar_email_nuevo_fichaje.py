# Generated by Django 3.1.3 on 2021-10-31 09:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lima', '0111_auto_20211027_0244'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='configuracion',
            name='enviar_email_nuevo_fichaje',
        ),
    ]
