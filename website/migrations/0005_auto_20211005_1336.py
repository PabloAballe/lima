# Generated by Django 3.1.3 on 2021-10-05 13:36

from django.db import migrations
import django_editorjs.fields


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_auto_20211005_1318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pages',
            name='cuerpo_pagina',
            field=django_editorjs.fields.EditorJsField(),
        ),
    ]
