
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
def sing(request, pk):
    footer=Configuracion.objects.all().last()
    sign_=get_object_or_404(DocSings, pk=pk)
    client=get_object_or_404(Paciente, pk=sign_.cliente.pk)
    form = SingForm()
    formatted_date = dateformat.format(timezone.now(), 'Y-m-d H:i:s')
    if request.method == 'POST':
        form = SingForm(request.POST, request.FILES)
        if form.is_valid():
            #messages.success(request,f'ha pasado por el valido')
            signature = form.cleaned_data.get('firma')
            if signature:
                sign_.imagen=signature
                # as an image
                # signature_picture = draw_signature(signature)
                # signature_file_path = draw_signature(signature, as_file=True)
                # try:
                #      filename=f'tmp_sign_{formatted_date}-{sign_.cliente.pk}.png'
                #      file = signature_picture.save(f'{settings.MEDIA_ROOT}/sings_user/{filename}' , mode='RGB')
                #      sign_.firma_imagen = f'{baseurl}/sings_user/{filename}'
                # except Exception as e:
                #     return HttpResponse(f"Error {e}")
                sign_.save()
            messages.success(request,f'Se ha guardado la firma')
            return redirect("cliente_details_citas", pk=sign_.cliente.pk)
        else:
           pass
    return render(request, 'signature/sing.html', {'footer': footer, 'form': form, 'client': client})