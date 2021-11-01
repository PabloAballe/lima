
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
from twilio.rest import Client
#email
from django.conf import settings
from mailchimp_marketing.api_client import ApiClientError
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.core.mail import send_mail

@login_required(login_url='login')
def caja_list(request, centro):
    footer=Configuracion.objects.all().last()
    if request.user.has_perm('lima.view_all_cajas') and centro==0:
        cajas=Cajas.objects.raw(f'SELECT * FROM lima_cajas   ORDER BY lima_cajas.fecha DESC LIMIT 50')
    elif centro!=0:
        cajas=Cajas.objects.raw(f'SELECT * FROM lima_cajas WHERE lima_cajas.centro_id={centro}  ORDER BY lima_cajas.fecha DESC LIMIT 50')
    else:
        now=dt.datetime.now ()
        dt_string = str(now.strftime("%Y-%m-%d %H:%M:%S"))
        tiempoExpira = footer.tiempo_expira_caja
        cajas=Cajas.objects.raw(F'SELECT * FROM lima_cajas WHERE fecha >= ("{dt_string}" - INTERVAL {tiempoExpira}  MINUTE ) AND tecnica_id = {request.user.tecnica.pk}  ORDER BY lima_cajas.fecha DESC LIMIT 50')
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")

    #pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(cajas, 10)
    try:
        cen = paginator.page(page)
    except PageNotAnInteger:
        cen = paginator.page(1)
    except EmptyPage:
        cen = paginator.page(paginator.num_pages)
    return render(request, 'cashDesk/caja_list.html', {'footer': footer, 'cajas': cen, 'cen': cen })

@login_required(login_url='login')
def caja(request, pk):
    footer=Configuracion.objects.all().last()
    if request.user.is_staff:
        if pk!=0:
            caja=get_object_or_404(Cajas, pk=pk)
            form=CajaFormAdmin(instance=caja)
            if request.method == 'POST':
                form = CajaFormAdmin(request.POST ,instance=caja)
                if form.is_valid():
                    form.save()
                    messages.success(request,f'Se ha guardado la caja del día ')

                    return redirect("caja_list", centro=0)
            else:
                pass
        else:
            form=CajaFormAdmin()
            if request.method == 'POST':
                form = CajaFormAdmin(request.POST)
                if form.is_valid():
                    caja = form.save()
                    messages.success(request,f'Se ha guardado la caja del día ')
                    if footer.email_nueva_caja==True:
                        plaintext = get_template('caja_mail.txt')
                        html     = get_template('caja_mail.html')
                        mensaje=Template(html)
                        c =  Context({ 'caja': caja })
                        subject = f'Se ha creado una nueva caja'
                        template=mensaje
                        html_message = render_to_string('caja_mail.html', {'caja': caja})
                        plain_message = strip_tags(html_message)
                    try:
                        from_email = footer.email_sistema
                        to = footer.email_nueva_caja
                        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
                        messages.success(request,f'Email Enviado a {cliente.email} ')
                    except Exception as e:
                        messages.error(request,f"A ocurrido el siguiente error {e}")
                    return redirect("caja_list" , centro=0)
    else:
        if pk!=0:
            caja=get_object_or_404(Cajas, pk=pk)
            form=CajaForm(instance=caja)
            if request.method == 'POST':
                form = CajaForm(request.POST ,instance=caja)
                if form.is_valid():
                    form.save()
                    messages.success(request,f'Se ha guardado la caja del día ')
                    return redirect("caja_list", centro=pk)
            else:
                pass
        else:
            form=CajaForm()
            if request.method == 'POST':
                form = CajaForm(request.POST)
                if form.is_valid():
                    caja = form.save(commit=False)
                    caja.tecnica=request.user.tecnica
                    caja = form.save()
                    messages.success(request,f'Se ha guardado la caja del día ')
                    if footer.email_nueva_caja==True:
                        plaintext = get_template('caja_mail.txt')
                        html     = get_template('caja_mail.html')
                        mensaje=Template(html)
                        c =  Context({ 'caja': caja })
                        subject = f'Se ha creado una nueva caja'
                        template=mensaje
                        html_message = render_to_string('caja_mail.html', {'caja': caja})
                        plain_message = strip_tags(html_message)
                    try:
                        from_email = footer.email_sistema
                        to = footer.email_nueva_caja
                        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
                        messages.success(request,f'Email Enviado a {cliente.email} ')
                    except Exception as e:
                        messages.error(request,f"A ocurrido el siguiente error {e}")
                    return redirect("caja_list", centro=pk)
    return render(request, 'cashDesk/caja.html', {'footer': footer,'form': form })