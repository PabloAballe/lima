
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..models import *
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from ..filters import *



@login_required(login_url='login')
def suscripcion(request):
    footer=Configuracion.objects.all().last()
    suscription=Suscription.objects.filter(type="S").latest('id_sicription')
    return render(request, 'suscription/suscripcion.html', {'footer': footer , 'suscription': suscription})