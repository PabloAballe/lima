# Generated by Django 3.1.3 on 2021-10-07 02:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lima', '0070_auto_20211007_0156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turnos',
            name='turno_fin',
            field=models.DateTimeField(default=datetime.date(2015, 12, 1)),
        ),
        migrations.AlterField(
            model_name='turnos',
            name='turno_inicio',
            field=models.DateTimeField(default=datetime.date(2015, 12, 1)),
        ),
    ]
