
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
def centro_details(request, pk):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    centro=get_object_or_404(Centro, id_centro=pk)
    anuncio=Anuncios.objects.filter(centro=centro).order_by("-fecha_creacion")
    notfound=False
    cliente=Paciente.objects.all().order_by("nombre_paciente").filter(centro=centro)
    #shearch cliente
    if request.method == "GET":
        form = SheachForm(request.GET)

    if form.is_valid():
            q= form.cleaned_data['shearch']
            existe=Paciente.objects.all().filter(centro=centro).order_by('nombre_paciente').filter(nombre_paciente__icontains=q).exists()
            if existe==True:
                cliente=Paciente.objects.all().filter(centro=centro).order_by('nombre_paciente').filter(nombre_paciente__icontains=q)
            else:
                notfound=True
                print("no hay resultados")
    else:
        form = SheachForm()

    #pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(cliente, 10)
    try:
        cen = paginator.page(page)
    except PageNotAnInteger:
        cen = paginator.page(1)
    except EmptyPage:
        cen = paginator.page(paginator.num_pages)


    return render(request, "centro_details.html", {'centro': centro, 'cliente': cen, 'cen': cen, 'form': form, 'notfound': notfound, 'footer': footer,'anuncio': anuncio})


@login_required(login_url='login')
def new_centro(request):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    form=CentroForm()
    if request.method == 'POST':
        form = CentroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,f'Se ha creado el centro ')
            return redirect("index")
    else:
        form = CentroForm()

    return render(request, "new_centro.html", {'form': form, 'footer': footer})




@login_required(login_url='login')
def edit_centro(request, pk):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    post = get_object_or_404(Centro, pk=pk)
    if request.method == "POST":
        form = CentroForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            messages.success(request,f'Se han guardado los datos del centro')
            return redirect('index')
    else:
        form = CentroForm(instance=post)
    return render(request, 'edit_centro.html', {'form': form, 'footer': footer})

@login_required(login_url='login')
def delete_centro(request, pk):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    centro=get_object_or_404(Centro, pk=pk).delete()
    messages.error(request,f'Se ha borrado el centro')
    return redirect("index")


