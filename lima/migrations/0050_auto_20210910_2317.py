# Generated by Django 3.1.3 on 2021-09-10 23:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lima', '0049_auto_20210910_2308'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuracion',
            name='enviar_email_nuevas_listas',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='configuracion',
            name='plantilla_lista',
            field=models.ForeignKey(blank=True, default='1', on_delete=django.db.models.deletion.RESTRICT, related_name='plantilla_lista', to='lima.emailtemplates'),
        ),
        migrations.AddField(
            model_name='historicalconfiguracion',
            name='enviar_email_nuevas_listas',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='historicalconfiguracion',
            name='plantilla_lista',
            field=models.ForeignKey(blank=True, db_constraint=False, default='1', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='lima.emailtemplates'),
        ),
        migrations.AlterField(
            model_name='configuracion',
            name='plantilla_email',
            field=models.ForeignKey(blank=True, default='1', on_delete=django.db.models.deletion.RESTRICT, related_name='plantilla_email', to='lima.emailtemplates'),
        ),
    ]