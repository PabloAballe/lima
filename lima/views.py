
# Create your views here.
from django.shortcuts import render, redirect

from django.core.mail import send_mail

def admin(request):
    return redirect("admin/")
