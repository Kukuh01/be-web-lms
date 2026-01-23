from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings
from .api import api


# Daftar URL utama pada proyek Django
urlpatterns = [
    # URL untuk dashboard admin Django
    path('admin/', admin.site.urls),

    # URL utama untuk REST API backend
    path('api/', api.urls),

    # URL untuk Django Silk (monitoring & profiling performa)
    path('silk/', include('silk.urls', namespace='silk')),
]


# Konfigurasi tambahan yang hanya aktif saat mode DEBUG (development)
if settings.DEBUG:
    # Import Django Debug Toolbar hanya saat development
    import debug_toolbar

    # URL untuk mengakses Debug Toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]

    # Menyajikan file media (upload user) saat development
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
