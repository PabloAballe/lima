# Generated by Django 3.1.3 on 2021-07-03 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lima', '0004_auto_20210703_0452'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='docsings',
            name='base64',
        ),
        migrations.AddField(
            model_name='docsings',
            name='firma_imagen',
            field=models.ImageField(default='', upload_to='firmas-images/'),
        ),
    ]
