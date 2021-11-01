# Generated by Django 3.1.3 on 2021-10-22 17:33

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('lima', '0102_auto_20211022_1032'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctemplate',
            name='icon',
        ),
        migrations.RemoveField(
            model_name='emailtemplates',
            name='icon',
        ),
        migrations.AlterField(
            model_name='docsings',
            name='firma',
            field=django_resized.forms.ResizedImageField(crop=None, default='', force_format='PNG', keep_meta=True, quality=75, size=[500, 500], upload_to='images/signatures/'),
        ),
    ]
