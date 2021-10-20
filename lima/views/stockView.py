
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login as do_login
from django.contrib.auth.decorators import login_required
from ..models import *
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ..forms import *
from django.shortcuts import render, get_object_or_404
from itertools import chain
import datetime as dt
from django.utils import timezone, dateformat
from django.http import HttpResponse
from django.template import Context, Template
from django.conf import settings
from datetime import datetime
from django.template.loader import get_template
from django.contrib import messages
from ..filters import *


def stock_list(request):
    footer=Configuracion.objects.all().last()
    st=Stock.objects.all().order_by('nombre_stock')
    #pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(st, 10)
    try:
        cen = paginator.page(page)
    except PageNotAnInteger:
        cen = paginator.page(1)
    except EmptyPage:
        cen = paginator.page(paginator.num_pages)
    return render(request, 'stock/stock_list.html', {'footer': footer, 'stocks':cen, 'cen': st })


def stock(request, pk=0):
    footer=Configuracion.objects.all().last()
    form=StockForm()
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

    return render(request, 'stock/stock.html', {'footer': footer,'form': form})