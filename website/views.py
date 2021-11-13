from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
from lima.models import *
from lima.forms import *
import datetime as dt
from django.utils import timezone, dateformat
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.template import Context, Template
from django.contrib import messages
from twilio.rest import Client
#mailchimp
from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
# Create your views here.
from django.http import HttpResponse
from django.template.loader import render_to_string
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.utils import timezone
from django.utils.html import strip_tags

def config_website(request):
    conf=ConfiguracionWEB.objects.all().last()
    footer=Configuracion.objects.all().last()
    form=ConfigWebAdmin(instance=conf)
    if request.method == 'POST':
             form=ConfigWebAdmin(request.POST, request.FILES,instance=conf)
             if form.is_valid():
                 config = form.save(commit=False)
                 form.save()
                 messages.success(request,f'Se ha guardado la configuración')
                 return redirect("config_website")
             else:
                 #messages.error(request,f'Ha sucedido el siguiente error {form.errors }')
                 pass
    return render(request, "webConfig.html", {'form': form,'footer': footer})

def website_index(request):
    conf=ConfiguracionWEB.objects.all().last()
    page=Pages.objects.filter(pertenece_a="I")
    nav=Pages.objects.filter(pertenece_a="O")
    return render(request, "web_index.html", {'page': page, 'web': conf, 'nav': nav})

def website_blog_list(request):
    conf=ConfiguracionWEB.objects.all().last()
    page=Pages.objects.filter(pertenece_a="B")
    nav=Pages.objects.filter(pertenece_a="O")
    posts=Blog.objects.order_by('-creado_el')
    return render(request, "blogList.html", {'page': page, 'web': conf,'posts': posts, 'nav': nav})

def website_blog_details(request,slug):
    conf=ConfiguracionWEB.objects.all().last()
    nav=Pages.objects.filter(pertenece_a="O")
    post=get_object_or_404(Blog, slug_post=slug)
    return render(request, "blogDetails.html", {'web': conf,'post': post, 'nav': nav})

def website_contact(request):
    conf=ConfiguracionWEB.objects.all().last()
    page=Pages.objects.filter(pertenece_a="C")
    nav=Pages.objects.filter(pertenece_a="O")
    form=ContactForm(instance=conf)
    if request.method == 'POST':
         form=ContactForm(request.POST)
         if form.is_valid():
             form = form.save(commit=False)
             form.save()
             messages.success(request,f'Se ha enviado el mensaje')
             return redirect("website_index")
         else:
             #messages.error(request,f'Ha sucedido el siguiente error {form.errors }')
             pass
    return render(request, "contact.html", {'page': page,'web': conf, 'form': form, 'nav': nav})

def website_page(request, slug):
    conf=ConfiguracionWEB.objects.all().last()
    nav=Pages.objects.filter(pertenece_a="O")
    page=get_object_or_404(Pages, slug_pagina=slug)
    return render(request, "web_index.html", {'web': conf,'page': page, 'nav': nav})


def website_pdf(request, cita):
    lista=get_object_or_404(Lista, pk=cita)
    footer=Configuracion.objects.all().last()
    cliente=get_object_or_404(Paciente, pk=lista.cliente.pk)
    msg=footer.plantilla_lista.plantilla
    mensaje=Template(msg)
    c = Context({'usuario': f'{cliente.nombre_paciente} {cliente.apellidos_paciente}',
                'centro': cliente.centro.nombre_centro, 'localizacion_centro': cliente.centro.localizacion,
                'nombre_comercial': footer.nombre_comercial, 'propietario': footer.propietario,
                'telefono': footer.telefono,
                'TelefonoUsuario':  cliente.telefono_paciente,
                'EmailUsuario': cliente.email,
                'dni': cliente.dni,
                'poblacion': cliente.poblacion,
                'direccion': cliente.direccion,
                'FechaActual' : timezone.now(),
                'HoraInicioCita': lista.hora_inicio,
                'HoraFinCita': lista.hora_fin,
                'Servicio': lista.servicios.nombre_servicio,
                'CitaURL': f'https://{request.get_host()}/website/appointment/{cliente.centro.pk}94840{cliente.pk}042f02cf{request.user.tecnica.pk}29d55a'})
    mensaje=mensaje.render(c)
    template=mensaje
    html_message = render_to_string('core/blanc.html', {'mensaje': template, 'footer': footer})
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html_message.encode("ISO-8859-1")), result)
    if not pdf.err:
        messages.success(request,f'Aquí tiene su resguardo de cita por favor guardelo para el futuro')
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    messages.error(request,f'No se ha podido agendar la cita')
    return redirect("website_appointment", centro=lista.cliente.centro.pk , cliente=cliente.pk, tecnica=lista.tecnica.pk)


def website_appointment(request, centro, cliente, tecnica):
    conf=ConfiguracionWEB.objects.all().last()
    nav=Pages.objects.filter(pertenece_a="A")
    footer=Configuracion.objects.all().last()
    cen=get_object_or_404(Centro , pk=centro)
    msg=footer.plantilla_lista.plantilla
    days_off={}
    if ('Lunes' in cen.dias_abre_centro):days_off.append(2)
    if ('Martes' in cen.dias_abre_centro):days_off.append(3)
    if ('Miercoles' in cen.dias_abre_centro):days_off.append(4)
    if ('Jueves' in cen.dias_abre_centro):days_off.append(5)
    if ('Viernes' in cen.dias_abre_centro):days_off.append(6)
    if ('Sabado' in cen.dias_abre_centro):days_off.append(7)
    if ('Domingo' in cen.dias_abre_centro):days_off.append(1)
    bloqueos=Lista.objects.raw(f'SELECT  * FROM lima_lista  WHERE  lima_lista.centro_id={centro}')
    form=AppointmentWEBForm()
    cliente=get_object_or_404(Paciente, pk=cliente)
    tec=get_object_or_404(Tecnica, pk=tecnica)
    citasCliente=Lista.objects.filter(cliente=cliente, hora_inicio__gt=timezone.now(),is_app=True).count()

    if citasCliente>0:
        messages.warning(request,f'Ya tiene una cita agendada por favor contacte con el centro si ha perdido su resguardo')
        return redirect("website_index")

    if request.method == 'POST':
        form = AppointmentWEBForm(request.POST)
        if 1==9:
            messages.warning(request,f'Ya tiene una cita agendada por favor contacte con el centro si ha perdido su resguardo')
            return redirect("website_index")
        else:
            if form.is_valid():
                date = form.cleaned_data['hora_inicio']
                if date < dt.datetime.now():
                    messages.error(request,f'Debe ingresar una fecha a futuro para la cita')
                    return redirect("website_appointment", centro=cliente.centro.pk, cliente=cliente.pk, tecnica=tec.pk)
                lista=form.save(commit=False)
                lista.centro=cliente.centro
                lista.tecnica=tec
                lista.cliente=cliente
                lista.is_app=True
                fecha = (lista.hora_inicio +  dt.timedelta(minutes=lista.servicios.duracion_sevicio))
                lista.hora_fin=fecha
                lista.save()
                messages.success(request,f'Se ha agendado la cita ')
                mensaje=Template(msg)
                c = Context({'usuario': f'{cliente.nombre_paciente} {cliente.apellidos_paciente}',
                            'centro': cliente.centro.nombre_centro, 'localizacion_centro': cliente.centro.localizacion,
                            'nombre_comercial': footer.nombre_comercial, 'propietario': footer.propietario,
                            'telefono': footer.telefono,
                            'TelefonoUsuario':  cliente.telefono_paciente,
                            'EmailUsuario': cliente.email,
                            'dni': cliente.dni,
                            'poblacion': cliente.poblacion,
                            'direccion': cliente.direccion,
                            'FechaActual' : timezone.now(),
                            'HoraInicioCita': lista.hora_inicio,
                            'HoraFinCita': lista.hora_fin,
                            'Servicio': lista.servicios.nombre_servicio,
                            'CitaURL': f'https://{request.get_host()}/website/appointment/{cliente.centro.pk}94840{cliente.pk}042f02cf{request.user.tecnica.pk}29d55a'})
                mensaje=mensaje.render(c)
                subject = f'Resguardo de cita en{footer.nombre_comercial}'
                template=mensaje
                html_message = render_to_string('core/blanc.html', {'mensaje': template, 'footer': footer})
                plain_message = strip_tags(html_message)
                try:
                    from_email = f'Enviado por {footer.propietario}'
                    to = cliente.email
                    mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
                    messages.success(request,f'Email Enviado a {cliente.email} ')
                except Exception as e:
                    messages.error(request,f"A ocurrido el siguiente error {e}")
                return redirect("website_pdf" , cita=lista.pk)
    return render(request, "appointments.html", {'web': conf, 'nav': nav, 'bloqueos': bloqueos,'footer': footer,'form': form, 'cen': cen,'cliente': cliente})