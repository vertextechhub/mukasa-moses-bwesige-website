from django.contrib import admin
from django.urls import include, path
from django.contrib.sitemaps.views import sitemap

from content.sitemaps import StaticViewSitemap

urlpatterns = [
    path("admin/", admin.site.urls),
    path("sitemap.xml", sitemap, {"sitemaps": {"pages": StaticViewSitemap}}, name="sitemap"),
    path("", include("content.urls")),
]
