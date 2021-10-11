
# Vistas de Email
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..models import *
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ..forms import *
from django.shortcuts import render, get_object_or_404
import datetime as dt
from django.utils import timezone, dateformat
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.template import Context, Template
import base64
from django.core.files.base import ContentFile
from django.template.loader import get_template
from django.contrib import messages
from ..filters import *
from twilio.rest import Client
#mailchimp
from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django_mail_admin import mail, models


@login_required(login_url='login')
def emails_templates(request):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    emails=EmailTemplates.objects.all()
    #shearch emails
    notfound=False
    if request.method == "GET":
        form = SheachForm(request.GET)

    if form.is_valid():
            q= form.cleaned_data['shearch']
            existe=EmailTemplates.objects.all().order_by('nombre').filter(nombre__icontains=q).exists()
            if existe==True:
                emails=EmailTemplates.objects.all().order_by('nombre').filter(nombre__icontains=q)
            else:
                notfound=True
                print("no hay resultados")
    else:
        form = SheachForm()
    return render(request, 'marketing/emails_templates.html', {'footer': footer, 'emails': emails, 'form': form ,'notfound': notfound })

@login_required(login_url='login')
def emails_template(request, pk):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    email=get_object_or_404(EmailTemplates, pk=pk)
    form = EmailTemplateEditForm(instance=email)
    if request.method == 'POST':
        form = EmailTemplateEditForm(request.POST, instance=email)
        if form.is_valid():
            cita = form.save(commit=False)
            form.save()
            messages.success(request,f'Se han guardado la plantilla')
            return redirect("emails_templates")
        else:
           pass
    return render(request, 'marketing/emails_template.html', {'footer': footer, 'form': form })

@login_required(login_url='login')
def new_emails_template(request):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    form=EmailTemplateNewForm()
    if request.method == 'POST':
        form = EmailTemplateNewForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,f'Se ha creado la plantilla')
            return redirect("emails_templates")
    else:
        pass
    return render(request, 'marketing/new_email_templates.html', {'footer': footer, 'form': form})

@login_required(login_url='login')
def delete_email(request, pk):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    email=get_object_or_404(EmailTemplates, pk=pk).delete()
    messages.error(request,f'Se ha borrado la plantilla')
    return redirect("emails_templates")



@login_required(login_url='login')
def send_emails(request):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    users=Paciente.objects.exclude(email='')
    title="Enviar Emails de Marketing"
    user_filter = ClientFilter(request.GET, queryset=users)
    form=EmailForm()
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            asunto=form.cleaned_data["asunto"]
            destinatario=form.cleaned_data["destinatario"]
            enviar_a_las=form.cleaned_data["enviar_a_las"]
            enviar_a_las=time.mktime(datetime.datetime.strptime(enviar_a_las, "%Y-%m-%d").timetuple())
            mensaje=form.cleaned_data["plantilla"].plantilla
            for usuario in user_filter.qs:
                msj=Template(mensaje)
                c = Context({'usuario': f'{usuario.nombre_paciente} {usuario.apellidos_paciente}',
                            'centro': usuario.centro.nombre_centro, 'localizacion_centro': usuario.centro.localizacion,
                            'nombre_comercial': footer.nombre_comercial, 'propietario': footer.propietario,
                            'telefono': footer.telefono,
                            'TelefonoUsuario':  usuario.telefono_paciente,
                            'EmailUsuario': usuario.email,
                            'dni': usuario.dni,
                            'poblacion': usuario.poblacion,
                            'direccion': usuario.direccion,
                            'FechaActual' : timezone.now(),
                            'CitaURL': f'https://{request.get_host()}/website/appointment/{usuario.centro.pk}/{usuario.pk}/{request.user.tecnica.pk}'})
                msj=msj.render(c)
                subject = asunto
                html_message = render_to_string('blanc.html', {'mensaje': msj, 'footer': footer})
                plain_message = strip_tags(html_message)
                # from_email = f'Enviado por {destinatario}'
                # to = usuario.email
                # mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
                try:

                    message = Mail(
                        from_email=footer.email_sistema,
                        to_emails=usuario.email,
                        subject=subject,
                        send_at=enviar_a_las,
                        html_content=html_message)

                    sg = SendGridAPIClient(footer.twilio_SENDGRID_API_KEY)
                    sg.send(message)
                    messages.success(request,f'Se han enviado los Emails ')
                except Exception as e:
                    messages.error(request,f"A ocurrido el siguiente error {e}")
            return redirect("index")
        else:
           pass

    return render(request, "marketing/send_emails.html", {'form': form, 'footer': footer,'filter': user_filter,'title': title})




