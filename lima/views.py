
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
from django.utils import timezone
from django.db.models import Sum
from django.db.models import Count
from django.core import serializers
from django.http import JsonResponse
from django.forms.models import model_to_dict

@login_required(login_url='login')
def admin(request):
    return redirect("admin/")

@login_required(login_url='login')
def index(request):

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
    return render(request, 'index.html',{'cen': cen, 'form': form ,'notfound': notfound ,'salida': salida})

def login(request):
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
    return render(request, "login.html", {'form': form})
@login_required(login_url='login')
def logout(request):
    do_logout(request)
    return redirect('login')
@login_required(login_url='login')
def centro_details(request, pk):
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

    return render(request, "centro_details.html", {'centro': centro, 'cliente': cliente, 'cen': cen, 'form': form, 'notfound': notfound})
@login_required(login_url='login')
def clientes(request):
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
    context={'cliente': cliente, 'form': form, 'notfound': notfound}
    return render (request, 'table_clientes_total.html', context)
@login_required(login_url='login')
def cliente_details(request, pk):
    cliente=get_object_or_404(Paciente, pk=pk)
    cita=Cita.objects.all().order_by("-fecha").filter(paciente=cliente)
    return render(request, "cliente_details.html", {'cliente': cliente, 'cita': cita})
@login_required(login_url='login')
def new_centro(request):
    form=CentroForm()
    if request.method == 'POST':
        form = CentroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = CentroForm()

    return render(request, "new_centro.html", {'form': form})
@login_required(login_url='login')
def new_cliente(request, pk):
    centro1=get_object_or_404(Centro, id_centro=pk)
    form=ClienteForm()
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.centro=centro1
            form.save()
            return redirect("centro_details", pk=centro1.id_centro)
    else:
        form = ClienteForm()

    return render(request, "new_cliente.html", {'form': form})

@login_required(login_url='login')
def new_cita(request, pk):
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
    
    return render(request, "new_cita.html", {'form': form})

@login_required(login_url='login')
def edit_cita(request, pk):
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
    
    return render(request, "edit_cita.html", {'form': form})

@login_required(login_url='login')
def edit_centro(request, pk):
    post = get_object_or_404(Centro, pk=pk)
    if request.method == "POST":
        form = CentroForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('index')
    else:
        form = CentroForm(instance=post)
    return render(request, 'edit_centro.html', {'form': form})
@login_required(login_url='login')
def edit_cliente(request, pk):
    cliente = get_object_or_404(Paciente, pk=pk)
    if request.method == "POST":
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect("centro_details", pk=cliente.centro.id_centro)
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'edit_cliente.html', {'form': form})
@login_required(login_url='login')
def edit_cita(request, pk):
    cita = get_object_or_404(Cita, id_cita=pk)
    if request.method == "POST":
        form = CitaForm(request.POST, instance=cita)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect("cliente_details", pk=cita.paciente.id_paciente)
    else:
        form = CitaForm(instance=cita)
    return render(request, 'edit_cita.html', {'form': form})
@login_required(login_url='login')
def historial(request):
    historial_centro=Centro.history.all()[:100]
    historial_paciente=Paciente.history.all()[:100]
    historial_tecnica=Tecnica.history.all()[:100]
    historial_cita=Cita.history.all()[:100]
    historial_controlhorario=ControlHorario.history.all()[:100]
    historial_total=list(chain(historial_centro,historial_paciente,historial_tecnica,historial_cita, historial_controlhorario))
    return render(request, 'history.html', {'historial_centro': historial_total})
@login_required(login_url='login')
def delete_centro(request, pk):
    centro=get_object_or_404(Centro, pk=pk).delete()
    return redirect("index")
@login_required(login_url='login')
def delete_cliente(request, pk):
    cliente1=get_object_or_404(Paciente, pk=pk)
    cliente=get_object_or_404(Paciente, pk=pk).delete()
    return redirect("centro_details", pk=cliente1.centro.id_centro)
@login_required(login_url='login')
def delete_cita(request, pk):
    cita1=get_object_or_404(Cita, pk=pk)
    cita=get_object_or_404(Cita, pk=pk).delete()
    return redirect("cliente_details", pk=cita1.paciente.id_paciente)
@login_required(login_url='login')
def entrada(request):
    user=request.user
    entrada=ControlHorario(tecnica=request.user.tecnica, fecha=datetime.date.today(), entrada=timezone.now())
    entrada.save()
    return redirect("index")
@login_required(login_url='login')
def salida(request):
    user=request.user
    salida=ControlHorario.objects.filter(tecnica=user.tecnica, salida=None).last()
    salida.salida=timezone.now()
    salida.save()
    return redirect("index")
@login_required(login_url='login')
def perfil(request):
    user=request.user
    meses=ControlHorario.objects.filter(tecnica=user.tecnica).order_by("-fecha", "-entrada")[:90]
    #checkea si ha enytrado o salido
    user=request.user
    horario=ControlHorario.objects.filter(tecnica=user.tecnica).last()
    salida=False
    if horario:
        if horario.salida is None:
            salida=True
    else:
        salida=False
    return render(request, 'perfil.html', {'meses': meses, 'salida': salida })

@login_required(login_url='login')
def view_perfiles(request):
    tecnica= Tecnica.objects.all().order_by("-nombre_tecnica")
    #shearch cliente
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
    return render(request, 'view_perfiles.html', { 'tecnica': tecnica })

@login_required(login_url='login')
def ver_horario(request, pk):
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
    return render(request, 'perfil_horario.html', {'meses': meses, 'salida': salida, 'tecnica': tecnica })



@login_required(login_url='login')
def ver_horario_visual(request, pk):
    today = date.today()
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
    return render(request, 'calendar_horario.html', {'meses': meses, 'salida': salida, 'tecnica': tecnica , 'today': today})

@login_required(login_url='login')
def ver_visual_tecnica(request, pk):
    today = date.today()
    salida=False
    #checkea si ha enytrado o salido
    tecnica=get_object_or_404(Tecnica, pk=pk)
    meses=Cita.objects.filter(tecnica=tecnica).order_by("-fecha")[:100]
    horario=ControlHorario.objects.filter(tecnica=tecnica).last()
    if horario:
        if horario.salida is None:
            salida=True
    else:
        salida=False
    return render(request, 'ver_visual_tecnica.html', {'meses': meses, 'salida': salida, 'tecnica': tecnica , 'today': today})