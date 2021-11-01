
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
def new_tratamiento(request, pk):
    footer=Configuracion.objects.all().last()
    cliente1=get_object_or_404(Paciente, id_paciente=pk)
    if request.user.is_staff:
         form=TratamientoFormAdmin()
         if request.method == 'POST':
             form = TratamientoFormAdmin(request.POST)
             if form.is_valid():
                 cita = form.save(commit=False)
                 cita.cliente=cliente1
                 form.save()
                 messages.success(request,f'Se ha guardado el tratamiento')
                 return redirect("cliente_details_tratamientos", pk=cliente1.id_paciente)
             else:
                 pass

    else:
         form=TratamientoForm()
         if request.method == 'POST':
             form = TratamientoForm(request.POST)
             if form.is_valid():
                 cita = form.save(commit=False)
                 cita.cliente=cliente1
                 cita.tecnica=request.user.tecnica
                 form.save()
                 messages.success(request,f'Se ha guardado el tratamiento')
                 return redirect("cliente_details_tratamientos", pk=cliente1.id_paciente)
             else:
                pass

    return render(request, "treatments/new_tratamiento.html", {'form': form, 'footer': footer})

@login_required(login_url='login')
def edit_tratamiento(request, pk):
    footer=Configuracion.objects.all().last()
    tratamiento=get_object_or_404(Tratamientos, pk=pk)
    cliente1=tratamiento.cliente
    if request.user.is_staff:
         form=TratamientoFormAdmin(instance=tratamiento)
         if request.method == 'POST':
             form = TratamientoFormAdmin(request.POST, instance=tratamiento)
             if form.is_valid():
                 cita = form.save(commit=False)
                 cita.cliente=cliente1
                 form.save()
                 messages.success(request,f'Se ha guardado el tratamiento')
                 return redirect("cliente_details_tratamientos", pk=cliente1.id_paciente)
             else:
                 #messages.error(request,f'Ha sucedido el siguiente error {form.errors }')
                 form = CitaFormAdmin()
    else:
         form=TratamientoForm(instance=tratamiento)
         if request.method == 'POST':
             form = TratamientoForm(request.POST, instance=tratamiento)
             if form.is_valid():
                 cita = form.save(commit=False)
                 cita.cliente=cliente1
                 cita.tecnica=request.user.tecnica
                 form.save()
                 messages.success(request,f'Se ha guardado el tratamiento')
                 return redirect("cliente_details_tratamientos", pk=cliente1.id_paciente)
             else:
                pass


    return render(request, "treatments/edit_tratamiento.html", {'form': form, 'footer': footer})


@login_required(login_url='login')
def delete_tratamiento(request, pk):
    footer=Configuracion.objects.all().last()
    tratamiento=get_object_or_404(Tratamientos, pk=pk)
    tr=get_object_or_404(Tratamientos, pk=pk).delete()
    messages.error(request,f'Se ha borrado el tratamiento')
    return redirect("cliente_details_tratamientos", pk=tratamiento.cliente.id_paciente)