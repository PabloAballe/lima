# Generated by Django 3.1.3 on 2021-09-08 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lima', '0040_estados_orden_del_estado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tags',
            name='tarea',
        ),
        migrations.AddField(
            model_name='tareas',
            name='etiquetas',
            field=models.ManyToManyField(blank=True, default='1', to='lima.Tags'),
        ),
    ]
