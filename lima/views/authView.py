
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as do_logout
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as do_login
from ..models import *
from ..forms import *
from django.template import Context, Template
from django.conf import settings
from django.contrib import messages



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
    return render(request, "auth/login.html", {'form': form, 'footer': footer})
@login_required(login_url='login')
def logout(request):
    footer=Configuracion.objects.all().last()
    do_logout(request)
    messages.warning(request,f'Has cerrado sesión')
    return redirect('login')