
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
def perfil(request):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    user=request.user
    meses=ControlHorario.objects.filter(tecnica=user.tecnica).order_by("-fecha", "-entrada")
    #pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(meses, 10)
    try:
        cen = paginator.page(page)
    except PageNotAnInteger:
        cen = paginator.page(1)
    except EmptyPage:
        cen = paginator.page(paginator.num_pages)
    #checkea si ha enytrado o salido
    user=request.user
    horario=ControlHorario.objects.filter(tecnica=user.tecnica).last()
    salida=False
    if horario:
        if horario.salida is None:
            salida=True
    else:
        salida=False

    return render(request, 'perfil.html', {'meses': cen,'cen': cen, 'salida': salida, 'footer': footer })

@login_required(login_url='login')
def view_perfiles(request):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    tecnica= Tecnica.objects.all().order_by("-nombre_tecnica")
    notfound=False
    #shearch perfiles
    if request.method == "GET":
        form = SheachForm(request.GET)

    if form.is_valid():
        q= form.cleaned_data['shearch']
        existe=Tecnica.objects.all().order_by('nombre_tecnica').filter(nombre_tecnica__icontains=q).exists()
        if existe==True:
            tecnica=Tecnica.objects.all().order_by('nombre_tecnica').filter(nombre_tecnica__icontains=q)
        else:
            notfound=True
            print("no hay resultados")
    else:
        form = SheachForm()

    #pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(tecnica, 10)
    try:
        cen = paginator.page(page)
    except PageNotAnInteger:
        cen = paginator.page(1)
    except EmptyPage:
        cen = paginator.page(paginator.num_pages)
    return render(request, 'view_perfiles.html', { 'tecnica': cen , 'form': form, 'footer': footer, 'cen': cen,'notfound': notfound  })

@login_required(login_url='login')
def ver_horario(request, pk):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    salida=False
    #checkea si ha enytrado o salido
    tecnica=get_object_or_404(Tecnica, pk=pk)
    meses=ControlHorario.objects.filter(tecnica=tecnica).order_by("-fecha", "-entrada")[:90]
    horario=ControlHorario.objects.filter(tecnica=tecnica).last()
    if horario:
        if horario.salida is None:
            salida=True
    else:
        salida=False
    return render(request, 'perfil_horario.html', {'meses': meses, 'salida': salida, 'tecnica': tecnica, 'footer': footer })



@login_required(login_url='login')
def ver_horario_visual(request, pk):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    today = dt.datetime.now()
    salida=False
    #checkea si ha enytrado o salido
    tecnica=get_object_or_404(Tecnica, pk=pk)
    meses=ControlHorario.objects.filter(tecnica=tecnica).order_by("-fecha", "-entrada")
    horario=ControlHorario.objects.filter(tecnica=tecnica).last()
    if horario:
        if horario.salida is None:
            salida=True
    else:
        salida=False
    return render(request, 'calendar_horario.html', {'meses': meses, 'salida': salida, 'tecnica': tecnica , 'today': today, 'footer': footer})

@login_required(login_url='login')
def ver_visual_tecnica(request, pk):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    today = dt.datetime.now()
    salida=False
    tecnica=request.user.tecnica
    #checkea si ha enytrado o salido
    if pk !=0:
        tecnica=get_object_or_404(Tecnica, pk=pk)
        tecnicas=Tecnica.objects.filter(id_tecnica=pk)
        citas=Tratamientos.objects.filter(tecnica=tecnica).order_by("-fecha")
        meses = citas
        horario=ControlHorario.objects.filter(tecnica=tecnica).last()
    else:
        citas=Tratamientos.objects.all().order_by("-fecha")
        tecnicas=Tecnica.objects.all().filter(habilitado=True)
        meses = citas
        horario=ControlHorario.objects.filter(tecnica=request.user.tecnica).last()

    if horario:
        if horario.salida is None:
            salida=True
    else:
        salida=False
    return render(request, 'ver_visual_tecnica.html', {'meses': meses, 'salida': salida, 'tecnica': tecnica , 'today': today, 'footer': footer, 'tecnicas': tecnicas})


@login_required(login_url='login')
def edit_turno(request, pk):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    today = dt.datetime.now()
    salida=False
    if pk !=0:
        tecnica=get_object_or_404(Tecnica, pk=pk)
        meses=Turnos.objects.filter(tecnica=tecnica).order_by("-turno")
    else:
        tecnica =request.user.tecnica
        meses=Turnos.objects.all().order_by("-turno")

    horario=ControlHorario.objects.filter(tecnica=tecnica).last()
    if horario:
        if horario.salida is None:
            salida=True
    else:
        salida=False
    return render(request, 'edit_turno.html', {'meses': meses, 'salida': salida, 'tecnica': tecnica , 'today': today, 'footer': footer})



