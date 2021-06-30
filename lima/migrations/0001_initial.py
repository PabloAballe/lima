# Generated by Django 3.1.3 on 2021-06-29 17:21

import colorfield.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Centro',
            fields=[
                ('id_centro', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('nombre_centro', models.CharField(help_text='Ingrese el nombre del centro', max_length=50)),
                ('propietaria', models.CharField(help_text='Ingrese el nombre de la/el propietari@', max_length=50)),
                ('localizacion', models.CharField(help_text='Ingrese la hubicación del centro', max_length=100)),
                ('habilitado', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'Centros',
            },
        ),
        migrations.CreateModel(
            name='EmailTemplates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('nombre', models.CharField(help_text='Ingrese el nombre de la plantilla', max_length=100)),
                ('plantilla', models.TextField(help_text='Confifure su plantilla')),
            ],
            options={
                'verbose_name_plural': 'Plantillas de email',
            },
        ),
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id_paciente', models.AutoField(auto_created=True, default=1, primary_key=True, serialize=False)),
                ('nombre_paciente', models.CharField(help_text='Ingrese el nombre de la/el paciente', max_length=50)),
                ('apellidos_paciente', models.CharField(help_text='Ingrese los apellidos de la/el paciente', max_length=50)),
                ('telefono_paciente', models.IntegerField(help_text='Ingrese el teléfono de la/el paciente')),
                ('email', models.EmailField(help_text='Ingrese el correo electronico de la/el paciente', max_length=254)),
                ('dni', models.CharField(default='', help_text='Ingrese el DNI del cliente', max_length=50)),
                ('autorizacion', models.BooleanField(default=False)),
                ('protec_datos', models.BooleanField(default=False)),
                ('poblacion', models.CharField(default='Valencia', help_text='Ingrese la población del/la paciente', max_length=50)),
                ('direccion', models.CharField(default='Valencia', help_text='Ingrese la dirección del/la paciente', max_length=50)),
                ('centro', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='lima.centro')),
            ],
            options={
                'verbose_name_plural': 'Clientes',
            },
        ),
        migrations.CreateModel(
            name='Tecnica',
            fields=[
                ('id_tecnica', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('imagen', models.ImageField(default='img/porfile.png', upload_to='images/')),
                ('nombre_tecnica', models.CharField(help_text='Ingrese el nombre de la/el tecnic@', max_length=50)),
                ('apellidos_tecnica', models.CharField(help_text='Ingrese los apellidos de la/el técnic@', max_length=50)),
                ('color', colorfield.fields.ColorField(default='#FF0000', max_length=18)),
                ('habilitado', models.BooleanField(default=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Técnicas | Técnicos',
            },
        ),
        migrations.CreateModel(
            name='Turnos',
            fields=[
                ('id_turno', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('turno', models.DateTimeField()),
                ('centro', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='lima.centro')),
                ('tecnica', models.ForeignKey(auto_created=True, default='lima', on_delete=django.db.models.deletion.RESTRICT, to='lima.tecnica')),
            ],
            options={
                'verbose_name_plural': 'Turnos de trabajo',
            },
        ),
        migrations.CreateModel(
            name='Tratamientos',
            fields=[
                ('id_tratamiento', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('fecha', models.DateField()),
                ('js', models.CharField(help_text='Ingrese los J/S', max_length=100)),
                ('jl', models.CharField(help_text='Ingrese los J/L', max_length=100)),
                ('comentario', models.CharField(help_text='Ingrese el comentario del tratamiento', max_length=100)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='lima.paciente')),
                ('tecnica', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='lima.tecnica')),
            ],
            options={
                'verbose_name_plural': 'Tratamientos agendados',
            },
        ),
        migrations.CreateModel(
            name='HistoricalTurnos',
            fields=[
                ('id_turno', models.IntegerField(auto_created=True, blank=True, db_index=True)),
                ('turno', models.DateTimeField()),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('centro', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='lima.centro')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('tecnica', models.ForeignKey(auto_created=True, blank=True, db_constraint=False, default='lima', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='lima.tecnica')),
            ],
            options={
                'verbose_name': 'historical turnos',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalTecnica',
            fields=[
                ('id_tecnica', models.IntegerField(auto_created=True, blank=True, db_index=True)),
                ('imagen', models.TextField(default='img/porfile.png', max_length=100)),
                ('nombre_tecnica', models.CharField(help_text='Ingrese el nombre de la/el tecnic@', max_length=50)),
                ('apellidos_tecnica', models.CharField(help_text='Ingrese los apellidos de la/el técnic@', max_length=50)),
                ('color', colorfield.fields.ColorField(default='#FF0000', max_length=18)),
                ('habilitado', models.BooleanField(default=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical tecnica',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalPaciente',
            fields=[
                ('id_paciente', models.IntegerField(auto_created=True, blank=True, db_index=True, default=1)),
                ('nombre_paciente', models.CharField(help_text='Ingrese el nombre de la/el paciente', max_length=50)),
                ('apellidos_paciente', models.CharField(help_text='Ingrese los apellidos de la/el paciente', max_length=50)),
                ('telefono_paciente', models.IntegerField(help_text='Ingrese el teléfono de la/el paciente')),
                ('email', models.EmailField(help_text='Ingrese el correo electronico de la/el paciente', max_length=254)),
                ('dni', models.CharField(default='', help_text='Ingrese el DNI del cliente', max_length=50)),
                ('autorizacion', models.BooleanField(default=False)),
                ('protec_datos', models.BooleanField(default=False)),
                ('poblacion', models.CharField(default='Valencia', help_text='Ingrese la población del/la paciente', max_length=50)),
                ('direccion', models.CharField(default='Valencia', help_text='Ingrese la dirección del/la paciente', max_length=50)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('centro', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='lima.centro')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical paciente',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalEmailTemplates',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True)),
                ('nombre', models.CharField(help_text='Ingrese el nombre de la plantilla', max_length=100)),
                ('plantilla', models.TextField(help_text='Confifure su plantilla')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical email templates',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalControlHorario',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('entrada', models.TimeField()),
                ('salida', models.TimeField(blank=True, default=None, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('tecnica', models.ForeignKey(auto_created=True, blank=True, db_constraint=False, default='lima', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='lima.tecnica')),
            ],
            options={
                'verbose_name': 'historical control horario',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalConfiguracion',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True)),
                ('nombre_comercial', models.CharField(help_text='Ingrese el nombre comercial del negocio', max_length=100)),
                ('propietario', models.CharField(help_text='Ingrese el nombre del propietario del negocio', max_length=100)),
                ('logo', models.TextField(default='img/login.png', max_length=100)),
                ('politica', models.TextField(help_text='Ingrese la política  de la empresa que aparecera en la parte inferior de los textos')),
                ('email_nuevos_clientes', models.BooleanField(default=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('cliente', models.ForeignKey(blank=True, db_constraint=False, default='1', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='lima.emailtemplates')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical configuracion',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalCita',
            fields=[
                ('id_cita', models.IntegerField(auto_created=True, blank=True, db_index=True)),
                ('fecha', models.DateTimeField()),
                ('zona', models.CharField(help_text='Ingrese la zona tratada o por tratar', max_length=50)),
                ('hertz', models.IntegerField(default=0, help_text='Ingrese la potencia en hertz')),
                ('milisegundos', models.IntegerField(default=0, help_text='Ingrese la potencia en milisegundos')),
                ('julios', models.IntegerField(default=0, help_text='Ingrese la potencia en julios')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('paciente', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='lima.paciente')),
                ('tecnica', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='lima.tecnica')),
            ],
            options={
                'verbose_name': 'historical cita',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalCentro',
            fields=[
                ('id_centro', models.IntegerField(auto_created=True, blank=True, db_index=True)),
                ('nombre_centro', models.CharField(help_text='Ingrese el nombre del centro', max_length=50)),
                ('propietaria', models.CharField(help_text='Ingrese el nombre de la/el propietari@', max_length=50)),
                ('localizacion', models.CharField(help_text='Ingrese la hubicación del centro', max_length=100)),
                ('habilitado', models.BooleanField(default=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical centro',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='ControlHorario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('entrada', models.TimeField()),
                ('salida', models.TimeField(blank=True, default=None, null=True)),
                ('tecnica', models.ForeignKey(auto_created=True, default='lima', on_delete=django.db.models.deletion.RESTRICT, to='lima.tecnica')),
            ],
            options={
                'verbose_name_plural': 'Control Horario',
            },
        ),
        migrations.CreateModel(
            name='Configuracion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('nombre_comercial', models.CharField(help_text='Ingrese el nombre comercial del negocio', max_length=100)),
                ('propietario', models.CharField(help_text='Ingrese el nombre del propietario del negocio', max_length=100)),
                ('logo', models.ImageField(default='img/login.png', upload_to='images/')),
                ('politica', models.TextField(help_text='Ingrese la política  de la empresa que aparecera en la parte inferior de los textos')),
                ('email_nuevos_clientes', models.BooleanField(default=True)),
                ('cliente', models.ForeignKey(blank=True, default='1', on_delete=django.db.models.deletion.RESTRICT, to='lima.emailtemplates')),
            ],
            options={
                'verbose_name_plural': 'Configuración del sistema',
            },
        ),
        migrations.CreateModel(
            name='Cita',
            fields=[
                ('id_cita', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('fecha', models.DateTimeField()),
                ('zona', models.CharField(help_text='Ingrese la zona tratada o por tratar', max_length=50)),
                ('hertz', models.IntegerField(default=0, help_text='Ingrese la potencia en hertz')),
                ('milisegundos', models.IntegerField(default=0, help_text='Ingrese la potencia en milisegundos')),
                ('julios', models.IntegerField(default=0, help_text='Ingrese la potencia en julios')),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='lima.paciente')),
                ('tecnica', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='lima.tecnica')),
            ],
            options={
                'verbose_name_plural': 'Zonas',
            },
        ),
    ]
