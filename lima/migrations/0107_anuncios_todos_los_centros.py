# Generated by Django 3.1.3 on 2021-10-25 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lima', '0106_auto_20211023_0010'),
    ]

    operations = [
        migrations.AddField(
            model_name='anuncios',
            name='todos_los_centros',
            field=models.BooleanField(default=False, help_text='Enviar anuncio a todos los centro'),
        ),
    ]