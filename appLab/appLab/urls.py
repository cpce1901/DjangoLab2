from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.attendance.urls')),
    path('', include('apps.core.urls'))
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    


# Nombre Admin
admin.site.site_title = "Panel de control Personal"
admin.site.site_header = "Personal"
admin.site.index_title = "Panel de control Personal"