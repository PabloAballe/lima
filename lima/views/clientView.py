
# Create your views here.
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
from django.template import Context, Template
from django.contrib import messages
from ..filters import *
import os

#email
from twilio.rest import Client
from django.conf import settings
from mailchimp_marketing.api_client import ApiClientError
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


@login_required(login_url='login')
def clientes(request):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    cliente=Paciente.objects.all().order_by('nombre_paciente')
    user_filter = ClientFilter(request.GET, queryset=cliente)
    notfound=False
    #shearch cliente
    if request.method == "GET":
        form = SheachForm(request.GET)

    if form.is_valid():
            q= form.cleaned_data['shearch']
            existe=Paciente.objects.all().order_by('nombre_paciente').filter(nombre_paciente__icontains=q).exists()
            if existe==True:
                cliente=Paciente.objects.all().order_by('nombre_paciente').filter(nombre_paciente__icontains=q)
            else:
                notfound=True
                print("no hay resultados")
    else:
        form = SheachForm()

    context={ 'form': form, 'notfound': notfound,'footer':footer,'filter': user_filter}
    return render (request, 'client/table_clientes_total.html', context)
@login_required(login_url='login')
def cliente_details_citas(request, pk):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    cliente1=get_object_or_404(Paciente, pk=pk)
    lista=Lista.objects.all().order_by("-hora_inicio").filter(cliente=cliente1)
    return render(request, "client/cliente_details_cita.html", {'cliente': cliente1, 'footer': footer, 'lista': lista})

@login_required(login_url='login')
def cliente_details_tratamientos(request, pk):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    cliente1=get_object_or_404(Paciente, pk=pk)
    tratamientos=Tratamientos.objects.all().order_by("-fecha").filter(cliente=cliente1)
    return render(request, "client/cliente_details_tratamientos.html", {'cliente': cliente1, 'footer': footer, 'tratamientos': tratamientos})

@login_required(login_url='login')
def cliente_details_zonas(request, pk):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    cliente1=get_object_or_404(Paciente, pk=pk)
    cita=Cita.objects.all().order_by("fecha").filter(paciente=cliente1)
    return render(request, "client/cliente_details_zonas.html", {'cliente': cliente1, 'cita': cita, 'footer': footer})

@login_required(login_url='login')
def cliente_details(request, pk):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    cliente1=get_object_or_404(Paciente, pk=pk)
    cita=Cita.objects.all().order_by("fecha").filter(paciente=cliente1)
    tratamientos=Tratamientos.objects.all().order_by("fecha").filter(cliente=cliente1)
    lista=Lista.objects.all().order_by("-hora_inicio").filter(cliente=cliente1)
    return render(request, "client/cliente_details.html", {'cliente': cliente1, 'cita': cita, 'footer': footer, 'tratamientos': tratamientos, 'lista': lista})


@login_required(login_url='login')
def new_cliente(request, pk):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    centro1=get_object_or_404(Centro, id_centro=pk)
    form=ClienteForm()
    mensaje=footer.plantilla_email.plantilla
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.centro=centro1
            if cliente.estado is None:
                cliente.estado=1
            form.save()
            if footer.enviar_email_nuevos_clientes and footer.plantilla_email:
                mensaje=Template(mensaje)
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
                })
                mensaje=mensaje.render(c)
                subject = f'Bienvenido a {footer.nombre_comercial}'
                template=mensaje
                html_message = render_to_string('blanc.html', {'mensaje': template, 'footer': footer})
                plain_message = strip_tags(html_message)
                # from_email = f'Enviado por {footer.propietario}'
                # to = cliente.email
                # mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
                try:
                    message = Mail(
                        from_email=footer.email_sistema,
                        to_emails=cliente.email,
                        subject=subject,
                        html_content=html_message)

                    sg = SendGridAPIClient(footer.twilio_SENDGRID_API_KEY)
                    sg.send(message)
                    messages.success(request,f'Se ha enviado el Email a la dirección {cliente.email} ')
                except Exception as e:
                    messages.error(request,f"A ocurrido el siguiente error {e}")
            messages.success(request,f'Se ha creado el cliente {cliente.nombre_paciente}')
            return redirect("centro_details", pk=centro1.id_centro)
    else:
        form = ClienteForm()

    return render(request, "client/new_cliente.html", {'form': form, 'footer': footer})



@login_required(login_url='login')
def edit_cliente(request, pk):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    cliente = get_object_or_404(Paciente, pk=pk)
    if request.method == "POST":
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            messages.success(request,f'Se han guardado los datos del cliente {cliente.nombre_paciente}')
            return redirect("cliente_details_citas", pk=cliente.id_paciente)
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'client/edit_cliente.html', {'form': form, 'footer': footer})

@login_required(login_url='login')
def delete_cliente(request, pk):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    cliente1=get_object_or_404(Paciente, pk=pk)
    cliente=get_object_or_404(Paciente, pk=pk).delete()
    messages.error(request,f'Se ha borrado el cliente')
    return redirect("centro_details", pk=cliente1.centro.id_centro)
