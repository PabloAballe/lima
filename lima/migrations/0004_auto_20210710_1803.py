# Generated by Django 3.1.3 on 2021-07-10 18:03

from django.db import migrations
import faicon.fields


class Migration(migrations.Migration):

    dependencies = [
        ('lima', '0003_auto_20210709_2336'),
    ]

    operations = [
        migrations.AddField(
            model_name='centro',
            name='icon',
            field=faicon.fields.FAIconField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='historicalcentro',
            name='icon',
            field=faicon.fields.FAIconField(default='', max_length=50),
        ),
    ]
