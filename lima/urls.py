
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
    path('new_tratamiento/<int:pk>/', views.new_tratamiento, name="new_tratamiento"),
    path('edit_tratamiento/<int:pk>/', views.edit_tratamiento, name="edit_tratamiento"),
    path('delete_tratamiento/<int:pk>/', views.delete_tratamiento, name='delete_tratamiento'),
    path('edit_turno/<int:pk>/', views.edit_turno, name="edit_turno"),
    #emails
    path('send_emails', views.send_emails, name="send_emails"),
    path('emails_template/<int:pk>/', views.emails_template, name="emails_template"),
    path('emails_templates', views.emails_templates, name="emails_templates"),
    path('delete_email/<int:pk>/', views.delete_email, name="delete_email"),
    path('new_emails_template', views.new_emails_template, name="new_emails_template"),
    #documentos
    path('docs_template/<int:pk>/', views.docs_template, name="docs_template"),
    path('docs_list', views.docs_list, name="docs_list"),
    path('delete_doc/<int:pk>/', views.delete_doc, name="delete_doc"),
    path('new_doc_template', views.new_doc_template, name="new_doc_template"),
    path('docs_sign_list/<int:user>/', views.docs_sign_list, name="docs_sign_list"),
    path('doc_prerender/<int:user>/<int:doc>/', views.doc_prerender, name="doc_prerender"),
    path('doc_prerender/<int:pk>/', views.doc_prerender, name="doc_prerender"),
    path('sing/<int:pk>/', views.sing, name="sing"),
    path('suscripcion', views.suscripcion, name="suscripcion"),
    path('doc_email/<int:pk>/', views.doc_email, name="doc_email"),
    #stock
    path('stock_list', views.stock_list, name="stock_list"),
    path('stock/<int:pk>/', views.stock, name="stock"),
    #caja
    path('caja_list/<int:centro>/', views.caja_list, name="caja_list"),
    path('caja/<int:pk>/', views.caja, name="caja"),
    #estadisticas
    path('estatisticas', views.estatisticas, name="estatisticas"),
    path('estadisticas_horario_tecnica/<int:pk>/', views.estadisticas_horario_tecnica, name="estadisticas_horario_tecnica"),
    #listas
    path('listas/<int:centro>/<int:pk>/', views.listas, name="listas"),
    path('edit_lista/<int:pk>/<int:paciente>/', views.edit_lista, name="edit_lista"),
    path('delete_lista/<int:pk>/', views.delete_lista, name="delete_lista"),
    #fotografias de clientes
    path('lista_fotos/<int:client>', views.lista_fotos, name="lista_fotos"),
    path('new_fotos/<int:cliente>/', views.new_fotos, name="new_fotos"),
    path('delete_fotos/<int:cliente>/<int:pk>/', views.delete_fotos, name="delete_fotos"),
    #configuración del sistema
    path('configuracion', views.configuracion, name="configuracion"),
    ### mapa
    path('map/<int:centro>/', views.map, name="map"),
    ### portales
    path('portales', views.portales, name="portales"),
    path('portal/<int:pk>', views.portales_details, name="portales_details"),
    #clientes
    path('cliente/<int:pk>/citas', views.cliente_details_citas, name='cliente_details_citas'),
    path('cliente/<int:pk>/tratamientos', views.cliente_details_tratamientos, name='cliente_details_tratamientos'),
    path('cliente/<int:pk>/zonas', views.cliente_details_zonas, name='cliente_details_zonas'),
     ### tareas
    path('tarea/<int:pk>', views.tarea_details, name="tarea_details"),
    path('new_tarea/<int:pk>/', views.new_tarea, name="new_tarea"),
]
