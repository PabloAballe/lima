
#importamoss las vistas y las urls
from django.urls import path
from . import views



urlpatterns = [
    path('admin', views.admin, name='admin'),
    path('', views.index, name="index"),
    path('login', views.login, name="login"),
    path('historial', views.historial, name="historial"),
    path('logout', views.logout, name="logout"),
    path('new_centro', views.new_centro, name="new_centro"),
    path('new_cita/<int:pk>/', views.new_cita, name="new_cita"),
    path('centro/<int:pk>/', views.centro_details, name='centro_details'),
    path('cliente/<int:pk>/', views.cliente_details, name='cliente_details'),
    path('edit/<int:pk>/', views.edit_centro, name='edit_centro'),
    path('edit_cliente/<int:pk>/', views.edit_cliente, name='edit_cliente'),
    path('edit_cita/<int:pk>/', views.edit_cita, name='edit_cita'),
    path('delete/<int:pk>/', views.delete_centro, name='delete_centro'),
    path('delete_cliente/<int:pk>/', views.delete_cliente, name='delete_cliente'),
    path('delete_cita/<int:pk>/', views.delete_cita, name='delete_cita'),
    path('new_cliente/<int:pk>/', views.new_cliente, name="new_cliente"),
    path('clientes', views.clientes, name="clientes"),
    path('entrada', views.entrada, name="entrada"),
    path('salida', views.salida, name="salida"),
    path('perfil', views.perfil, name="perfil"),
]
