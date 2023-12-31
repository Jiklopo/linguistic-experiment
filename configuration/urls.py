from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from configuration import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('experiments/', include('apps.experiments.urls')),
    path('', RedirectView.as_view(url='admin/')),
]

if settings.SECURITY_LEVEL < 1:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
