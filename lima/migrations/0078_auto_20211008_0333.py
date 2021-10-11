# Generated by Django 3.1.3 on 2021-10-08 03:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lima', '0077_auto_20211008_0332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tareas',
            name='descripcion_tarea',
            field=models.CharField(blank=True, default='', help_text='Ingrese la descripción de la tarea', max_length=10000),
        ),
        migrations.AlterField(
            model_name='turnos',
            name='turno_fin',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 8, 3, 33, 16, 425021)),
        ),
        migrations.AlterField(
            model_name='turnos',
            name='turno_inicio',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 8, 3, 33, 16, 425021)),
        ),
    ]
