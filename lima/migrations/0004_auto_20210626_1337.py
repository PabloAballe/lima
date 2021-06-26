# Generated by Django 3.1.3 on 2021-06-26 11:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lima', '0003_auto_20201212_1330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cita',
            name='paciente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='lima.paciente'),
        ),
        migrations.AlterField(
            model_name='cita',
            name='tecnica',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='lima.tecnica'),
        ),
        migrations.AlterField(
            model_name='controlhorario',
            name='tecnica',
            field=models.ForeignKey(auto_created=True, default='lima', on_delete=django.db.models.deletion.RESTRICT, to='lima.tecnica'),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='centro',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='lima.centro'),
        ),
        migrations.AlterField(
            model_name='tecnica',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL),
        ),
    ]