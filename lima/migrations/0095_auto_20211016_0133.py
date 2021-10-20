# Generated by Django 3.1.3 on 2021-10-16 01:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lima', '0094_auto_20211016_0123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anuncios',
            name='id_anuncio',
            field=models.AutoField(auto_created=True, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='cajas',
            name='id_caja',
            field=models.AutoField(auto_created=True, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='centro',
            name='id_centro',
            field=models.AutoField(auto_created=True, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='cita',
            name='id_cita',
            field=models.AutoField(auto_created=True, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='configuracion',
            name='id',
            field=models.AutoField(auto_created=True, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='controlhorario',
            name='tecnica',
            field=models.ForeignKey(auto_created=True, default='lima', editable=False, on_delete=django.db.models.deletion.RESTRICT, to='lima.tecnica'),
        ),
        migrations.AlterField(
            model_name='docsings',
            name='id',
            field=models.AutoField(auto_created=True, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='doctemplate',
            name='id',
            field=models.AutoField(auto_created=True, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='emailtemplates',
            name='id',
            field=models.AutoField(auto_created=True, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='estados',
            name='id_estado',
            field=models.AutoField(auto_created=True, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='estadosclientes',
            name='id_estado',
            field=models.AutoField(auto_created=True, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='imagenesclientes',
            name='id_image_cliente',
            field=models.AutoField(auto_created=True, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='lista',
            name='id_lista',
            field=models.AutoField(auto_created=True, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='mensajes',
            name='id_mensaje',
            field=models.AutoField(auto_created=True, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='id_paciente',
            field=models.AutoField(auto_created=True, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='paneles',
            name='id_panel',
            field=models.AutoField(auto_created=True, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='servicios',
            name='id_servicio',
            field=models.AutoField(auto_created=True, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='stock',
            name='id_stock',
            field=models.AutoField(auto_created=True, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='suscription',
            name='id_sicription',
            field=models.AutoField(auto_created=True, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='tags',
            name='id_tag',
            field=models.AutoField(auto_created=True, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='tareas',
            name='id_tarea',
            field=models.AutoField(auto_created=True, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='tecnica',
            name='id_tecnica',
            field=models.AutoField(auto_created=True, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='tratamientos',
            name='id_tratamiento',
            field=models.AutoField(auto_created=True, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='turnos',
            name='id_turno',
            field=models.AutoField(auto_created=True, editable=False, primary_key=True, serialize=False),
        ),
        migrations.DeleteModel(
            name='HistoricalPaciente',
        ),
    ]
