# Generated by Django 3.1.3 on 2021-09-26 18:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lima', '0060_auto_20210926_1829'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalpaciente',
            name='telefono_paciente',
            field=models.CharField(blank=True, default=0, help_text='Ingrese el teléfono de la/el paciente', max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')]),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='telefono_paciente',
            field=models.CharField(blank=True, default=0, help_text='Ingrese el teléfono de la/el paciente', max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')]),
        ),
    ]
