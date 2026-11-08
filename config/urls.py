from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
admin.site.site_header = "Al-Shifa Modern Hospital"
urlpatterns = [path("admin/", admin.site.urls), path("", include("hospital.urls"))]
admin.site.site_title = "Al-Shifa Admin"
admin.site.index_title = "Hospital Management"
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
