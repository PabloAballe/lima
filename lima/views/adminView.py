
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ..forms import *
from django.shortcuts import render, get_object_or_404
import datetime as dt
from django.utils import timezone, dateformat
from django.http import HttpResponse
from django.conf import settings
from django.contrib import messages



@login_required(login_url='login')
def admin(request):
    return redirect("admin/")