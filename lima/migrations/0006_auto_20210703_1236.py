# Generated by Django 3.1.3 on 2021-07-03 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lima', '0005_auto_20210703_0550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='docsings',
            name='firma_imagen',
            field=models.CharField(help_text='Ingrese la url de la firma', max_length=100),
        ),
    ]
