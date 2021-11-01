# Generated by Django 3.1.3 on 2021-10-22 09:08

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('lima', '0100_auto_20211020_2318'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='docsings',
            name='icon',
        ),
        migrations.AddField(
            model_name='docsings',
            name='imagen',
            field=django_resized.forms.ResizedImageField(crop=None, default='', force_format='PNG', keep_meta=True, quality=75, size=[500, 500], upload_to='images/signatures'),
        ),
    ]
