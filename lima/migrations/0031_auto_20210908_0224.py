# Generated by Django 3.1.3 on 2021-09-08 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lima', '0030_auto_20210908_0104'),
    ]

    operations = [
        migrations.RenameField(
            model_name='centro',
            old_name='horario_apertura_entre_semana',
            new_name='horario_apertura',
        ),
        migrations.RenameField(
            model_name='centro',
            old_name='horario_cierre_entre_semana',
            new_name='horario_cierre',
        ),
        migrations.RemoveField(
            model_name='centro',
            name='horario_apertura_fin_semana',
        ),
        migrations.RemoveField(
            model_name='centro',
            name='horario_cierre_fin_semana',
        ),
        migrations.RemoveField(
            model_name='historicalcentro',
            name='horario_apertura_entre_semana',
        ),
        migrations.RemoveField(
            model_name='historicalcentro',
            name='horario_apertura_fin_semana',
        ),
        migrations.RemoveField(
            model_name='historicalcentro',
            name='horario_cierre_entre_semana',
        ),
        migrations.RemoveField(
            model_name='historicalcentro',
            name='horario_cierre_fin_semana',
        ),
        migrations.RemoveField(
            model_name='tags',
            name='centro',
        ),
        migrations.AddField(
            model_name='historicalcentro',
            name='horario_apertura',
            field=models.TimeField(default='09:00:00', help_text='Ingrese la hora de apertura de la clínica entre semana'),
        ),
        migrations.AddField(
            model_name='historicalcentro',
            name='horario_cierre',
            field=models.TimeField(default='21:00:00', help_text='Ingrese la hora de cierre de la clínica entre semana'),
        ),
    ]