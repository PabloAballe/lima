# Generated by Django 3.1.3 on 2021-06-30 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lima', '0004_auto_20210629_1754'),
    ]

    operations = [
        migrations.AddField(
            model_name='controlhorario',
            name='trabajado',
            field=models.TimeField(default='00:00'),
        ),
        migrations.AddField(
            model_name='historicalcontrolhorario',
            name='trabajado',
            field=models.TimeField(default='00:00'),
        ),
    ]
