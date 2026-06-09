from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .content import SERVICE_PAGES
from .models import LegalPage


class StaticViewSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return ["home", "about", "faq", "contact"]

    def location(self, item):
        return reverse(item)

    def lastmod(self, item):
        return None


class ServicePageSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.85

    def items(self):
        return list(SERVICE_PAGES.keys())

    def location(self, slug):
        return reverse("service_landing", kwargs={"slug": slug})


class LegalPageSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.3

    def items(self):
        return LegalPage.objects.all()

    def lastmod(self, obj):
        return getattr(obj, "updated_at", None)
