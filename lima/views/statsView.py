
# Create your views here.
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth import logout as do_logout
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as do_login
from .models import *
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import *
from django.shortcuts import render, get_object_or_404
from itertools import chain
import datetime as dt
from django.utils import timezone, dateformat
from django.db.models import Sum
from django.db.models import Count
from django.core import serializers
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.core.mail import send_mail
from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.utils.safestring import SafeString
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.template import Context, Template
from jsignature.utils import draw_signature
import base64
from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image
import PIL
from django.conf import settings
from datetime import datetime
from django.template.loader import get_template
from django.contrib import messages
from .filters import *
import os
import webbrowser as web
from twilio.rest import Client
#mailchimp
from django.conf import settings
from mailchimp_marketing.api_client import ApiClientError
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

@login_required(login_url='login')
def estatisticas(request):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    clientes = Paciente.objects.raw('SELECT lima_paciente.id_paciente,COUNT(*) AS count, 	lima_paciente.fecha_alta as fecha_alta FROM 	lima_paciente WHERE 	YEAR(lima_paciente.fecha_alta)=YEAR(CURDATE()) GROUP BY WEEK(lima_paciente.fecha_alta)')
    tratamientos=Tratamientos.objects.raw('SELECT  lima_tratamientos.id_tratamiento, 	COUNT(*) AS count, 	lima_tratamientos.fecha as fecha FROM 	lima_tratamientos WHERE 	YEAR(lima_tratamientos.fecha)=YEAR(CURDATE()) GROUP BY WEEK(lima_tratamientos.fecha)')
    facturacion = Cajas.objects.raw('SELECT lima_cajas.id_caja, ROUND(SUM(cantidad_total),0) AS count, 	lima_cajas.fecha as fecha FROM 	lima_cajas WHERE 	YEAR(lima_cajas.fecha)=YEAR(CURDATE()) GROUP BY WEEK(lima_cajas.fecha)')
    citas = Lista.objects.raw('SELECT lima_lista.id_lista, COUNT(*) AS count, DATE(lima_lista.hora_inicio) FROM lima_lista WHERE YEAR(lima_lista.hora_inicio)=YEAR(CURDATE()) GROUP BY WEEK(lima_lista.hora_inicio)')
    tecnicas_horarios=ControlHorario.objects.raw(f'SELECT id, SUBSTRING_INDEX(CONCAT(SEC_TO_TIME(SUM(TIME_TO_SEC(trabajado)))), ":",1) AS count_tecnica, lima_tecnica.nombre_tecnica as nombre FROM lima_controlhorario INNER JOIN lima_tecnica ON lima_tecnica.id_tecnica=lima_controlhorario.tecnica_id WHERE MONTH(fecha)= MONTH(CURDATE()) AND YEAR(fecha)=YEAR(CURDATE())GROUP BY tecnica_id')
    #shearch form
    if request.user.is_staff:
        if request.method == "GET":
            form = EstadisticasAdminForm(request.GET)

            if form.is_valid():
                    fecha_inico= form.cleaned_data['fecha_inico']
                    fecha_fin= form.cleaned_data['fecha_fin']
                    centro= form.cleaned_data['centro']
                    tecnicas=form.cleaned_data['tecnicas']
                    clientes = Paciente.objects.raw(f'SELECT lima_paciente.id_paciente, COUNT(*) AS count, lima_paciente.fecha_alta FROM 	lima_paciente WHERE lima_paciente.fecha_alta BETWEEN  "{fecha_inico}" AND  "{fecha_fin}" AND centro_id = {centro.pk}  GROUP BY WEEK(lima_paciente.fecha_alta)')
                    tratamientos=Tratamientos.objects.raw(f'SELECT lima_tratamientos.id_tratamiento, COUNT(*) AS count, lima_tratamientos.fecha FROM 	lima_tratamientos WHERE lima_tratamientos.fecha BETWEEN  "{fecha_inico}" AND "{fecha_fin}" AND lima_tratamientos.tecnica_id = {tecnicas.pk} GROUP BY WEEK(lima_tratamientos.fecha)')
                    facturacion = Cajas.objects.raw(f'SELECT lima_cajas.id_caja, ROUND(SUM(cantidad_total),0) AS count, lima_cajas.fecha FROM 	lima_cajas WHERE lima_cajas.fecha BETWEEN "{fecha_inico}" AND "{fecha_fin}" AND centro_id = {centro.pk} AND tecnica_id = {tecnicas.pk} GROUP BY WEEK(lima_cajas.fecha)')
                    citas = Lista.objects.raw(f'SELECT lima_lista.id_lista, COUNT(*) AS count, DATE(lima_lista.hora_inicio) FROM lima_lista WHERE lima_lista.hora_inicio BETWEEN "{fecha_inico}" AND "{fecha_fin}" AND lima_lista.centro_id = {centro.pk} AND tecnica_id = {tecnicas.pk} GROUP BY WEEK(lima_lista.hora_inicio)')
                    tecnicas_horarios=ControlHorario.objects.raw(f'SELECT id, SUBSTRING_INDEX(CONCAT(SEC_TO_TIME(SUM(TIME_TO_SEC(trabajado)))), ":",1) AS count_tecnica, lima_tecnica.nombre_tecnica AS nombre FROM lima_controlhorario INNER JOIN lima_tecnica ON id_tecnica=lima_controlhorario.tecnica_id WHERE fecha  BETWEEN "{fecha_inico}" AND "{fecha_fin}"  AND tecnica_id = {tecnicas.pk} GROUP BY tecnica_id')
            else:
                form = EstadisticasAdminForm()
    else:
        if request.method == "GET":
            form = EstadisticasTecnicaForm(request.GET)

            if form.is_valid():
                    q= form.cleaned_data['shearch']
                    existe=Centro.objects.all().order_by('nombre_centro').filter(nombre_centro__icontains=q).filter(tecnica__id_tecnica=request.user.tecnica.id_tecnica).exists()
                    if existe==True:
                        centro=Centro.objects.all().order_by('nombre_centro').filter(nombre_centro__icontains=q).filter(tecnica__id_tecnica=request.user.tecnica.id_tecnica)
                    else:
                        notfound=True
                        print("no hay resultados")
            else:
                form = EstadisticasTecnicaForm()


    return render(request, 'estatisticas.html', {'footer': footer,'clientes': clientes, 'tratamientos': tratamientos,'facturacion': facturacion,'tecnicas_horarios':tecnicas_horarios,'form': form, 'citas': citas})

@login_required(login_url='login')
def estadisticas_horario_tecnica(request, pk=0):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    timeMonth=ControlHorario.objects.raw(f'SELECT id, CONCAT(SEC_TO_TIME( SUM(time_to_sec(trabajado))))  As count FROM lima_controlhorario WHERE tecnica_id ={pk} AND YEAR(fecha)=YEAR(CURDATE()) AND MONTH(fecha)=MONTH(CURDATE())   GROUP BY WEEK(fecha)')
    tiempo = ControlHorario.objects.raw(f'SELECT id, SUBSTRING_INDEX(CONCAT(SEC_TO_TIME(SUM(TIME_TO_SEC(trabajado)))), ":",1)  As count_time, fecha AS fecha FROM lima_controlhorario WHERE tecnica_id ={pk} AND YEAR(fecha)=YEAR(CURDATE())   GROUP BY WEEK(fecha)')
    if request.method == "GET":
            form = EstadisticasTecnicaForm(request.GET)

            if form.is_valid():
                    fecha_inico= form.cleaned_data['fecha_inico']
                    fecha_fin= form.cleaned_data['fecha_fin']
                    timeMonth=ControlHorario.objects.raw(f'SELECT id, CONCAT(SEC_TO_TIME( SUM(time_to_sec(trabajado))))  As count FROM lima_controlhorario WHERE tecnica_id ={pk} AND fecha BETWEEN "{fecha_inico}" AND "{fecha_fin}"    GROUP BY WEEK(fecha)')
                    tiempo = ControlHorario.objects.raw(f'SELECT id, SUBSTRING_INDEX(CONCAT(SEC_TO_TIME(SUM(TIME_TO_SEC(trabajado)))), ":",1)  As count_time, fecha AS fecha FROM lima_controlhorario WHERE tecnica_id ={pk} AND fecha BETWEEN "{fecha_inico}" AND "{fecha_fin}"   GROUP BY WEEK(fecha)')

            else:
                form = EstadisticasTecnicaForm()

    return render(request, 'estadistica_horario.html', {'footer': footer,'tiempo': tiempo,'timeMonth': timeMonth, 'form': form})