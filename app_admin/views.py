
# Create your views here.
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as do_logout
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as do_login
from lima.models import *
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from lima.forms import *
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
from lima.filters import *
import os
import webbrowser as web
from twilio.rest import Client
#mailchimp
from django.conf import settings
from mailchimp_marketing.api_client import ApiClientError
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.contrib.sessions.models import Session

# Create your views here.

def app_admin_index(request):
    page_name="Inicio"
    footer=Configuracion.objects.all().last()
    centro=Centro.objects.all().order_by('nombre_centro').filter(tecnica__id_tecnica=request.user.tecnica.id_tecnica)
    notfound=False
    #shearch centro
    if request.method == "GET":
        form = SheachForm(request.GET)

    if form.is_valid():
            q= form.cleaned_data['shearch']
            existe=Centro.objects.all().order_by('nombre_centro').filter(nombre_centro__icontains=q).filter(tecnica__id_tecnica=request.user.tecnica.id_tecnica).exists()
            if existe==True:
                centro=Centro.objects.all().order_by('nombre_centro').filter(nombre_centro__icontains=q).filter(tecnica__id_tecnica=request.user.tecnica.id_tecnica)
            else:
                notfound=True
                print("no hay resultados")
    else:
        form = SheachForm()
    return render(request, 'app_admin_index.html',{'cen': centro, 'form': form ,'notfound': notfound , 'footer': footer,'page_name':page_name})