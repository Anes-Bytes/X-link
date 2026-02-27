from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from django.contrib import admin
from core.seo_views import robots_txt_view, sitemap_xml_view

# Admin site configuration
admin.site.site_header = "پنل مدیریت X-Link"
admin.site.site_title = "مدیریت X-Link"
admin.site.index_title = "داشبورد مدیریت"

urlpatterns = [
    path('admin/', admin.site.urls),
    path("robots.txt", robots_txt_view, name="robots_txt"),
    path("sitemap.xml", sitemap_xml_view, name="sitemap_xml"),
    path('', include('core.urls')),
    path('', include('Billing.urls')),
    path('', include('cards.urls')),
    path('', include('shop.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
