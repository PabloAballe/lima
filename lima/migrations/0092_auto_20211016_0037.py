# Generated by Django 3.1.3 on 2021-10-16 00:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lima', '0091_auto_20211014_0039'),
    ]

    operations = [
        # migrations.AlterField(
        #     model_name='historicalpaciente',
        #     name='email',
        #     field=models.EmailField(blank=True, db_index=True, default='', help_text='Ingrese el correo electronico de la/el paciente', max_length=254),
        # ),
        # migrations.AlterField(
        #     model_name='historicalpaciente',
        #     name='telefono_paciente',
        #     field=models.CharField(blank=True, db_index=True, default=0, help_text='Ingrese el teléfono de la/el paciente', max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')]),
        # ),
        # migrations.AlterField(
        #     model_name='paciente',
        #     name='email',
        #     field=models.EmailField(blank=True, default='', help_text='Ingrese el correo electronico de la/el paciente', max_length=254, unique=True),
        # ),
        # migrations.AlterField(
        #     model_name='paciente',
        #     name='telefono_paciente',
        #     field=models.CharField(blank=True, default=0, help_text='Ingrese el teléfono de la/el paciente', max_length=17, unique=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')]),
        # ),
    ]
