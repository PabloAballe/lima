# Generated by Django 3.1.3 on 2021-09-07 21:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lima', '0023_auto_20210907_2059'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalestadosclientes',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalpaneles',
            name='history_user',
        ),
        migrations.DeleteModel(
            name='HistoricalEstados',
        ),
        migrations.DeleteModel(
            name='HistoricalEstadosClientes',
        ),
        migrations.DeleteModel(
            name='HistoricalPaneles',
        ),
    ]
