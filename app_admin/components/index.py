from django_unicorn.components import UnicornView

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from lima.models import *
from lima.forms import *
from django.contrib import messages
from lima.filters import *


class IndexView(UnicornView):

    centros: Centro = None

    def mount(self):
      self.centros = Centro.objects.all().order_by('nombre_centro')
