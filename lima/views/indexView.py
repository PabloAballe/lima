
# Create your views here.
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from ..models import *
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ..forms import *
import datetime as dt
from django.utils import timezone
from datetime import datetime
from django.contrib import messages
from ..filters import *
from django.contrib.sessions.models import Session

def get_current_users():
    active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    user_id_list = []
    for session in active_sessions:
        data = session.get_decoded()
        user_id_list.append(data.get('_auth_user_id', None))
    # Query all logged in users based on id list
    return User.objects.filter(id__in=user_id_list)

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
    perfiles= get_current_users()
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
     # determino si el centro está trabajando o no
    now=dt.datetime.now()
    return render(request, 'index.html',{'cen': cen, 'form': form ,'notfound': notfound ,'salida': salida, 'footer': footer,'cTime':now,'perfiles': perfiles})





def handler404(request, *args, **argv):
    response = render_to_response('errors/404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    response = render_to_response('errors/500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response