# Generated by Django 3.1.3 on 2021-09-25 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lima', '0051_auto_20210925_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='estado',
            field=models.ManyToManyField(blank=True, default='01', to='lima.EstadosClientes'),
        ),
    ]
