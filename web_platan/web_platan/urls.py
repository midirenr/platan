import django.contrib.auth
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('stands.urls')),
    path('', include('django.contrib.auth.urls')),

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL) + static(settings.IMAGES_URL, document_root=settings.IMAGES_URL)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
