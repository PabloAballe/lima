# Generated by Django 3.1.3 on 2021-10-16 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0010_auto_20211008_0313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='id_post',
            field=models.AutoField(auto_created=True, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='conctact',
            name='id_contacto',
            field=models.AutoField(auto_created=True, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='configuracionweb',
            name='id_configuracion',
            field=models.AutoField(auto_created=True, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='pages',
            name='id_pagina',
            field=models.AutoField(auto_created=True, editable=False, primary_key=True, serialize=False),
        ),
    ]
