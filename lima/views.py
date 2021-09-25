
# Create your views here.
from django.shortcuts import render, redirect
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


#mailchimp
from django.conf import settings
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError

@login_required(login_url='login')
def admin(request):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    return redirect("admin/")

@login_required(login_url='login')
def index(request):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
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

    page = request.GET.get('page', 1)
    paginator = Paginator(centro, 5)
    try:
        cen = paginator.page(page)
    except PageNotAnInteger:
        cen = paginator.page(1)
    except EmptyPage:
        cen = paginator.page(paginator.num_pages)
    #checkea si ha enytrado o salido
    user=request.user

    horario=ControlHorario.objects.filter(tecnica=user.tecnica).last()
    salida=False
    if horario:
        if horario.salida is None:
            salida=True
    else:
        salida=False


    #fin del bloque
     # determino si el centro está trabajando o no
    now=dt.datetime.now()
    return render(request, 'index.html',{'cen': cen, 'form': form ,'notfound': notfound ,'salida': salida, 'footer': footer,'cTime':now})

def login(request):
    footer=Configuracion.objects.all().last()
    form = AuthenticationForm()
    if request.method == "POST":
        # Añadimos los datos recibidos al formulario
        form = AuthenticationForm(data=request.POST)
        # Si el formulario es válido...
        if form.is_valid():
            # Recuperamos las credenciales validadas
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Verificamos las credenciales del usuario
            user = authenticate(username=username, password=password)

            # Si existe un usuario con ese nombre y contraseña
            if user is not None:
                # Hacemos el login manualmente
                do_login(request, user)
                messages.success(request,f'Has iniciado sesión como {username}')
                # Y le redireccionamos a la portada
                return redirect('/')

    # Si llegamos al final renderizamos el formulario
    return render(request, "login.html", {'form': form, 'footer': footer})
@login_required(login_url='login')
def logout(request):
    footer=Configuracion.objects.all().last()
    do_logout(request)
    messages.warning(request,f'Has cerrado sesión')
    return redirect('login')
@login_required(login_url='login')
def centro_details(request, pk):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    centro=get_object_or_404(Centro, id_centro=pk)
    anuncio=Anuncios.objects.filter(centro=centro).order_by("-fecha_creacion")
    notfound=False
    cliente=Paciente.objects.all().order_by("nombre_paciente").filter(centro=centro)
    #shearch cliente
    if request.method == "GET":
        form = SheachForm(request.GET)

    if form.is_valid():
            q= form.cleaned_data['shearch']
            existe=Paciente.objects.all().filter(centro=centro).order_by('nombre_paciente').filter(nombre_paciente__icontains=q).exists()
            if existe==True:
                cliente=Paciente.objects.all().filter(centro=centro).order_by('nombre_paciente').filter(nombre_paciente__icontains=q)
            else:
                notfound=True
                print("no hay resultados")
    else:
        form = SheachForm()

    #pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(cliente, 10)
    try:
        cen = paginator.page(page)
    except PageNotAnInteger:
        cen = paginator.page(1)
    except EmptyPage:
        cen = paginator.page(paginator.num_pages)


    return render(request, "centro_details.html", {'centro': centro, 'cliente': cen, 'cen': cen, 'form': form, 'notfound': notfound, 'footer': footer,'anuncio': anuncio})
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
    #pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(cliente, 10)
    try:
        cen = paginator.page(page)
    except PageNotAnInteger:
        cen = paginator.page(1)
    except EmptyPage:
        cen = paginator.page(paginator.num_pages)
    context={'cliente': cen, 'cen': cen, 'form': form, 'notfound': notfound,'footer':footer}
    return render (request, 'table_clientes_total.html', context)
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
    return render(request, "cliente_details_cita.html", {'cliente': cliente1, 'footer': footer, 'lista': lista})

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
    tratamientos=Tratamientos.objects.all().order_by("fecha").filter(cliente=cliente1)
    return render(request, "cliente_details_tratamientos.html", {'cliente': cliente1, 'footer': footer, 'tratamientos': tratamientos})

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
    return render(request, "cliente_details_zonas.html", {'cliente': cliente1, 'cita': cita, 'footer': footer})

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
    return render(request, "cliente_details.html", {'cliente': cliente1, 'cita': cita, 'footer': footer, 'tratamientos': tratamientos, 'lista': lista})
@login_required(login_url='login')
def new_centro(request):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    form=CentroForm()
    if request.method == 'POST':
        form = CentroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,f'Se ha creado el centro ')
            return redirect("index")
    else:
        form = CentroForm()

    return render(request, "new_centro.html", {'form': form, 'footer': footer})
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
                from_email = f'Enviado por {footer.propietario}'
                to = cliente.email
                mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
                print(f"Email Enviado a {cliente.email} ")
                messages.success(request,f'Se ha enviado el Email a la dirección {cliente.email} ')
            messages.success(request,f'Se ha creado el cliente {cliente.nombre_paciente}')
            return redirect("centro_details", pk=centro1.id_centro)
    else:
        form = ClienteForm()

    return render(request, "new_cliente.html", {'form': form, 'footer': footer})

@login_required(login_url='login')
def new_cita(request, pk):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    cliente1=get_object_or_404(Paciente, id_paciente=pk)
    if request.user.is_staff:
         form=CitaFormAdmin()
         if request.method == 'POST':
             form = CitaFormAdmin(request.POST)
             if form.is_valid():
                 cita = form.save(commit=False)
                 cita.paciente=cliente1
                 form.save()
                 messages.success(request,f'Se ha guardado la cita del cliente {cita.paciente.nombre_paciente}')
                 return redirect("cliente_details_zonas", pk=cliente1.id_paciente)
             else:
                 messages.error(request,f'Ha sucedido el siguiente error {form.errors }')
                 form = CitaFormAdmin()
    else:
         form=CitaForm()
         if request.method == 'POST':
             form = CitaForm(request.POST)
             if form.is_valid():
                 cita = form.save(commit=False)
                 cita.paciente=cliente1
                 cita.tecnica=request.user.tecnica
                 form.save()
                 messages.success(request,f'Se ha creado el cliente {cita.paciente.nombre_paciente}')
                 return redirect("cliente_details_zonas", pk=cliente1.id_paciente)
             else:
                #messages.error(request,f'Ha sucedido el siguiennte error {form.errors }')
                form = CitaForm()

    return render(request, "new_cita.html", {'form': form, 'footer': footer})

@login_required(login_url='login')
def edit_cita(request, pk):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    cita=get_object_or_404(Cita, pk=pk)
    if request.user.is_staff:
         form=CitaFormAdmin()
         if request.method == 'POST':
             form = CitaFormAdmin(request.POST, instance=post)
             if form.is_valid():
                 cita = form.save(commit=False)
                 cita.paciente=cliente1
                 form.save()
                 messages.success(request,f'Se ha guardado la cita')
                 return redirect("cliente_details_zonas", pk=cliente1.id_paciente)
             else:
                 #messages.error(request,f'Ha sucedido el siguiente error {form.errors }')
                 form = CitaFormAdmin()
    else:
         form=CitaForm()
         if request.method == 'POST':
             form = CitaForm(request.POST, instance=post)
             if form.is_valid():
                 cita = form.save(commit=False)
                 cita.paciente=cliente1
                 cita.tecnica=request.user.tecnica
                 form.save()
                 messages.success(request,f'Se ha guardado la cita')
                 return redirect("cliente_details_zonas", pk=cliente1.id_paciente)
             else:
                #messages.error(request,f'Ha sucedido el siguiente error {form.errors }')
                form = CitaForm()

    return render(request, "edit_cita.html", {'form': form, 'footer': footer})
@login_required(login_url='login')
def new_tratamiento(request, pk):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    cliente1=get_object_or_404(Paciente, id_paciente=pk)
    if request.user.is_staff:
         form=TratamientoFormAdmin()
         if request.method == 'POST':
             form = TratamientoFormAdmin(request.POST)
             if form.is_valid():
                 cita = form.save(commit=False)
                 cita.cliente=cliente1
                 form.save()
                 messages.success(request,f'Se ha guardado el tratamiento')
                 return redirect("cliente_details_tratamientos", pk=cliente1.id_paciente)
             else:
                 pass

    else:
         form=TratamientoForm()
         if request.method == 'POST':
             form = TratamientoForm(request.POST)
             if form.is_valid():
                 cita = form.save(commit=False)
                 cita.cliente=cliente1
                 cita.tecnica=request.user.tecnica
                 form.save()
                 messages.success(request,f'Se ha guardado el tratamiento')
                 return redirect("cliente_details_tratamientos", pk=cliente1.id_paciente)
             else:
                pass

    return render(request, "new_tratamiento.html", {'form': form, 'footer': footer})

@login_required(login_url='login')
def edit_tratamiento(request, pk):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    tratamiento=get_object_or_404(Tratamientos, pk=pk)
    cliente1=tratamiento.cliente
    if request.user.is_staff:
         form=TratamientoFormAdmin(instance=tratamiento)
         if request.method == 'POST':
             form = TratamientoFormAdmin(request.POST, instance=tratamiento)
             if form.is_valid():
                 cita = form.save(commit=False)
                 cita.cliente=cliente1
                 form.save()
                 messages.success(request,f'Se ha guardado el tratamiento')
                 return redirect("cliente_details_tratamientos", pk=cliente1.id_paciente)
             else:
                 #messages.error(request,f'Ha sucedido el siguiente error {form.errors }')
                 form = CitaFormAdmin()
    else:
         form=TratamientoForm(instance=tratamiento)
         if request.method == 'POST':
             form = TratamientoForm(request.POST, instance=tratamiento)
             if form.is_valid():
                 cita = form.save(commit=False)
                 cita.cliente=cliente1
                 cita.tecnica=request.user.tecnica
                 form.save()
                 messages.success(request,f'Se ha guardado el tratamiento')
                 return redirect("cliente_details_tratamientos", pk=cliente1.id_paciente)
             else:
                pass


    return render(request, "edit_tratamiento.html", {'form': form, 'footer': footer})

@login_required(login_url='login')
def edit_centro(request, pk):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    post = get_object_or_404(Centro, pk=pk)
    if request.method == "POST":
        form = CentroForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            messages.success(request,f'Se han guardado los datos del centro')
            return redirect('index')
    else:
        form = CentroForm(instance=post)
    return render(request, 'edit_centro.html', {'form': form, 'footer': footer})
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
    return render(request, 'edit_cliente.html', {'form': form, 'footer': footer})
@login_required(login_url='login')
def edit_cita(request, pk):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    cita = get_object_or_404(Cita, id_cita=pk)
    if request.method == "POST":
        form = CitaForm(request.POST, instance=cita)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            messages.success(request,f'Se ha guardado la cita')
            return redirect("cliente_details_citas", pk=cita.paciente.id_paciente)
    else:
        form = CitaForm(instance=cita)
    return render(request, 'edit_cita.html', {'form': form, 'footer': footer})
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
@login_required(login_url='login')
def delete_centro(request, pk):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    centro=get_object_or_404(Centro, pk=pk).delete()
    messages.error(request,f'Se ha borrado el centro')
    return redirect("index")
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
@login_required(login_url='login')
def delete_cita(request, pk):
    footer=Configuracion.objects.all().last()
    cita1=get_object_or_404(Cita, pk=pk)
    cita=get_object_or_404(Cita, pk=pk).delete()
    messages.error(request,f'Se ha borrado la cita')
    return redirect("cliente_details_citas", pk=cita1.paciente.id_paciente)
@login_required(login_url='login')
def delete_tratamiento(request, pk):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    tratamiento=get_object_or_404(Tratamientos, pk=pk)
    tr=get_object_or_404(Tratamientos, pk=pk).delete()
    messages.error(request,f'Se ha borrado el tratamiento')
    return redirect("cliente_details_tratamientos", pk=tratamiento.cliente.id_paciente)
@login_required(login_url='login')
def entrada(request):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    user=request.user
    entrada=ControlHorario(tecnica=request.user.tecnica, fecha=dt.datetime.now(), entrada=timezone.now().time())
    entrada.save()
    messages.success(request,f'Has fichado la entrada como {user.tecnica.nombre_tecnica}')
    return redirect("index")
@login_required(login_url='login')
def salida(request):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    user=request.user
    salida=ControlHorario.objects.filter(tecnica=user.tecnica, salida=None).last()
    salida.salida=timezone.now().time()
    salida.save()
    if footer.enviar_email_nuevo_fichaje:
        html= get_template('fichaje_mail.html')
        mensaje=Template(html)
        c =  Context({ 'horario': salida, 'footer': footer })
        subject = f'{salida.tecnica.nombre_tecnica} ha realizado un nuevo fichaje'
        template=mensaje
        html_message = render_to_string('fichaje_mail.html', {'horario': salida, 'footer': footer})
        plain_message = strip_tags(html_message)
        from_email = f'Enviado desde {footer.nombre_comercial}'
        to = footer.email_nueva_caja
        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
    messages.warning(request,f'Has fichado la salida como {user.tecnica.nombre_tecnica}')
    return redirect("index")
@login_required(login_url='login')
def perfil(request):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    user=request.user
    meses=ControlHorario.objects.filter(tecnica=user.tecnica).order_by("-fecha", "-entrada")
    #pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(meses, 10)
    try:
        cen = paginator.page(page)
    except PageNotAnInteger:
        cen = paginator.page(1)
    except EmptyPage:
        cen = paginator.page(paginator.num_pages)
    #checkea si ha enytrado o salido
    user=request.user
    horario=ControlHorario.objects.filter(tecnica=user.tecnica).last()
    salida=False
    if horario:
        if horario.salida is None:
            salida=True
    else:
        salida=False

    return render(request, 'perfil.html', {'meses': cen,'cen': cen, 'salida': salida, 'footer': footer })

@login_required(login_url='login')
def view_perfiles(request):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    tecnica= Tecnica.objects.all().order_by("-nombre_tecnica")
    notfound=False
    #shearch perfiles
    if request.method == "GET":
        form = SheachForm(request.GET)

    if form.is_valid():
        q= form.cleaned_data['shearch']
        existe=Tecnica.objects.all().order_by('nombre_tecnica').filter(nombre_tecnica__icontains=q).exists()
        if existe==True:
            tecnica=Tecnica.objects.all().order_by('nombre_tecnica').filter(nombre_tecnica__icontains=q)
        else:
            notfound=True
            print("no hay resultados")
    else:
        form = SheachForm()

    #pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(tecnica, 10)
    try:
        cen = paginator.page(page)
    except PageNotAnInteger:
        cen = paginator.page(1)
    except EmptyPage:
        cen = paginator.page(paginator.num_pages)
    return render(request, 'view_perfiles.html', { 'tecnica': cen , 'form': form, 'footer': footer, 'cen': cen,'notfound': notfound  })

@login_required(login_url='login')
def ver_horario(request, pk):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    salida=False
    #checkea si ha enytrado o salido
    tecnica=get_object_or_404(Tecnica, pk=pk)
    meses=ControlHorario.objects.filter(tecnica=tecnica).order_by("-fecha", "-entrada")[:90]
    horario=ControlHorario.objects.filter(tecnica=tecnica).last()
    if horario:
        if horario.salida is None:
            salida=True
    else:
        salida=False
    return render(request, 'perfil_horario.html', {'meses': meses, 'salida': salida, 'tecnica': tecnica, 'footer': footer })



@login_required(login_url='login')
def ver_horario_visual(request, pk):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    today = dt.datetime.now()
    salida=False
    #checkea si ha enytrado o salido
    tecnica=get_object_or_404(Tecnica, pk=pk)
    meses=ControlHorario.objects.filter(tecnica=tecnica).order_by("-fecha", "-entrada")
    horario=ControlHorario.objects.filter(tecnica=tecnica).last()
    if horario:
        if horario.salida is None:
            salida=True
    else:
        salida=False
    return render(request, 'calendar_horario.html', {'meses': meses, 'salida': salida, 'tecnica': tecnica , 'today': today, 'footer': footer})

@login_required(login_url='login')
def ver_visual_tecnica(request, pk):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    today = dt.datetime.now()
    salida=False
    tecnica=request.user.tecnica
    #checkea si ha enytrado o salido
    if pk !=0:
        tecnica=get_object_or_404(Tecnica, pk=pk)
        tecnicas=Tecnica.objects.filter(id_tecnica=pk)
        citas=Tratamientos.objects.filter(tecnica=tecnica).order_by("-fecha")
        meses = citas
        horario=ControlHorario.objects.filter(tecnica=tecnica).last()
    else:
        citas=Tratamientos.objects.all().order_by("-fecha")
        tecnicas=Tecnica.objects.all().filter(habilitado=True)
        meses = citas
        horario=ControlHorario.objects.filter(tecnica=request.user.tecnica).last()

    if horario:
        if horario.salida is None:
            salida=True
    else:
        salida=False
    return render(request, 'ver_visual_tecnica.html', {'meses': meses, 'salida': salida, 'tecnica': tecnica , 'today': today, 'footer': footer, 'tecnicas': tecnicas})


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
    user_filter = ClientFilter(request.GET, queryset=users)
    form=EmailForm()
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            asunto=form.cleaned_data["asunto"]
            destinatario=form.cleaned_data["destinatario"]
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
                            'FechaActual' : timezone.now(),})
                msj=msj.render(c)
                subject = asunto
                html_message = render_to_string('blanc.html', {'mensaje': msj, 'footer': footer})
                plain_message = strip_tags(html_message)
                from_email = f'Enviado por {destinatario}'
                to = usuario.email
                mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
            messages.success(request,f'Se han enviado los Emails ')
            return redirect("index")
        else:
           pass

    return render(request, "send_emails.html", {'form': form, 'footer': footer,'filter': user_filter})
@login_required(login_url='login')
def edit_turno(request, pk):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    today = dt.datetime.now()
    salida=False
    if pk !=0:
        tecnica=get_object_or_404(Tecnica, pk=pk)
        meses=Turnos.objects.filter(tecnica=tecnica).order_by("-turno")
    else:
        tecnica =request.user.tecnica
        meses=Turnos.objects.all().order_by("-turno")

    horario=ControlHorario.objects.filter(tecnica=tecnica).last()
    if horario:
        if horario.salida is None:
            salida=True
    else:
        salida=False
    return render(request, 'edit_turno.html', {'meses': meses, 'salida': salida, 'tecnica': tecnica , 'today': today, 'footer': footer})
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
    return render(request, 'emails_templates.html', {'footer': footer, 'emails': emails, 'form': form ,'notfound': notfound })

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
    return render(request, 'emails_template.html', {'footer': footer, 'form': form })

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
    return render(request, 'new_email_templates.html', {'footer': footer, 'form': form})

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

#documentos firmables
@login_required(login_url='login')
def docs_list(request):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
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
    return render(request, 'docs_list.html', {'footer': footer, 'docs': docs, 'form': form ,'notfound': notfound})
@login_required(login_url='login')
def docs_template(request, pk):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
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
    return render(request, 'docs_template.html', {'footer': footer, 'form': form })


@login_required(login_url='login')
def delete_doc(request, pk):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
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
    return render(request, 'docs_template.html', {'footer': footer, 'form': form})

@login_required(login_url='login')
def sing(request, pk):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    sign_=get_object_or_404(DocSings, pk=pk)
    form = SingForm()
    formatted_date = dateformat.format(timezone.now(), 'Y-m-d H:i:s')
    baseurl='https://wavecompany.pythonanywhere.com/media'
    if request.method == 'POST':
        form = SingForm(request.POST or None, instance=sign_)
        if form.is_valid():
            signature = form.cleaned_data.get('firma')
            if signature:
                # as an image
                signature_picture = draw_signature(signature)
                signature_file_path = draw_signature(signature, as_file=True)
                try:
                     filename=f'tmp_sign_{formatted_date}-{sign_.cliente.pk}.png'
                     file = signature_picture.save(f'{settings.MEDIA_ROOT}/sings_user/{filename}' , mode='RGB')
                     sign_.firma_imagen = f'{baseurl}/sings_user/{filename}'
                except Exception as e:
                    return HttpResponse(f"Error {e}")
                form.save()
            messages.success(request,f'Se ha guardado la firma')
            return redirect("cliente_details_citas", pk=sign_.cliente.pk)
        else:
           pass
    return render(request, 'sing.html', {'footer': footer, 'form': form})
@login_required(login_url='login')
def doc_prerender(request, user,doc):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    doc_=get_object_or_404(DocTemplate, pk=doc)
    user_=get_object_or_404(Paciente, pk=user)
    sign = DocSings.objects.get_or_create(cliente=user_, plantilla_doc=doc_)
    sign_=get_object_or_404(DocSings, cliente=user_, plantilla_doc=doc_)
    if sign_.plantilla_render=='':
        sign_.plantilla_render=doc_.plantilla_doc
    firm=' <img   width="20%"  src="{{ sign_.firma_imagen }}" alt=" {{sign_.plantilla_doc.nombre_doc}} " />'
    mensaje= sign_.plantilla_render
    mensaje=Template(mensaje)
    c = Context({
                'usuario': f'{user_.nombre_paciente} {user_.apellidos_paciente}',
                'centro': user_.centro.nombre_centro, 'localizacion_centro': user_.centro.localizacion,
                'nombre_comercial': footer.nombre_comercial, 'propietario': footer.propietario,
                'telefono': footer.telefono,
                'firma' : firm, 'sign_': sign_ ,
                'TelefonoUsuario':  user_.telefono_paciente,
                'EmailUsuario': user_.email,
                'dni': user_.dni,
                'poblacion': user_.poblacion,
                'direccion': user_.direccion,
                'FechaActual' : timezone.now(),

                })
    sign_.plantilla_render=mensaje.render(c)
    mensaje=Template(sign_.plantilla_render)
    c = Context({
                'usuario': f'{user_.nombre_paciente} {user_.apellidos_paciente}',
                'centro': user_.centro.nombre_centro, 'localizacion_centro': user_.centro.localizacion,
                'nombre_comercial': footer.nombre_comercial, 'propietario': footer.propietario,
                'telefono': footer.telefono,
                'firma' : firm, 'sign_': sign_ ,
                'TelefonoUsuario':  user_.telefono_paciente,
                'EmailUsuario': user_.email,
                'dni': user_.dni,
                'poblacion': user_.poblacion,
                'direccion': user_.direccion,
                'FechaActual' : timezone.now(),

                })
    sign_.plantilla_render=mensaje.render(c)
    form=PrerenderForm(instance=sign_)
    if request.method == 'POST':
        form = PrerenderForm(request.POST, instance=sign_)
        if form.is_valid():
            sign = form.save(commit=False)
            sign.plantilla_doc = doc_
            sign.cliente=user_
            sign.save()
            return redirect("sing", pk=sign_.pk)
    else:
        form=PrerenderForm(instance=sign_)

    return render(request, "doc_prerender.html", {'form': form, 'footer': footer, 'doc': doc_, 'user_':user_ ,'firma': sign_.firma_imagen, 'sign': sign_})
@login_required(login_url='login')
def docs_sign_list(request, user=0):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
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
    return render(request, 'docs_list.html', {'footer': footer, 'docs': docs, 'form': form ,'notfound': notfound, 'cliente': user })

@login_required(login_url='login')
def suscripcion(request):
    footer=Configuracion.objects.all().last()
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    return render(request, 'suscripcion.html', {'footer': footer , 'suscription': suscription})
@login_required(login_url='login')
def doc_email(request, pk):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    doc=get_object_or_404(DocSings, pk=pk)
    cliente=doc.cliente
    mensaje=doc.plantilla_render
    mensaje=Template(mensaje)
    c = Context()
    mensaje=mensaje.render(c)
    subject = f'Tu documento de {doc.plantilla_doc.nombre_doc} de {footer.nombre_comercial}'
    template=mensaje
    html_message = render_to_string('blanc.html', {'mensaje': template, 'footer': footer})
    plain_message = strip_tags(html_message)
    from_email = f'Enviado por {footer.propietario}'
    to = cliente.email
    mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
    mail.send_mail(subject, plain_message, from_email, [footer.email_sistema], html_message=html_message)
    messages.success(request,f"Email Enviado a {cliente.email}")
    return redirect("cliente_details_citas", pk=doc.cliente.pk)

@login_required(login_url='login')
def stock_list(request):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    stocks=Stock.objects.all()
    page = request.GET.get('page', 1)
    #pagination
    paginator = Paginator(stocks, 10)
    try:
        cen = paginator.page(page)
    except PageNotAnInteger:
        cen = paginator.page(1)
    except EmptyPage:
        cen = paginator.page(paginator.num_pages)
    return render(request, 'stock_list.html', {'footer': footer, 'stocks':cen, 'cen': stock })

@login_required(login_url='login')
def stock(request, pk=0):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if pk!=0:
        stock=get_object_or_404(Stock, pk=pk)
        form=StockForm(instance=stock)
        if request.method == 'POST':
            form = StockForm(request.POST ,instance=stock)
            if form.is_valid():
                cantidad_retirar= form.cleaned_data['cantidad_retirar']
                if cantidad_retirar < 0:
                    messages.error(request,f'Ingrese una cantidad válida para retirar ')
                    return redirect("stock_list")
                stock.cantidad=stock.cantidad - cantidad_retirar
                stock.tecnica=request.user.tecnica
                form.save()
                messages.success(request,f'Se ha creado guardado el stock ')
                return redirect("stock_list")
        else:
            pass
    else:
        form=StockNewForm()
        if request.method == 'POST':
            form = StockNewForm(request.POST)
            if form.is_valid():
                form.tecnica=request.user.tecnica
                form.save()
                messages.success(request,f'Se ha creado guardado el stock ')
                return redirect("stock_list")
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()

    return render(request, 'stock.html', {'footer': footer,'form': form})

@login_required(login_url='login')
def caja_list(request, centro):
    footer=Configuracion.objects.all().last()
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
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
    return render(request, 'caja_list.html', {'footer': footer, 'cajas': cen, 'cen': cen })

@login_required(login_url='login')
def caja(request, pk):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
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
                        from_email = f'Enviado desde {footer.nombre_comercial}'
                        to = footer.email_nueva_caja
                        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
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
                        from_email = f'Enviado desde {footer.nombre_comercial}'
                        to = footer.email_nueva_caja
                        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

                    return redirect("caja_list", centro=pk)
    return render(request, 'caja.html', {'footer': footer,'form': form })

@login_required(login_url='login')
def estatisticas(request):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    clientes = Paciente.objects.raw('SELECT lima_paciente.id_paciente,COUNT(*) AS count, 	lima_paciente.fecha_alta as fecha_alta FROM 	lima_paciente WHERE 	YEAR(lima_paciente.fecha_alta)=YEAR(CURDATE()) GROUP BY WEEK(lima_paciente.fecha_alta)')
    tratamientos=Tratamientos.objects.raw('SELECT  lima_tratamientos.id_tratamiento, 	COUNT(*) AS count, 	lima_tratamientos.fecha as fecha FROM 	lima_tratamientos WHERE 	YEAR(lima_tratamientos.fecha)=YEAR(CURDATE()) GROUP BY WEEK(lima_tratamientos.fecha)')
    facturacion = Cajas.objects.raw('SELECT lima_cajas.id_caja, ROUND(SUM(cantidad_total),0) AS count, 	lima_cajas.fecha as fecha FROM 	lima_cajas WHERE 	YEAR(lima_cajas.fecha)=YEAR(CURDATE()) GROUP BY WEEK(lima_cajas.fecha)')
    citas = Lista.objects.raw('SELECT lima_lista.id_lista, COUNT(*) AS count, DATE(lima_lista.hora_inicio) FROM lima_lista WHERE YEAR(lima_lista.hora_inicio)=YEAR(CURDATE()) GROUP BY WEEK(lima_lista.hora_inicio)')
    tecnicas_horarios=ControlHorario.objects.raw(f'SELECT id, SUBSTRING_INDEX(CONCAT(SEC_TO_TIME(SUM(TIME_TO_SEC(trabajado)))), ":",1) AS count_tecnica, lima_tecnica.nombre_tecnica as nombre FROM lima_controlhorario INNER JOIN lima_tecnica ON lima_tecnica.id_tecnica=lima_controlhorario.tecnica_id WHERE MONTH(fecha)= MONTH(CURDATE()) AND YEAR(fecha)=YEAR(CURDATE())GROUP BY tecnica_id')
    #shearch form
    if request.user.is_staff:
        if request.method == "GET":
            form = EstadisticasAdminForm(request.GET)

            if form.is_valid():
                    fecha_inico= form.cleaned_data['fecha_inico']
                    fecha_fin= form.cleaned_data['fecha_fin']
                    centro= form.cleaned_data['centro']
                    tecnicas=form.cleaned_data['tecnicas']
                    clientes = Paciente.objects.raw(f'SELECT lima_paciente.id_paciente, COUNT(*) AS count, lima_paciente.fecha_alta FROM 	lima_paciente WHERE lima_paciente.fecha_alta BETWEEN  "{fecha_inico}" AND  "{fecha_fin}" AND centro_id = {centro.pk}  GROUP BY WEEK(lima_paciente.fecha_alta)')
                    tratamientos=Tratamientos.objects.raw(f'SELECT lima_tratamientos.id_tratamiento, COUNT(*) AS count, lima_tratamientos.fecha FROM 	lima_tratamientos WHERE lima_tratamientos.fecha BETWEEN  "{fecha_inico}" AND "{fecha_fin}" AND lima_tratamientos.tecnica_id = {tecnicas.pk} GROUP BY WEEK(lima_tratamientos.fecha)')
                    facturacion = Cajas.objects.raw(f'SELECT lima_cajas.id_caja, ROUND(SUM(cantidad_total),0) AS count, lima_cajas.fecha FROM 	lima_cajas WHERE lima_cajas.fecha BETWEEN "{fecha_inico}" AND "{fecha_fin}" AND centro_id = {centro.pk} AND tecnica_id = {tecnicas.pk} GROUP BY WEEK(lima_cajas.fecha)')
                    citas = Lista.objects.raw(f'SELECT lima_lista.id_lista, COUNT(*) AS count, DATE(lima_lista.hora_inicio) FROM lima_lista WHERE lima_lista.hora_inicio BETWEEN "{fecha_inico}" AND "{fecha_fin}" AND lima_lista.centro_id = {centro.pk} AND tecnica_id = {tecnicas.pk} GROUP BY WEEK(lima_lista.hora_inicio)')
                    tecnicas_horarios=ControlHorario.objects.raw(f'SELECT id, SUBSTRING_INDEX(CONCAT(SEC_TO_TIME(SUM(TIME_TO_SEC(trabajado)))), ":",1) AS count_tecnica, lima_tecnica.nombre_tecnica AS nombre FROM lima_controlhorario INNER JOIN lima_tecnica ON id_tecnica=lima_controlhorario.tecnica_id WHERE fecha  BETWEEN "{fecha_inico}" AND "{fecha_fin}"  AND tecnica_id = {tecnicas.pk} GROUP BY tecnica_id')
            else:
                form = EstadisticasAdminForm()
    else:
        if request.method == "GET":
            form = EstadisticasTecnicaForm(request.GET)

            if form.is_valid():
                    q= form.cleaned_data['shearch']
                    existe=Centro.objects.all().order_by('nombre_centro').filter(nombre_centro__icontains=q).filter(tecnica__id_tecnica=request.user.tecnica.id_tecnica).exists()
                    if existe==True:
                        centro=Centro.objects.all().order_by('nombre_centro').filter(nombre_centro__icontains=q).filter(tecnica__id_tecnica=request.user.tecnica.id_tecnica)
                    else:
                        notfound=True
                        print("no hay resultados")
            else:
                form = EstadisticasTecnicaForm()


    return render(request, 'estatisticas.html', {'footer': footer,'clientes': clientes, 'tratamientos': tratamientos,'facturacion': facturacion,'tecnicas_horarios':tecnicas_horarios,'form': form, 'citas': citas})

@login_required(login_url='login')
def estadisticas_horario_tecnica(request, pk=0):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    timeMonth=ControlHorario.objects.raw(f'SELECT id, CONCAT(SEC_TO_TIME( SUM(time_to_sec(trabajado))))  As count FROM lima_controlhorario WHERE tecnica_id ={pk} AND YEAR(fecha)=YEAR(CURDATE()) AND MONTH(fecha)=MONTH(CURDATE())   GROUP BY WEEK(fecha)')
    tiempo = ControlHorario.objects.raw(f'SELECT id, SUBSTRING_INDEX(CONCAT(SEC_TO_TIME(SUM(TIME_TO_SEC(trabajado)))), ":",1)  As count_time, fecha AS fecha FROM lima_controlhorario WHERE tecnica_id ={pk} AND YEAR(fecha)=YEAR(CURDATE())   GROUP BY WEEK(fecha)')
    if request.method == "GET":
            form = EstadisticasTecnicaForm(request.GET)

            if form.is_valid():
                    fecha_inico= form.cleaned_data['fecha_inico']
                    fecha_fin= form.cleaned_data['fecha_fin']
                    timeMonth=ControlHorario.objects.raw(f'SELECT id, CONCAT(SEC_TO_TIME( SUM(time_to_sec(trabajado))))  As count FROM lima_controlhorario WHERE tecnica_id ={pk} AND fecha BETWEEN "{fecha_inico}" AND "{fecha_fin}"    GROUP BY WEEK(fecha)')
                    tiempo = ControlHorario.objects.raw(f'SELECT id, SUBSTRING_INDEX(CONCAT(SEC_TO_TIME(SUM(TIME_TO_SEC(trabajado)))), ":",1)  As count_time, fecha AS fecha FROM lima_controlhorario WHERE tecnica_id ={pk} AND fecha BETWEEN "{fecha_inico}" AND "{fecha_fin}"   GROUP BY WEEK(fecha)')

            else:
                form = EstadisticasTecnicaForm()

    return render(request, 'estadistica_horario.html', {'footer': footer,'tiempo': tiempo,'timeMonth': timeMonth, 'form': form})

@login_required(login_url='login')
def listas(request, centro=0, pk=0):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
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
    return render(request, 'listas.html', {'footer': footer, 'lista': lista, 'lista_future': lista_future})

@login_required(login_url='login')
def edit_lista(request, paciente=0,pk=0):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    msg=footer.plantilla_email.plantilla
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
                flag=Lista.objects.raw(f"SELECT lima_lista.id_lista,COUNT(lima_lista.id_lista) AS flag FROM 	lima_lista WHERE lima_lista.hora_inicio BETWEEN '{lista.hora_inicio}' AND '{lista.hora_fin}' AND lima_lista.tecnica_id={lista.tecnica.id_tecnica}")
                if flag[0].flag>0:
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
                                    'Servicio': lista.servicios.nombre_servicio
                        })
                        mensaje=mensaje.render(c)
                        subject = f'Resguardo de cita con {footer.nombre_comercial}'
                        template=mensaje
                        html_message = render_to_string('blanc.html', {'mensaje': template, 'footer': footer})
                        plain_message = strip_tags(html_message)
                        from_email = f'Enviado por {footer.propietario}'
                        to = cliente.email
                        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
                        print(f"Email Enviado a {cliente.email} ")
                        messages.success(request,f'Email Enviado a {cliente.email} ')
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
                flag=Lista.objects.raw(f"SELECT lima_lista.id_lista, COUNT(*) AS flag FROM 	lima_lista WHERE lima_lista.hora_inicio BETWEEN '{lista.hora_inicio}' AND '{lista.hora_fin}' AND lima_lista.tecnica_id={lista.tecnica.id_tecnica}")
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
                                    'Servicio': lista.servicios.nombre_servicio
                        })
                        mensaje=mensaje.render(c)
                        subject = f'Resguardo de cita con {footer.nombre_comercial}'
                        template=mensaje
                        html_message = render_to_string('blanc.html', {'mensaje': template, 'footer': footer})
                        plain_message = strip_tags(html_message)
                        from_email = f'Enviado por {footer.propietario}'
                        to = cliente.email
                        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
                        print(f"Email Enviado a {cliente.email} ")
                        messages.success(request,f'Email Enviado a {cliente.email} ')
                    return redirect("cliente_details_citas", pk=lista.cliente.pk)

    return render(request, 'edit_lista.html', {'footer': footer, 'form': form })

@login_required(login_url='login')
def delete_lista(request, pk=0):
    list=get_object_or_404(Lista, pk=pk)
    lista=get_object_or_404(Lista, pk=pk).delete()
    return redirect("cliente_details_citas", pk=list.cliente.pk)

@login_required(login_url='login')
def lista_fotos(request, client):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    cls=get_object_or_404(Paciente, pk=client)
    fotos=ImagenesClientes.objects.all().filter(cliente=client).order_by('-fecha')
    return render(request, 'lista_fotos.html', {'footer': footer, 'cliente': cls, 'fotos': fotos })

@login_required(login_url='login')
def new_fotos(request, cliente):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    cls=get_object_or_404(Paciente, pk=cliente)
    form=FotoForm()
    if request.method == 'POST':
        form = FotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo=form.save(commit=False)
            photo.cliente=cls
            photo.tecnica=request.user.tecnica
            photo.save()
            messages.success(request,f'Se ha guardado la fotografia ')
            return redirect("lista_fotos", client=cls.pk)
    return render(request, 'new_fotos.html', {'footer': footer, 'form': form })

@login_required(login_url='login')
def delete_fotos(request,cliente, pk):
    foto=get_object_or_404(ImagenesClientes, pk=pk).delete()
    cls=get_object_or_404(Paciente, pk=cliente)
    return redirect("lista_fotos", client=cls.pk)


@login_required(login_url='login')
# Subscription Logic
def configuracion(request):
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    form=ConfigAdmin(instance=footer)
    if request.method == 'POST':
             form=ConfigAdmin(request.POST,instance=footer)
             if form.is_valid():
                 config = form.save(commit=False)
                 form.save()
                 messages.success(request,f'Se ha guardado la configuración')
                 return redirect("configuracion")
             else:
                 #messages.error(request,f'Ha sucedido el siguiente error {form.errors }')
                 pass
    return render(request, "configuración.html", {'form': form,'footer': footer,})

@login_required(login_url='login')
def map(request, centro):
    # Subscription Logic
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    cen_=get_object_or_404(Centro, pk=centro)
    return render(request, "centro_map.html", {'centro': cen_,'footer': footer})

@login_required(login_url='login')
def portales(request):
    # Subscription Logic
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    paneles=Paneles.objects.all().order_by('nombre_panel').filter(portales__id_tecnica=request.user.tecnica.id_tecnica)
    return render(request, "portales.html", {'footer': footer,'paneles':paneles})

@login_required(login_url='login')
def portales_details(request,pk):
    # Subscription Logic
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    panel=get_object_or_404(Paneles, pk=pk)
    estados=Estados.objects.all().order_by('orden_del_estado').filter(panel=panel)
    return render(request, "portal_details.html", {'footer': footer,'panel':panel, 'estados': estados})

@login_required(login_url='login')
def estados(request):
    # Subscription Logic
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    paneles=Paneles.objects.all().order_by('nombre_panel').filter(portales__id_tecnica=request.user.tecnica.id_tecnica)
    return render(request, "portales.html", {'footer': footer,'paneles':paneles})

@login_required(login_url='login')
def tarea_details(request, pk):
    # Subscription Logic
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    mensajes=Mensajes.objects.filter(tarea=pk)
    tarea=get_object_or_404(Tareas, id_tarea=pk)
    form=TareaForm(instance=tarea)
    formMensaje=MensajeForm()
    if request.method == 'POST':
        form = TareaForm(request.POST, instance=tarea)
        formMensaje=MensajeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,f'Se ha guardado la tarea')
            return redirect("tarea_details", pk=tarea.id_tarea)
        else:
            form = TareaForm()
        if formMensaje.is_valid():
            mensaje = formMensaje.save(commit=False)
            mensaje.enviado_por=request.user.tecnica
            mensaje.tarea=tarea
            formMensaje.save()
            messages.success(request,f'Se ha guardado el mensaje')
            return redirect("tarea_details", pk=tarea.id_tarea)
        else:
            formMensaje = MensajeForm()
    return render(request, "tarea_details.html", {'footer': footer,'mensajes':mensajes, 'tarea': tarea,'form': form,'formMensaje': formMensaje})

@login_required(login_url='login')
def new_tarea(request, pk):
    # Subscription Logic
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    if suscription.enddate<dt.datetime.now():
        messages.error(request,f'Su suscripción ha caducado el día {suscription.enddate}')
        return redirect("suscripcion")
    elif suscription.clinicas_max < Centro.objects.all().filter(habilitado=True).count():
        messages.error(request,f'Su suscripción ha excedido el número de clínicas por favor contrate un plan superior. Actualmente hace uso de {Centro.objects.all().filter(habilitado=True).count()} clínicas')
        return redirect("suscripcion")
    footer=Configuracion.objects.all().last()
    form=TareaForm()
    portal=get_object_or_404(Paneles, pk=pk)
    if request.method == 'POST':
        form = TareaForm(request.POST)
        if form.is_valid():
            tarea = form.save(commit=False)
            tarea.portal=portal
            form.save()
            messages.success(request,f'Se ha guardado la tarea')
            return redirect("portales_details", pk=portal.id_panel)
        else:
            form = TareaForm()
    return render(request, "new_tarea.html", {'footer': footer,'form': form})
