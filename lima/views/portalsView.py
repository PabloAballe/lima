
# Create your views here.
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth import logout as do_logout
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as do_login
from ..models import *
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ..forms import *
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
from ..filters import *
import os
import webbrowser as web
from twilio.rest import Client
#mailchimp
from django.conf import settings
from mailchimp_marketing.api_client import ApiClientError
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


@login_required(login_url='login')
def portales(request):
    # Subscription Logic
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    paneles=Paneles.objects.all().order_by('nombre_panel').filter(portales__id_tecnica=request.user.tecnica.id_tecnica)
    return render(request, "portals/portales.html", {'footer': footer,'paneles':paneles})

@login_required(login_url='login')
def portales_details(request,pk):
    # Subscription Logic
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    panel=get_object_or_404(Paneles, pk=pk)
    estados=Estados.objects.all().order_by('orden_del_estado').filter(panel=panel)
    return render(request, "portals/portal_details.html", {'footer': footer,'panel':panel, 'estados': estados})

@login_required(login_url='login')
def estados(request):
    # Subscription Logic
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    paneles=Paneles.objects.all().order_by('nombre_panel').filter(portales__id_tecnica=request.user.tecnica.id_tecnica)
    return render(request, "portals/portales.html", {'footer': footer,'paneles':paneles})

@login_required(login_url='login')
def tarea_details(request, pk):
    # Subscription Logic
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    mensajes=Mensajes.objects.filter(tarea=pk)
    tarea=get_object_or_404(Tareas, id_tarea=pk)
    form=TareaForm(instance=tarea)
    formMensaje=MensajeForm()
    if request.method == 'POST':
        form = TareaForm(request.POST, instance=tarea)
        formMensaje=MensajeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,f'Se ha guardado la tarea')
            return redirect("tarea_details", pk=tarea.id_tarea)
        else:
            form = TareaForm()
        if formMensaje.is_valid():
            mensaje = formMensaje.save(commit=False)
            mensaje.enviado_por=request.user.tecnica
            mensaje.tarea=tarea
            formMensaje.save()
            messages.success(request,f'Se ha guardado el mensaje')
            return redirect("tarea_details", pk=tarea.id_tarea)
        else:
            formMensaje = MensajeForm()
    return render(request, "portals/tarea_details.html", {'footer': footer,'mensajes':mensajes, 'tarea': tarea,'form': form,'formMensaje': formMensaje})

@login_required(login_url='login')
def new_tarea(request, pk):
    # Subscription Logic
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    form=TareaForm()
    portal=get_object_or_404(Paneles, pk=pk)
    if request.method == 'POST':
        form = TareaForm(request.POST)
        if form.is_valid():
            tarea = form.save(commit=False)
            tarea.portal=portal
            form.save()
            messages.success(request,f'Se ha guardado la tarea')
            return redirect("portales_details", pk=portal.id_panel)
        else:
            form = TareaForm()
    return render(request, "portals/new_tarea.html", {'footer': footer,'form': form})


