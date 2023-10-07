from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from configuration import settings

urlpatterns = [
    path('admin/', admin.site.urls),
]

if settings.SECURITY_LEVEL < 1:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
