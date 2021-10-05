from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
# Create your views here.


def config_website(request):
    conf=ConfiguracionWEB.objects.all().last()
    form=ConfigWebAdmin(instance=conf)
    if request.method == 'POST':
             form=ConfigWebAdmin(request.POST, request.FILES,instance=conf)
             if form.is_valid():
                 config = form.save(commit=False)
                 form.save()
                 messages.success(request,f'Se ha guardado la configuración')
                 return redirect("config_website")
             else:
                 #messages.error(request,f'Ha sucedido el siguiente error {form.errors }')
                 pass
    return render(request, "webConfig.html", {'form': form,})

def website_index(request):
    conf=ConfiguracionWEB.objects.all().last()
    page=Pages.objects.filter(pertenece_a="I")
    nav=Pages.objects.filter(pertenece_a="O")
    return render(request, "web_index.html", {'page': page, 'web': conf, 'nav': nav})

def website_blog_list(request):
    conf=ConfiguracionWEB.objects.all().last()
    page=Pages.objects.filter(pertenece_a="B")
    nav=Pages.objects.filter(pertenece_a="O")
    posts=Blog.objects.order_by('-creado_el')
    return render(request, "blogList.html", {'page': page, 'web': conf,'posts': posts, 'nav': nav})

def website_blog_details(request,slug):
    conf=ConfiguracionWEB.objects.all().last()
    nav=Pages.objects.filter(pertenece_a="O")
    post=get_object_or_404(Blog, slug_post=slug)
    return render(request, "blogDetails.html", {'web': conf,'post': post, 'nav': nav})

def website_contact(request):
    conf=ConfiguracionWEB.objects.all().last()
    page=Pages.objects.filter(pertenece_a="C")
    nav=Pages.objects.filter(pertenece_a="O")
    form=ContactForm(instance=conf)
    if request.method == 'POST':
         form=ContactForm(request.POST)
         if form.is_valid():
             form = form.save(commit=False)
             form.save()
             messages.success(request,f'Se ha enviado el mensaje')
             return redirect("website_index")
         else:
             #messages.error(request,f'Ha sucedido el siguiente error {form.errors }')
             pass
    return render(request, "contact.html", {'page': page,'web': conf, 'form': form, 'nav': nav})

def website_page(request, slug):
    conf=ConfiguracionWEB.objects.all().last()
    nav=Pages.objects.filter(pertenece_a="O")
    page=get_object_or_404(Pages, slug_pagina=slug)
    return render(request, "web_index.html", {'web': conf,'page': page, 'nav': nav})