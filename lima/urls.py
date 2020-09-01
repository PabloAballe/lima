
#importamoss las vistas y las urls
from django.urls import path
from . import views



urlpatterns = [
    path('', views.admin, name='admin'),
]
