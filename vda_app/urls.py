from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('arc.urls')),
    path('vda/', include('vda.urls')),
    path('vda/', include('clients.urls')),
    path('vda/', include('staff.urls')),
    path('vda/', include('tools.urls')),
    path('vda/', include('documents.urls')),
]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)