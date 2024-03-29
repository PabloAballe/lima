
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
from django.template.loader import render_to_string
from django.template import Context, Template
from django.contrib import messages
from ..filters import *
from django.core.mail import send_mail
from twilio.rest import Client
#mailchimp
from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

@login_required(login_url='login')
def listas(request, centro=0, pk=0):
    footer=Configuracion.objects.all().last()
    if centro==0 and pk==0:
        lista=Lista.objects.all().order_by("-hora_inicio")
        lista_future=Lista.objects.raw('SELECT * FROM 	lima_lista  WHERE 	lima_lista.hora_inicio>=CURDATE()')
    elif centro!=0:
        lista=Lista.objects.raw(f'SELECT  	* FROM 	lima_lista  WHERE  lima_lista.centro_id={centro}')
        lista_future=Lista.objects.raw(f'SELECT  * FROM 	lima_lista  WHERE 	lima_lista.hora_inicio>=CURDATE() 	AND lima_lista.centro_id={centro}')
    else:
        lista=Lista.objects.raw(f'SELECT  	* FROM 	lima_lista  WHERE  lima_lista.tecnica_id={pk}')
        lista_future=Lista.objects.raw(f'SELECT  * FROM 	lima_lista  WHERE 	lima_lista.hora_inicio>=CURDATE() AND lima_lista.tecnica_id={pk}')
    return render(request, 'appointments/listas.html', {'footer': footer, 'lista': lista, 'lista_future': lista_future})

@login_required(login_url='login')
def edit_lista(request, paciente=0,pk=0):
    footer=Configuracion.objects.all().last()
    msg=footer.plantilla_lista.plantilla
    if pk!=0:
        lista=get_object_or_404(Lista, pk=pk)
        mensaje=footer.plantilla_email.plantilla
        form=ListaForm(instance=lista)
        if request.method == 'POST':
            form = ListaForm(request.POST ,instance=lista)
            if form.is_valid():
                lista=form.save(commit=False)
                fecha = (lista.hora_inicio +  dt.timedelta(minutes=lista.servicios.duracion_sevicio))
                lista.hora_fin=fecha
                flag=Lista.objects.raw(f"SELECT lima_lista.id_lista,COUNT(lima_lista.id_lista) AS flag FROM 	lima_lista WHERE 	lima_lista.centro_id={lista.centro.pk} AND ( (	lima_lista.hora_inicio >= '{lista.hora_inicio}' AND lima_lista.hora_inicio<='{lista.hora_fin}') OR (lima_lista.hora_fin> '{lista.hora_inicio}' AND lima_lista.hora_fin < '{lista.hora_fin}'))")
                if flag[0].flag!=0:
                    messages.error(request,f'No se ha podido guardar la cita porque no se encuentra este espacio y técnica disponible actualmente de {lista.hora_inicio} a {lista.hora_fin}')
                    return redirect("cliente_details_citas", pk=lista.cliente.pk)
                else:
                    lista.save()
                    messages.success(request,f'Se ha guardado la cita ')
                    cliente=lista.cliente
                    if footer.enviar_email_nuevas_listas and footer.plantilla_lista :
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
                        subject = f'Resguardo de cita con {footer.nombre_comercial}'
                        template=mensaje
                        html_message = render_to_string('blanc.html', {'mensaje': template, 'footer': footer})
                        plain_message = strip_tags(html_message)

                        try:
                            from_email = f'Enviado por {footer.propietario}'
                            to = cliente.email
                            mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
                            messages.success(request,f'Email Enviado a {cliente.email} ')
                        except Exception as e:
                            messages.error(request,f"A ocurrido el siguiente error {e}")
                    return redirect("cliente_details_citas", pk=lista.cliente.pk)
        else:
            pass
    else:
        form=ListaForm()
        cliente=get_object_or_404(Paciente, pk=paciente)
        if request.method == 'POST':
            form = ListaForm(request.POST)
            if form.is_valid():
                date = form.cleaned_data['hora_inicio']
                if date < dt.datetime.now():
                    messages.error(request,f'Debe ingresar una fecha a futuro para la cita')
                    return redirect("cliente_details", pk=cliente.pk)
                lista=form.save(commit=False)
                lista.centro=cliente.centro
                lista.cliente=cliente
                fecha = (lista.hora_inicio +  dt.timedelta(minutes=lista.servicios.duracion_sevicio))
                lista.hora_fin=fecha
                flag=Lista.objects.raw(f"SELECT lima_lista.id_lista,COUNT(lima_lista.id_lista) AS flag FROM 	lima_lista WHERE 	lima_lista.centro_id={lista.centro.pk} 	AND ( (	lima_lista.hora_inicio >= '{lista.hora_inicio}' AND lima_lista.hora_inicio<='{lista.hora_fin}') OR (lima_lista.hora_fin> '{lista.hora_inicio}' AND lima_lista.hora_fin < '{lista.hora_fin}'))")
                if flag[0].flag>0:
                    messages.error(request,f'No se ha podido guardar la cita porque no se encuentra este espacio y técnica disponible actualmente de {lista.hora_inicio} a {lista.hora_fin}')
                    return redirect("cliente_details_citas", pk=lista.cliente.pk)
                else:
                    lista.save()
                    messages.success(request,f'Se ha guardado la cita ')
                    if footer.enviar_email_nuevas_listas and footer.plantilla_lista :
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
                        subject = f'Resguardo de cita con {footer.nombre_comercial}'
                        template=mensaje
                        html_message = render_to_string('blanc.html', {'mensaje': template, 'footer': footer})
                        plain_message = strip_tags(html_message)
                        try:
                            from_email = f'Enviado por {footer.propietario}'
                            to = cliente.email
                            mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
                            messages.success(request,f'Email Enviado a {cliente.email} ')
                        except Exception as e:
                            messages.error(request,f"A ocurrido el siguiente error {e}")
                    return redirect("cliente_details_citas", pk=lista.cliente.pk)

    return render(request, 'appointments/edit_lista.html', {'footer': footer, 'form': form })

@login_required(login_url='login')
def delete_lista(request, pk=0):
    list=get_object_or_404(Lista, pk=pk)
    lista=get_object_or_404(Lista, pk=pk).delete()
    return redirect("cliente_details_citas", pk=list.cliente.pk)