# Generated by Django 3.1.3 on 2021-07-13 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lima', '0009_auto_20210713_2019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalpaciente',
            name='email',
            field=models.EmailField(blank=True, default='', help_text='Ingrese el correo electronico de la/el paciente', max_length=254),
        ),
        migrations.AlterField(
            model_name='historicalpaciente',
            name='telefono_paciente',
            field=models.IntegerField(blank=True, default='', help_text='Ingrese el teléfono de la/el paciente'),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='email',
            field=models.EmailField(blank=True, default='', help_text='Ingrese el correo electronico de la/el paciente', max_length=254),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='telefono_paciente',
            field=models.IntegerField(blank=True, default='', help_text='Ingrese el teléfono de la/el paciente'),
        ),
        migrations.AlterField(
            model_name='tratamientos',
            name='comentario',
            field=models.CharField(blank=True, default='', help_text='Ingrese el comentario del tratamiento', max_length=100),
        ),
    ]