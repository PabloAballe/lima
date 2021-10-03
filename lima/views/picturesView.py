
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
def lista_fotos(request, client):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    cls=get_object_or_404(Paciente, pk=client)
    fotos=ImagenesClientes.objects.all().filter(cliente=client).order_by('-fecha')
    return render(request, 'lista_fotos.html', {'footer': footer, 'cliente': cls, 'fotos': fotos })

@login_required(login_url='login')
def new_fotos(request, cliente):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    cls=get_object_or_404(Paciente, pk=cliente)
    form=FotoForm()
    if request.method == 'POST':
        form = FotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo=form.save(commit=False)
            photo.cliente=cls
            photo.tecnica=request.user.tecnica
            photo.save()
            messages.success(request,f'Se ha guardado la fotografia ')
            return redirect("lista_fotos", client=cls.pk)
    return render(request, 'new_fotos.html', {'footer': footer, 'form': form })

@login_required(login_url='login')
def delete_fotos(request,cliente, pk):
    foto=get_object_or_404(ImagenesClientes, pk=pk).delete()
    cls=get_object_or_404(Paciente, pk=cliente)
    return redirect("lista_fotos", client=cls.pk)
