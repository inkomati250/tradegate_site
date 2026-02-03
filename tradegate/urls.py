from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path
from django.contrib.sitemaps.views import sitemap

from website.sitemaps import StaticViewSitemap, LegalPageSitemap

sitemaps = {
    "static": StaticViewSitemap,
    "legal": LegalPageSitemap,
}


def robots_txt(request):
    """
    Basic robots.txt that:
    - Allows normal crawling
    - Discourages indexing admin
    - Points to sitemap.xml
    """
    sitemap_url = request.build_absolute_uri("/sitemap.xml")

    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        f"Sitemap: {sitemap_url}",
    ]
    return HttpResponse("\n".join(lines) + "\n", content_type="text/plain")


def healthcheck(request):
    """
    Very small health endpoint for monitoring.
    """
    return HttpResponse("ok\n", content_type="text/plain")


urlpatterns = [
    path("admin/", admin.site.urls),

    # SEO + indexing
    path("robots.txt", robots_txt, name="robots_txt"),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),

    # Ops
    path("health/", healthcheck, name="healthcheck"),

    # Website
    path("", include("website.urls")),
]

