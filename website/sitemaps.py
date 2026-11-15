from urllib.parse import urlparse

from django.conf import settings
from django.contrib.sitemaps import Sitemap as DjangoSitemap
from django.urls import reverse

from .content import SERVICE_PAGES
from .models import LegalPage, TradeFair

PUBLIC_DOMAIN = "www.tradegateconsultants.com"


class Sitemap(DjangoSitemap):
    """Every sitemap URL uses the real public domain (never Django's default 'example.com').

    Order: DJANGO_SITE_URL setting -> Sites framework entry (if not the default) -> public domain.
    """

    def get_domain(self, site=None):
        host = urlparse(getattr(settings, "SITE_URL", "") or "").netloc
        if host:
            return host
        domain = getattr(site, "domain", "") or ""
        if domain and domain != "example.com":
            return domain
        return PUBLIC_DOMAIN


class StaticViewSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return ["home", "trade_fairs", "partner_pool", "about", "faq", "contact"]

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


class TradeFairSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return TradeFair.objects.filter(is_published=True)

    def location(self, obj):
        return reverse("trade_fair_detail", kwargs={"slug": obj.slug})

    def lastmod(self, obj):
        return getattr(obj, "updated_at", None)


class TranslatedSitemap(Sitemap):
    """German, French, Portuguese and Spanish versions of every public page (?lang=xx)."""
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        from . import i18n
        paths = [reverse(n) for n in ("home", "trade_fairs", "partner_pool", "about", "faq", "contact")]
        paths += [reverse("service_landing", kwargs={"slug": s}) for s in SERVICE_PAGES]
        paths += [reverse("trade_fair_detail", kwargs={"slug": f.slug}) for f in TradeFair.objects.filter(is_published=True)]
        return [(p, code) for code in i18n.LANGS if code != i18n.DEFAULT for p in paths]

    def location(self, item):
        path, code = item
        return f"{path}?lang={code}"
