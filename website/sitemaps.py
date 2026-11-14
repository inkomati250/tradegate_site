from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .content import SERVICE_PAGES
from .models import LegalPage, TradeFair


class StaticViewSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return ["home", "trade_fairs", "about", "faq", "contact"]

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
        paths = [reverse(n) for n in ("home", "trade_fairs", "about", "faq", "contact")]
        paths += [reverse("service_landing", kwargs={"slug": s}) for s in SERVICE_PAGES]
        paths += [reverse("trade_fair_detail", kwargs={"slug": f.slug}) for f in TradeFair.objects.filter(is_published=True)]
        return [(p, code) for code in i18n.LANGS if code != i18n.DEFAULT for p in paths]

    def location(self, item):
        path, code = item
        return f"{path}?lang={code}"
