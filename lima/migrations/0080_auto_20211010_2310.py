# Generated by Django 3.1.3 on 2021-10-10 23:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lima', '0079_auto_20211008_0335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turnos',
            name='turno_fin',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 10, 23, 10, 38, 198768)),
        ),
        migrations.AlterField(
            model_name='turnos',
            name='turno_inicio',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 10, 23, 10, 38, 198768)),
        ),
    ]