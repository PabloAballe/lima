# Generated by Django 3.1.3 on 2021-11-29 23:39

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('lima', '0122_anuncios_activo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Origenes',
            fields=[
                ('id', models.AutoField(auto_created=True, editable=False, primary_key=True, serialize=False)),
                ('origen', models.CharField(help_text='Ingrese el nombre del servicio', max_length=100)),
                ('fecha_creacion', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name_plural': 'Origenes',
            },
        ),
        migrations.AddField(
            model_name='paciente',
            name='origen',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='lima.origenes'),
        ),
    ]
