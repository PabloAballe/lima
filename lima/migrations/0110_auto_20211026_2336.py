# Generated by Django 3.1.3 on 2021-10-26 23:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lima', '0109_auto_20211025_1048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='docsings',
            name='plantilla_doc',
            field=models.TextField(help_text='Configure su plantilla'),
        ),
    ]
