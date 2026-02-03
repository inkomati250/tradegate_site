from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import LegalPage


class StaticViewSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        # These must match named URL patterns
        return [
            "home",
            "about",
            "faq",
            "contact",
        ]

    def location(self, item):
        return reverse(item)

    def lastmod(self, item):
        # Static pages don’t really change often,
        # but returning None is perfectly valid.
        return None


class LegalPageSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.3

    def items(self):
        # Only include pages meant to be public/indexable
        return LegalPage.objects.all()

    def lastmod(self, obj):
        # Helps Google understand updates to legal texts
        # Works even if you only edit content occasionally
        return getattr(obj, "updated_at", None)
