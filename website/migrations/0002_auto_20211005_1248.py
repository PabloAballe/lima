# Generated by Django 3.1.3 on 2021-10-05 12:48

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='post',
            field=ckeditor.fields.RichTextField(),
        ),
    ]