
#importamoss las vistas y las urls
from django.urls import path
from . import views
from django.conf.urls import (
handler400, handler403, handler404, handler500
)




urlpatterns = [
     path('', views.index_dashboard, name='index'),
]
