# Generated by Django 3.1.3 on 2021-09-27 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lima', '0062_auto_20210927_2109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configuracion',
            name='politica',
            field=models.TextField(blank=True, help_text='Ingrese la política  de la empresa que aparecera en la parte inferior de los textos'),
        ),
        migrations.AlterField(
            model_name='configuracion',
            name='twilio_ACCOUNT_SID',
            field=models.CharField(blank=True, default='', help_text='Ingrese la ACCOUNT SID de Twilio', max_length=500),
        ),
        migrations.AlterField(
            model_name='configuracion',
            name='twilio_AUTH_TOKEN',
            field=models.CharField(blank=True, default='', help_text='Ingrese el AUTH TOKEN de Twilio', max_length=500),
        ),
        migrations.AlterField(
            model_name='configuracion',
            name='twilio_SENDGRID_API_KEY',
            field=models.CharField(blank=True, default='', help_text='Ingrese la SENDGRID API KEY de Twilio', max_length=500),
        ),
        migrations.AlterField(
            model_name='historicalconfiguracion',
            name='politica',
            field=models.TextField(blank=True, help_text='Ingrese la política  de la empresa que aparecera en la parte inferior de los textos'),
        ),
        migrations.AlterField(
            model_name='historicalconfiguracion',
            name='twilio_ACCOUNT_SID',
            field=models.CharField(blank=True, default='', help_text='Ingrese la ACCOUNT SID de Twilio', max_length=500),
        ),
        migrations.AlterField(
            model_name='historicalconfiguracion',
            name='twilio_AUTH_TOKEN',
            field=models.CharField(blank=True, default='', help_text='Ingrese el AUTH TOKEN de Twilio', max_length=500),
        ),
        migrations.AlterField(
            model_name='historicalconfiguracion',
            name='twilio_SENDGRID_API_KEY',
            field=models.CharField(blank=True, default='', help_text='Ingrese la SENDGRID API KEY de Twilio', max_length=500),
        ),
    ]
