# Generated by Django 3.1.3 on 2021-11-10 17:51

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('lima', '0117_auto_20211108_2144'),
    ]

    operations = [
        # migrations.CreateModel(
        #     name='Origenes',
        #     fields=[
        #         ('id', models.AutoField(auto_created=True, editable=False, primary_key=True, serialize=False)),
        #         ('origen', models.CharField(help_text='Ingrese el nombre del servicio', max_length=100)),
        #         ('fecha_creacion', models.DateTimeField(default=django.utils.timezone.now)),
        #     ],
        #     options={
        #         'verbose_name_plural': 'Origenes',
        #     },
        # ),
        migrations.AlterField(
            model_name='paciente',
            name='estado',
            field=models.ForeignKey(blank=True, default='1', on_delete=django.db.models.deletion.RESTRICT, to='lima.estadosclientes'),
        ),
        # migrations.AddField(
        #     model_name='paciente',
        #     name='origen',
        #     field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='lima.origenes'),
        # ),
    ]
