
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('website/', include('website.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('', include('lima.urls')),
    # path('website', include('website.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('faicon/', include('faicon.urls')),
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
    path("unicorn/", include("django_unicorn.urls")),
    path(r'^ckeditor/', include('ckeditor_uploader.urls')),


]



from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
