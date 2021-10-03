
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
def historial(request):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    historial_centro=Centro.history.all().order_by("-history_date")[:500]
    historial_paciente=Paciente.history.all().order_by("-history_date")[:500]
    historial_tecnica=Tecnica.history.all().order_by("-history_date")[:500]
    historial_cita=Cita.history.all().order_by("-history_date")[:500]
    historial_controlhorario=ControlHorario.history.all().order_by("-history_date")[:500]
    historial_turnos=Turnos.history.all().order_by("-history_date")[:500]
    historial_email=EmailTemplates.history.all().order_by("-history_date")[:500]
    historial_total=list(chain(historial_centro,historial_paciente,historial_tecnica,historial_cita, historial_controlhorario, historial_turnos, historial_email))
    #pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(historial_total, 10)
    try:
        cen = paginator.page(page)
    except PageNotAnInteger:
        cen = paginator.page(1)
    except EmptyPage:
        cen = paginator.page(paginator.num_pages)
    return render(request, 'history.html', {'historial_centro': cen , 'cen': cen , 'footer': footer})