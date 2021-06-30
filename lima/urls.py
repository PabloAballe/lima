
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
    path('edit_cita/<int:pk>/', views.edit_cita, name="edit_cita"),
    path('centro/<int:pk>/', views.centro_details, name='centro_details'),
    path('cliente/<int:pk>/', views.cliente_details, name='cliente_details'),
    path('edit/<int:pk>/', views.edit_centro, name='edit_centro'),
    path('edit_cliente/<int:pk>/', views.edit_cliente, name='edit_cliente'),
    path('delete/<int:pk>/', views.delete_centro, name='delete_centro'),
    path('delete_cliente/<int:pk>/', views.delete_cliente, name='delete_cliente'),
    path('delete_cita/<int:pk>/', views.delete_cita, name='delete_cita'),
    path('new_cliente/<int:pk>/', views.new_cliente, name="new_cliente"),
    path('clientes', views.clientes, name="clientes"),
    path('entrada', views.entrada, name="entrada"),
    path('salida', views.salida, name="salida"),
    path('perfil', views.perfil, name="perfil"),
    path('ver_horario/<int:pk>/', views.ver_horario, name="ver_horario"),
    path('ver_horario_visual/<int:pk>/', views.ver_horario_visual, name="ver_horario_visual"),
    path('ver_visual_tecnica/<int:pk>/', views.ver_visual_tecnica, name="ver_visual_tecnica"),
    path('view_perfiles', views.view_perfiles, name="view_perfiles"),
    path('send_emails', views.send_emails, name="send_emails"),
    path('new_tratamiento/<int:pk>/', views.new_tratamiento, name="new_tratamiento"),
    path('edit_tratamiento/<int:pk>/', views.edit_tratamiento, name="edit_tratamiento"),
    path('delete_tratamiento/<int:pk>/', views.delete_tratamiento, name='delete_tratamiento'),
    path('edit_turno/<int:pk>/', views.edit_turno, name="edit_turno"),
    path('emails_template/<int:pk>/', views.emails_template, name="emails_template"),
    path('emails_templates', views.emails_templates, name="emails_templates"),
    path('delete_email/<int:pk>/', views.delete_email, name="delete_email"),
    path('new_emails_template', views.new_emails_template, name="new_emails_template"),

]
