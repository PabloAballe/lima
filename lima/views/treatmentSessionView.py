
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
def new_cita(request, pk):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    cliente1=get_object_or_404(Paciente, id_paciente=pk)
    if request.user.is_staff:
         form=CitaFormAdmin()
         if request.method == 'POST':
             form = CitaFormAdmin(request.POST)
             if form.is_valid():
                 cita = form.save(commit=False)
                 cita.paciente=cliente1
                 form.save()
                 messages.success(request,f'Se ha guardado la cita del cliente {cita.paciente.nombre_paciente}')
                 return redirect("cliente_details_zonas", pk=cliente1.id_paciente)
             else:
                 messages.error(request,f'Ha sucedido el siguiente error {form.errors }')
                 form = CitaFormAdmin()
    else:
         form=CitaForm()
         if request.method == 'POST':
             form = CitaForm(request.POST)
             if form.is_valid():
                 cita = form.save(commit=False)
                 cita.paciente=cliente1
                 cita.tecnica=request.user.tecnica
                 form.save()
                 messages.success(request,f'Se ha creado el cliente {cita.paciente.nombre_paciente}')
                 return redirect("cliente_details_zonas", pk=cliente1.id_paciente)
             else:
                #messages.error(request,f'Ha sucedido el siguiennte error {form.errors }')
                form = CitaForm()

    return render(request, "new_cita.html", {'form': form, 'footer': footer})

@login_required(login_url='login')
def edit_cita(request, pk):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    cita=get_object_or_404(Cita, pk=pk)
    if request.user.is_staff:
         form=CitaFormAdmin()
         if request.method == 'POST':
             form = CitaFormAdmin(request.POST, instance=post)
             if form.is_valid():
                 cita = form.save(commit=False)
                 cita.paciente=cliente1
                 form.save()
                 messages.success(request,f'Se ha guardado la cita')
                 return redirect("cliente_details_zonas", pk=cliente1.id_paciente)
             else:
                 #messages.error(request,f'Ha sucedido el siguiente error {form.errors }')
                 form = CitaFormAdmin()
    else:
         form=CitaForm()
         if request.method == 'POST':
             form = CitaForm(request.POST, instance=post)
             if form.is_valid():
                 cita = form.save(commit=False)
                 cita.paciente=cliente1
                 cita.tecnica=request.user.tecnica
                 form.save()
                 messages.success(request,f'Se ha guardado la cita')
                 return redirect("cliente_details_zonas", pk=cliente1.id_paciente)
             else:
                #messages.error(request,f'Ha sucedido el siguiente error {form.errors }')
                form = CitaForm()

    return render(request, "edit_cita.html", {'form': form, 'footer': footer})




@login_required(login_url='login')
def edit_cita(request, pk):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    cita = get_object_or_404(Cita, id_cita=pk)
    if request.method == "POST":
        form = CitaForm(request.POST, instance=cita)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            messages.success(request,f'Se ha guardado la cita')
            return redirect("cliente_details_citas", pk=cita.paciente.id_paciente)
    else:
        form = CitaForm(instance=cita)
    return render(request, 'edit_cita.html', {'form': form, 'footer': footer})



@login_required(login_url='login')
def delete_cita(request, pk):
    footer=Configuracion.objects.all().last()
    cita1=get_object_or_404(Cita, pk=pk)
    cita=get_object_or_404(Cita, pk=pk).delete()
    messages.error(request,f'Se ha borrado la cita')
    return redirect("cliente_details_citas", pk=cita1.paciente.id_paciente)