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
def entrada(request):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    user=request.user
    entrada=ControlHorario(tecnica=request.user.tecnica, fecha=dt.datetime.now(), entrada=timezone.now().time())
    entrada.save()
    messages.success(request,f'Has fichado la entrada como {user.tecnica.nombre_tecnica}')
    return redirect("index")
@login_required(login_url='login')
def salida(request):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    user=request.user
    salida=ControlHorario.objects.filter(tecnica=user.tecnica, salida=None).last()
    salida.salida=timezone.now().time()
    salida.save()
    if footer.enviar_email_nuevo_fichaje:
        html= get_template('fichaje_mail.html')
        mensaje=Template(html)
        c =  Context({ 'horario': salida, 'footer': footer })
        subject = f'{salida.tecnica.nombre_tecnica} ha realizado un nuevo fichaje'
        template=mensaje
        html_message = render_to_string('fichaje_mail.html', {'horario': salida, 'footer': footer})
        plain_message = strip_tags(html_message)
        # from_email = f'Enviado desde {footer.nombre_comercial}'
        # to = footer.email_nueva_caja
        # mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
        try:
            message = Mail(
                        from_email=footer.email_sistema,
                        to_emails=cliente.email,
                        subject=subject,
                        html_content=html_message)

            sg = SendGridAPIClient(footer.twilio_SENDGRID_API_KEY)
            sg.send(message)
        except Exception as e:
            messages.error(request,f"A ocurrido el siguiente error {e}")
    messages.warning(request,f'Has fichado la salida como {user.tecnica.nombre_tecnica}')
    return redirect("index")