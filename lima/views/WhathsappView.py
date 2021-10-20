
# Vistas de Whathsapp
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
from django.contrib import messages
from ..filters import *
#mailchimp
from django.conf import settings

from twilio.rest import Client
#mailchimp
from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

@login_required(login_url='login')
def send_whatsApp(request):
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
    title="Enviar WhatsApps de Marketing"
    # client credentials are read from TWILIO_ACCOUNT_SID and AUTH_TOKEN
    client = Client(footer.twilio_ACCOUNT_SID, footer.twilio_AUTH_TOKEN)
    # this is the Twilio sandbox testing number
    from_whatsapp_number=f'whatsapp:+{footer.twilio_NUMBER}'
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
                            'FechaActual' : timezone.now(),
                            'CitaURL': f'https://{request.get_host()}/website/appointment/{usuario.centro.pk}94840{usuario.pk}042f02cf{request.user.tecnica.pk}29d55a'})
                msg=msg.render(c)
                # replace this number with your own WhatsApp Messaging number
                to_whatsapp_number=f'whatsapp:+{usuario.telefono_paciente}'
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