from django.contrib import admin
from django.urls import path, include
from store import urls
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, documentroot = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, documentroot = settings.MEDIA_ROOT)