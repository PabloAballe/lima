# Generated by Django 3.1.3 on 2021-10-11 00:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lima', '0080_auto_20211010_2310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turnos',
            name='turno_fin',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 11, 0, 5, 32, 929350)),
        ),
        migrations.AlterField(
            model_name='turnos',
            name='turno_inicio',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 11, 0, 5, 32, 929350)),
        ),
    ]
