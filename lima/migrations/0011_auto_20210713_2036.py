# Generated by Django 3.1.3 on 2021-07-13 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lima', '0010_auto_20210713_2033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalpaciente',
            name='apellidos_paciente',
            field=models.CharField(blank=True, default='', help_text='Ingrese los apellidos de la/el paciente', max_length=50),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='apellidos_paciente',
            field=models.CharField(blank=True, default='', help_text='Ingrese los apellidos de la/el paciente', max_length=50),
        ),
    ]
