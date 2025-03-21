from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='dashboard/', permanent=True)),
    path('dashboard/', include('equipment.urls')),
    path('users/', include('users.urls')),
    path('parts/', include('parts.urls')),
    path('equipment/', include('equipment.urls')),
    path('docs/', include('documentation.urls')),
    path('search/', views.global_search, name='global-search'),  # Add the global search URL here
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)