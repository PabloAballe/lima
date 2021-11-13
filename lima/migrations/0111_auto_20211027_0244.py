# Generated by Django 3.1.3 on 2021-10-27 02:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lima', '0110_auto_20211026_2336'),
    ]

    operations = [
        migrations.AddField(
            model_name='docsings',
            name='plantilla_document',
            field=models.TextField(default='', help_text='Configure su plantilla'),
        ),
        migrations.AlterField(
            model_name='docsings',
            name='plantilla_doc',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='lima.doctemplate'),
        ),
    ]