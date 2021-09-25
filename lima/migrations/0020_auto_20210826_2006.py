# Generated by Django 3.1.3 on 2021-08-26 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lima', '0019_auto_20210826_1935'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuracion',
            name='mailchimp_api_key',
            field=models.CharField(blank=True, default='', help_text='Ingrese el nombre las credenciales de MailChimp', max_length=100),
        ),
        migrations.AddField(
            model_name='configuracion',
            name='mailchimp_list_id',
            field=models.CharField(blank=True, default='', help_text='Ingrese el nombre las credenciales de MailChimp', max_length=100),
        ),
        migrations.AddField(
            model_name='configuracion',
            name='mailchimp_server',
            field=models.CharField(blank=True, default='', help_text='Ingrese el nombre las credenciales de MailChimp', max_length=100),
        ),
        migrations.AddField(
            model_name='historicalconfiguracion',
            name='mailchimp_api_key',
            field=models.CharField(blank=True, default='', help_text='Ingrese el nombre las credenciales de MailChimp', max_length=100),
        ),
        migrations.AddField(
            model_name='historicalconfiguracion',
            name='mailchimp_list_id',
            field=models.CharField(blank=True, default='', help_text='Ingrese el nombre las credenciales de MailChimp', max_length=100),
        ),
        migrations.AddField(
            model_name='historicalconfiguracion',
            name='mailchimp_server',
            field=models.CharField(blank=True, default='', help_text='Ingrese el nombre las credenciales de MailChimp', max_length=100),
        ),
    ]