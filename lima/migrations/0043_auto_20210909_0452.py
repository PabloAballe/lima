# Generated by Django 3.1.3 on 2021-09-09 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lima', '0042_auto_20210909_0434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicaltecnica',
            name='tema',
            field=models.CharField(choices=[('light', 'light'), ('dark', 'dark'), ('retro', 'retro'), ('cyberpunk', 'cyberpunk'), ('valentine', 'valentine'), ('garden', 'garden'), ('lofi', 'lofi')], default='light', max_length=20),
        ),
        migrations.AlterField(
            model_name='tecnica',
            name='tema',
            field=models.CharField(choices=[('light', 'light'), ('dark', 'dark'), ('retro', 'retro'), ('cyberpunk', 'cyberpunk'), ('valentine', 'valentine'), ('garden', 'garden'), ('lofi', 'lofi')], default='light', max_length=20),
        ),
    ]
