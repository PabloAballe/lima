# Generated by Django 3.1.3 on 2021-10-05 13:48

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_auto_20211005_1336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pages',
            name='cuerpo_pagina',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
