from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path
from django.contrib.sitemaps.views import sitemap

from website.sitemaps import StaticViewSitemap, ServicePageSitemap, LegalPageSitemap, TradeFairSitemap, TranslatedSitemap

sitemaps = {
    "static": StaticViewSitemap,
    "services": ServicePageSitemap,
    "legal": LegalPageSitemap,
    "trade_fairs": TradeFairSitemap,
    "languages": TranslatedSitemap,
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


def _static_file(name, content_type):
    """Serve a file from website/static at the site root (Google looks for /favicon.ico)."""
    from pathlib import Path
    from django.http import FileResponse, Http404

    path = Path(__file__).resolve().parent.parent / "website" / "static" / name
    if not path.exists():
        raise Http404
    response = FileResponse(open(path, "rb"), content_type=content_type)
    response["Cache-Control"] = "public, max-age=604800"
    return response


def favicon(request):
    return _static_file("favicon.ico", "image/x-icon")


def webmanifest(request):
    return _static_file("site.webmanifest", "application/manifest+json")


def healthcheck(request):
    """
    Very small health endpoint for monitoring.
    """
    return HttpResponse("ok\n", content_type="text/plain")


urlpatterns = [
    path("admin/", admin.site.urls),

    # SEO + indexing
    path("robots.txt", robots_txt, name="robots_txt"),
    path("favicon.ico", favicon, name="favicon"),
    path("site.webmanifest", webmanifest, name="webmanifest"),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),

    # Ops
    path("health/", healthcheck, name="healthcheck"),

    # Website
    path("", include("website.urls")),

    #test to triger deploy
]



from django.conf import settings  # noqa: E402

if settings.DEBUG:
    from django.conf.urls.static import static  # noqa: E402

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
