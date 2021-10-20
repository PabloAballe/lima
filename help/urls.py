#importamoss las vistas y las urls
from django.urls import path
from . import views
import django


urlpatterns = [
    ### academy
    path('', views.academy, name='academy'),
]