# Generated by Django 3.1.3 on 2021-09-09 04:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lima', '0041_auto_20210908_0435'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicaltecnica',
            name='tema',
            field=models.CharField(choices=[('LG', 'light'), ('DK', 'dark'), ('RT', 'retro'), ('CP', 'cyberpunk'), ('VL', 'valentine'), ('GR', 'garden'), ('LF', 'lofi')], default='LG', max_length=2),
        ),
        migrations.AddField(
            model_name='tecnica',
            name='tema',
            field=models.CharField(choices=[('LG', 'light'), ('DK', 'dark'), ('RT', 'retro'), ('CP', 'cyberpunk'), ('VL', 'valentine'), ('GR', 'garden'), ('LF', 'lofi')], default='LG', max_length=2),
        ),
    ]