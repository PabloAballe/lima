# Generated by Django 3.1.3 on 2021-11-11 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lima', '0121_auto_20211111_0112'),
    ]

    operations = [
        migrations.AddField(
            model_name='anuncios',
            name='activo',
            field=models.BooleanField(default=True, help_text='Determina si el auncio está activo'),
        ),
    ]