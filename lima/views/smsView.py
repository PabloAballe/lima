
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
def send_SMS(request):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    users=Paciente.objects.exclude(telefono_paciente=0)
    user_filter = ClientFilter(request.GET, queryset=users)
    title="Enviar SMS de Marketing"
    # client credentials are read from TWILIO_ACCOUNT_SID and AUTH_TOKEN
    client = Client(footer.twilio_ACCOUNT_SID, footer.twilio_AUTH_TOKEN)
    # this is the Twilio sandbox testing number
    from_number=f'+{footer.twilio_NUMBER}'
    form=WhatsappForm()
    if request.method == 'POST':
        form = WhatsappForm(request.POST)
        if form.is_valid():
            mensaje =form.cleaned_data["mensaje"]

            for usuario in user_filter.qs:
                msg=Template(mensaje)
                c = Context({'usuario': f'{usuario.nombre_paciente} {usuario.apellidos_paciente}',
                            'centro': usuario.centro.nombre_centro, 'localizacion_centro': usuario.centro.localizacion,
                            'nombre_comercial': footer.nombre_comercial, 'propietario': footer.propietario,
                            'telefono': footer.telefono,
                            'TelefonoUsuario':  usuario.telefono_paciente,
                            'EmailUsuario': usuario.email,
                            'dni': usuario.dni,
                            'poblacion': usuario.poblacion,
                            'direccion': usuario.direccion,
                            'FechaActual' : timezone.now(),})
                msg=msg.render(c)
                # replace this number with your own WhatsApp Messaging number
                to_number=f'+{usuario.telefono_paciente}'
                try:
                    client.messages.create(body=msg,
                       from_=from_whatsapp_number,
                       to=to_whatsapp_number)
                    messages.success(request,f'El mensaje se ha enviado correctamente')
                except Exception as e:
                    # handling exception
                    # and printing error message
                    messages.error(request,f"A ocurrido el siguiente error {e}")

            messages.success(request,f'Los mensajes se han enviado correctamente ')
            return redirect("index")
        else:
           messages.success(request,f'Los mensajes no se han podido enviar')

    return render(request, "marketing/send_emails.html", {'form': form, 'footer': footer,'filter': user_filter, 'title': title})