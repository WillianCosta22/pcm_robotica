from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('dashboard:index'), name='home'),
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),
    path('robots/', include('robots.urls', namespace='robots')),
    path('manutencoes/', include('manutencoes.urls', namespace='manutencoes')),
    path('tecnicos/', include('tecnicos.urls', namespace='tecnicos')),
    path('usuarios/', include('usuarios.urls', namespace='usuarios')),
    path('api/', include('robots.api_urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
