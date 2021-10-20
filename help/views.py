
# Create your views here.
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from lima.models import *
from django.contrib.auth.models import User
from lima.forms import *
from django.shortcuts import render, get_object_or_404
import datetime as dt
from django.http import HttpResponse
from django.template import Context, Template
from django.contrib import messages
from lima.filters import *
from django.contrib.auth.decorators import login_required
from .models import *


@login_required(login_url='login')
def academy(request):
    footer=Configuracion.objects.all().last()
    cat=HelpClases.objects.order_by('nombre_catogoria')
    #shearch artículo
    form=SheachForm()
    notfound=False
    if request.method == "GET":
        form = SheachForm(request.GET)
        if form.is_valid():
            q= form.cleaned_data['shearch']
            existe=HelpClases.objects.order_by('nombre_catogoria').filter(nombre_catogoria__icontains=q).exists()
            if existe==True:
                cat=HelpClases.objects.order_by('nombre_catogoria').filter(nombre_catogoria__icontains=q)
            else:
                notfound=True
                messages.error(request,f'No se han encontrado resultados para el termino de busqueda')
        else:
            form = SheachForm()
    return render(request, "academy_list.html", {'form': form, 'notfound': notfound, 'footer': footer,  'categorias': cat})
    #return HttpResponse("Bien")