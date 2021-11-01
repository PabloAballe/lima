#importamoss las vistas y las urls
from django.urls import path
from . import views
import django


urlpatterns = [
    ### index
    path('', views.app_admin_index, name='app_admin_index'),
]