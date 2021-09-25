
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('summernote/', include('django_summernote.urls')),
    path('admin/', admin.site.urls),
    path('', include('lima.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('faicon/', include('faicon.urls')),
]

from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
