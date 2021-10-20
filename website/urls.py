
#importamoss las vistas y las urls
from django.urls import path
from . import views


urlpatterns = [
    path('config', views.config_website, name='config_website'),
    path('', views.website_index, name='website_index'),
    path('blog', views.website_blog_list, name='website_blog_list'),
    path('blog/<slug:slug>/', views.website_blog_details, name='website_blog_details'),
    path('page/<slug:slug>/', views.website_page, name='website_page'),
    path('contact', views.website_contact, name='website_contact'),
    path('appointment/<int:centro>94840<int:cliente>042f02cf<int:tecnica>29d55a', views.website_appointment, name='website_appointment'),
    path('pdf/<int:cita>/', views.website_pdf, name='website_pdf'),
]
