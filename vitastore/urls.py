from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('home.urls')),
    path('vitastore/admin/', include('site_admin.urls')),
    path('vitastore/admin/setup/', include('site_setup.urls')),
    path('catalog/', include('catalog.urls')),
    path('order/', include('order.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
