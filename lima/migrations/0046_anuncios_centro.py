# Generated by Django 3.1.3 on 2021-09-10 22:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lima', '0045_anuncios'),
    ]

    operations = [
        migrations.AddField(
            model_name='anuncios',
            name='centro',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.RESTRICT, to='lima.centro'),
        ),
    ]