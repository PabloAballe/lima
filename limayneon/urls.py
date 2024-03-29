from django.contrib import admin
from django.urls import path, include
import debug_toolbar

handler404 = 'lima.views.handler404'
handler500 = 'lima.views.handler500'

urlpatterns = [
    path('website/', include('website.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('', include('lima.urls')),
    path('faicon/', include('faicon.urls')),
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
    path(r'^__debug__/', include(debug_toolbar.urls)),
    path('help', include('help.urls')),
]



from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)