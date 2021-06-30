
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
import datetime
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

@login_required(login_url='login')
def admin(request):
    return redirect("admin/")

@login_required(login_url='login')
def index(request):
    footer=Configuracion.objects.all().last()
    centro=Centro.objects.all().order_by('nombre_centro')
    notfound=False
    #shearch centro
    if request.method == "GET":
        form = SheachForm(request.GET)

    if form.is_valid():
            q= form.cleaned_data['shearch']
            existe=Centro.objects.all().order_by('nombre_centro').filter(nombre_centro__icontains=q).exists()
            if existe==True:
                centro=Centro.objects.all().order_by('nombre_centro').filter(nombre_centro__icontains=q)
            else:
                notfound=True
                print("no hay resultados")
    else:
        form = SheachForm()

    #pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(centro, 10)
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
    return render(request, 'index.html',{'cen': cen, 'form': form ,'notfound': notfound ,'salida': salida, 'footer': footer})

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
                # Y le redireccionamos a la portada
                return redirect('/')

    # Si llegamos al final renderizamos el formulario
    return render(request, "login.html", {'form': form, 'footer': footer})
@login_required(login_url='login')
def logout(request):
    footer=Configuracion.objects.all().last()
    do_logout(request)
    return redirect('login')
@login_required(login_url='login')
def centro_details(request, pk):
    footer=Configuracion.objects.all().last()
    centro=get_object_or_404(Centro, id_centro=pk)
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

    return render(request, "centro_details.html", {'centro': centro, 'cliente': cen, 'cen': cen, 'form': form, 'notfound': notfound, 'footer': footer})
@login_required(login_url='login')
def clientes(request):
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
def cliente_details(request, pk):
    footer=Configuracion.objects.all().last()
    cliente1=get_object_or_404(Paciente, pk=pk)
    cita=Cita.objects.all().order_by("fecha").filter(paciente=cliente1)
    tratamientos=Tratamientos.objects.all().order_by("fecha").filter(cliente=cliente1)
    return render(request, "cliente_details.html", {'cliente': cliente1, 'cita': cita, 'footer': footer, 'tratamientos': tratamientos})
@login_required(login_url='login')
def new_centro(request):
    footer=Configuracion.objects.all().last()
    form=CentroForm()
    if request.method == 'POST':
        form = CentroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = CentroForm()

    return render(request, "new_centro.html", {'form': form, 'footer': footer})
@login_required(login_url='login')
def new_cliente(request, pk):
    footer=Configuracion.objects.all().last()
    centro1=get_object_or_404(Centro, id_centro=pk)
    form=ClienteForm()
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.centro=centro1
            form.save()
            if footer.email_nuevos_clientes and footer.plantilla_email:
                subject = f'Bienvenido a {footer.nombre_comercial}'
                html_message = render_to_string('blanc.html', {'mensaje': footer.plantilla_email.plantilla, 'footer': footer})
                plain_message = strip_tags(html_message)
                from_email = f'Enviado por {footer.propietario}'
                to = cliente.email
                mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
                print(f"Email Enviado a {cliente.email}")
            return redirect("centro_details", pk=centro1.id_centro)
    else:
        form = ClienteForm()

    return render(request, "new_cliente.html", {'form': form, 'footer': footer})

@login_required(login_url='login')
def new_cita(request, pk):
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
                 return redirect("cliente_details", pk=cliente1.id_paciente)
             else:
                 print(f"Ha sucedido el siguiennte error {form.errors }")
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
                 return redirect("cliente_details", pk=cliente1.id_paciente)
             else:
                print(f"Ha sucedido el siguiennte error {form.errors }")
                form = CitaForm()

    return render(request, "new_cita.html", {'form': form, 'footer': footer})

@login_required(login_url='login')
def edit_cita(request, pk):
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
                 return redirect("cliente_details", pk=cliente1.id_paciente)
             else:
                 print(f"Ha sucedido el siguiennte error {form.errors }")
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
                 return redirect("cliente_details", pk=cliente1.id_paciente)
             else:
                print(f"Ha sucedido el siguiennte error {form.errors }")
                form = CitaForm()

    return render(request, "edit_cita.html", {'form': form, 'footer': footer})
@login_required(login_url='login')
def new_tratamiento(request, pk):
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
                 return redirect("cliente_details", pk=cliente1.id_paciente)
             else:
                 print(f"Ha sucedido el siguiente error {form.errors }")

    else:
         form=TratamientoForm()
         if request.method == 'POST':
             form = TratamientoForm(request.POST)
             if form.is_valid():
                 cita = form.save(commit=False)
                 cita.cliente=cliente1
                 cita.tecnica=request.user.tecnica
                 form.save()
                 return redirect("cliente_details", pk=cliente1.id_paciente)
             else:
                print(f"Ha sucedido el siguiente error {form.errors }")

    return render(request, "new_tratamiento.html", {'form': form, 'footer': footer})

@login_required(login_url='login')
def edit_tratamiento(request, pk):
    footer=Configuracion.objects.all().last()
    tratamiento=get_object_or_404(Tratamientos, pk=pk)
    cliente1=get_object_or_404(Paciente, pk=pk)
    if request.user.is_staff:
         form=TratamientoFormAdmin(instance=tratamiento)
         if request.method == 'POST':
             form = TratamientoFormAdmin(request.POST, instance=tratamiento)
             if form.is_valid():
                 cita = form.save(commit=False)
                 cita.cliente=cliente1
                 form.save()
                 return redirect("cliente_details", pk=cliente1.id_paciente)
             else:
                 print(f"Ha sucedido el siguiennte error {form.errors }")
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
                 return redirect("cliente_details", pk=cliente1.id_paciente)
             else:
                print(f"Ha sucedido el siguiennte error {form.errors }")


    return render(request, "edit_tratamiento.html", {'form': form, 'footer': footer})

@login_required(login_url='login')
def edit_centro(request, pk):
    footer=Configuracion.objects.all().last()
    post = get_object_or_404(Centro, pk=pk)
    if request.method == "POST":
        form = CentroForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('index')
    else:
        form = CentroForm(instance=post)
    return render(request, 'edit_centro.html', {'form': form, 'footer': footer})
@login_required(login_url='login')
def edit_cliente(request, pk):
    footer=Configuracion.objects.all().last()
    cliente = get_object_or_404(Paciente, pk=pk)
    if request.method == "POST":
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect("cliente_details", pk=cliente.id_paciente)
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'edit_cliente.html', {'form': form, 'footer': footer})
@login_required(login_url='login')
def edit_cita(request, pk):
    footer=Configuracion.objects.all().last()
    cita = get_object_or_404(Cita, id_cita=pk)
    if request.method == "POST":
        form = CitaForm(request.POST, instance=cita)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect("cliente_details", pk=cita.paciente.id_paciente)
    else:
        form = CitaForm(instance=cita)
    return render(request, 'edit_cita.html', {'form': form, 'footer': footer})
@login_required(login_url='login')
def historial(request):
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
    footer=Configuracion.objects.all().last()
    centro=get_object_or_404(Centro, pk=pk).delete()
    return redirect("index")
@login_required(login_url='login')
def delete_cliente(request, pk):
    footer=Configuracion.objects.all().last()
    cliente1=get_object_or_404(Paciente, pk=pk)
    cliente=get_object_or_404(Paciente, pk=pk).delete()
    return redirect("centro_details", pk=cliente1.centro.id_centro)
@login_required(login_url='login')
def delete_cita(request, pk):
    footer=Configuracion.objects.all().last()
    cita1=get_object_or_404(Cita, pk=pk)
    cita=get_object_or_404(Cita, pk=pk).delete()
    return redirect("cliente_details", pk=cita1.paciente.id_paciente)
@login_required(login_url='login')
def delete_tratamiento(request, pk):
    footer=Configuracion.objects.all().last()
    tratamiento=get_object_or_404(Tratamientos, pk=pk).delete()
    return redirect("cliente_details", pk=tratamiento.paciente.id_paciente)
@login_required(login_url='login')
def entrada(request):
    footer=Configuracion.objects.all().last()
    user=request.user
    entrada=ControlHorario(tecnica=request.user.tecnica, fecha=datetime.date.today(), entrada=timezone.now().time())
    entrada.save()
    return redirect("index")
@login_required(login_url='login')
def salida(request):
    footer=Configuracion.objects.all().last()
    user=request.user
    salida=ControlHorario.objects.filter(tecnica=user.tecnica, salida=None).last()
    salida.salida=timezone.now().time()
    salida.save()
    return redirect("index")
@login_required(login_url='login')
def perfil(request):
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
    footer=Configuracion.objects.all().last()
    today = date.today()
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
    footer=Configuracion.objects.all().last()
    today = date.today()
    salida=False
    #checkea si ha enytrado o salido
    tecnica=get_object_or_404(Tecnica, pk=pk)
    tratamientos=Tratamientos.objects.filter(tecnica=tecnica).order_by("-fecha")
    citas=Cita.objects.filter(tecnica=tecnica).order_by("-fecha")
    horario=ControlHorario.objects.filter(tecnica=tecnica).last()
    meses = list(chain(citas, tratamientos))
    if horario:
        if horario.salida is None:
            salida=True
    else:
        salida=False
    return render(request, 'ver_visual_tecnica.html', {'meses': meses, 'salida': salida, 'tecnica': tecnica , 'today': today, 'footer': footer})


@login_required(login_url='login')
def send_emails(request):
    footer=Configuracion.objects.all().last()
    users=Paciente.objects.exclude(email='')
    form=EmailForm()
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            asunto=form.cleaned_data["asunto"]
            destinatario=form.cleaned_data["destinatario"]
            #emails=form.cleaned_data.get["emails"]
            mensaje=form.cleaned_data["plantilla"].plantilla
            for users in form.cleaned_data['emails']:
                # send_mail(
                # asunto,
                # SafeString(mensaje),
                # destinatario,
                # [users.email],
                # fail_silently=False,
                # )
                subject = asunto
                html_message = render_to_string('blanc.html', {'mensaje': mensaje, 'footer': footer})
                plain_message = strip_tags(html_message)
                from_email = f'Enviado por {destinatario}'
                to = users.email
                mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
                print(f"Email Enviado a {users.email}")

            return redirect("index")
        else:
           HttpResponse(f"Ha sucedido el siguiennte error {form.errors }")
           #form = EmailForm()

    return render(request, "send_emails.html", {'form': form, 'footer': footer})
@login_required(login_url='login')
def edit_turno(request, pk):
    footer=Configuracion.objects.all().last()
    today = date.today()
    salida=False
    if pk !=0:
        tecnica=get_object_or_404(Tecnica, pk=pk)
        meses=Turnos.objects.filter(tecnica=tecnica).order_by("-turno")[:90]
    else:
        tecnica =request.user.tecnica
        meses=Turnos.objects.all().order_by("-turno")[:90]

    horario=ControlHorario.objects.filter(tecnica=tecnica).last()
    if horario:
        if horario.salida is None:
            salida=True
    else:
        salida=False
    return render(request, 'edit_turno.html', {'meses': meses, 'salida': salida, 'tecnica': tecnica , 'today': today, 'footer': footer})
@login_required(login_url='login')
def emails_templates(request):
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
    footer=Configuracion.objects.all().last()
    email=get_object_or_404(EmailTemplates, pk=pk)
    form = EmailTemplateEditForm( instance=email)
    if request.method == 'POST':
        form = EmailTemplateEditForm(request.POST, instance=email)
        if form.is_valid():
            cita = form.save(commit=False)
            form.save()
            return redirect("emails_templates")
        else:
           print(f"Ha sucedido el siguiennte error {form.errors }")
    return render(request, 'emails_template.html', {'footer': footer, 'form': form })

@login_required(login_url='login')
def new_emails_template(request):
    footer=Configuracion.objects.all().last()
    form=EmailTemplateNewForm()
    if request.method == 'POST':
        form = EmailTemplateNewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("emails_templates")
    else:
        #form = EmailTemplateNewForm()
        print(f"Ha sucedido el siguiennte error {form.errors }")
    return render(request, 'new_email_templates.html', {'footer': footer, 'form': form})

@login_required(login_url='login')
def delete_email(request, pk):
    footer=Configuracion.objects.all().last()
    email=get_object_or_404(EmailTemplates, pk=pk).delete()
    return redirect("emails_templates")


