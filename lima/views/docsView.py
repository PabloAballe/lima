
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



#documentos firmables
@login_required(login_url='login')
def docs_list(request):
    footer=Configuracion.objects.all().last()
    docs=DocTemplate.objects.all()

    #shearch emails
    notfound=False
    if request.method == "GET":
        form = SheachForm(request.GET)

    if form.is_valid():
            q= form.cleaned_data['shearch']
            existe=DocTemplate.objects.all().order_by('nombre_doc').filter(nombre__icontains=q).exists()
            if existe==True:
                docs=DocTemplate.objects.all().order_by('nombre_doc').filter(nombre__icontains=q)
            else:
                notfound=True
                print("no hay resultados")
    else:
        form = SheachForm()
    return render(request, 'docs/docs_list.html', {'footer': footer, 'docs': docs, 'form': form ,'notfound': notfound})
@login_required(login_url='login')
def docs_template(request, pk):
    footer=Configuracion.objects.all().last()
    doc=get_object_or_404(DocTemplate, pk=pk)
    form = DocTemplateEditForm(instance=doc)
    if request.method == 'POST':
        form = DocTemplateEditForm(request.POST, instance=doc)
        if form.is_valid():
            doc = form.save(commit=False)
            form.save()
            messages.success(request,f'Se ha guardado el documento')
            return redirect("docs_list")
        else:
           pass
    return render(request, 'docs/docs_template.html', {'footer': footer, 'form': form })


@login_required(login_url='login')
def delete_doc(request, pk):
    footer=Configuracion.objects.all().last()
    doc=get_object_or_404(DocTemplate, pk=pk).delete()
    messages.error(request,f'Se ha borrado el docuemento')
    return redirect("docs_list")
@login_required(login_url='login')
def new_doc_template(request):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    form=DocTemplateNewForm()
    if request.method == 'POST':
        form = DocTemplateNewForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,f'Se ha creado el documento')
            return redirect("docs_list")
    else:
        pass
    return render(request, 'docs/docs_template.html', {'footer': footer, 'form': form})


@login_required(login_url='login')
def doc_prerender(request, user,doc):
    footer=Configuracion.objects.all().last()
    doc_=get_object_or_404(DocTemplate, pk=doc)
    user_=get_object_or_404(Paciente, pk=user)
    sign__ = DocSings.objects.get_or_create(cliente=user_, plantilla_doc=doc_)
    sign=DocSings.objects.filter(cliente=user_, plantilla_doc=doc_).last()
    if sign.firma:
        firm=f'<img   width="10rem"  src="{sign.firma.url}" alt="{sign.plantilla_doc.nombre_doc}" />'
    else:
        firm=''
    if sign.plantilla_document=='':
        sign.plantilla_document=doc_.plantilla_doc
        sign.save()
    mensaje=Template(sign.plantilla_document)
    c = Context({
                'usuario': f'{user_.nombre_paciente} {user_.apellidos_paciente}',
                'centro': user_.centro.nombre_centro, 'localizacion_centro': user_.centro.localizacion,
                'nombre_comercial': footer.nombre_comercial, 'propietario': footer.propietario,
                'telefono': footer.telefono,
                'firma' : firm,
                'TelefonoUsuario':  user_.telefono_paciente,
                'EmailUsuario': user_.email,
                'dni': user_.dni,
                'poblacion': user_.poblacion,
                'direccion': user_.direccion,
                'FechaActual' : timezone.now(),
                'CitaURL': f'https://{request.get_host()}/website/appointment/{user_.centro.pk}94840{user_.pk}042f02cf{request.user.tecnica.pk}29d55a',
                })
    render_doc=mensaje.render(c)
    form=SingForm(instance=sign)
    if request.method == 'POST':
        form = SingForm(request.POST,request.FILES,instance=sign)
        if form.is_valid():
            try:
                sign.delete()
                firma=form.save(commit=False)
                sign.plantilla_document=render_doc
                firma.cliente=user_
                firma.save()
                messages.success(request,f'Se ha guardado el documento')
                return redirect("cliente_details_tratamientos", pk=user_.pk)
            except ValueError as e:
                messages.error(request,f'Ha ocurrido el siguiente error: ', e)
    else:
        form=SingForm(instance=sign)
    return render(request, "docs/doc_prerender.html" , {'form': form, 'footer': footer, 'doc': doc_,'sign': sign, 'cliente': user_ })
    #return HttpResponse('ok')
@login_required(login_url='login')
def docs_sign_list(request, user=0):
    footer=Configuracion.objects.all().last()
    docs=DocTemplate.objects.all()
    #shearch emails
    if user!=0:
        user=get_object_or_404(Paciente, pk=user)
    else:
        user=0
    notfound=False
    if request.method == "GET":
        form = SheachForm(request.GET)

    if form.is_valid():
            q= form.cleaned_data['shearch']
            existe=DocTemplate.objects.all().order_by('nombre_doc').filter(nombre__icontains=q).exists()
            if existe==True:
                docs=DocTemplate.objects.all().order_by('nombre_doc').filter(nombre__icontains=q)
            else:
                notfound=True
                print("no hay resultados")
    else:
        form = SheachForm()
    return render(request, 'docs/docs_list.html', {'footer': footer, 'docs': docs, 'form': form ,'notfound': notfound, 'cliente': user })



@login_required(login_url='login')
def doc_email(request, pk):
    footer=Configuracion.objects.all().last()
    doc=get_object_or_404(DocSings, pk=pk)
    cliente=doc.cliente
    mensaje=doc.plantilla_document
    mensaje=Template(mensaje)
    c = Context()
    mensaje=mensaje.render(c)
    subject = f'Tu documento de {doc.plantilla_doc.nombre_doc} de {footer.nombre_comercial}'
    template=mensaje
    html_message = render_to_string('core/blanc.html', {'mensaje': template, 'footer': footer})
    plain_message = strip_tags(html_message)
    from_email = f'Enviado por {footer.propietario}'
    to = cliente.email
    mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
    mail.send_mail(subject, plain_message, from_email, [footer.email_sistema], html_message=html_message)
    messages.success(request,f'Se ha enviado el documento por email')
    return redirect("cliente_details_tratamientos", pk=doc.cliente.pk)