"""Cookieless, first-party visitor statistics.

What we store per page view: day, page, country (from the IP via a local DB-IP
country database), source (Google, LinkedIn, direct ...), device type, site
language and a visitor code. The visitor code is a hash of IP + browser + a salt
that changes every day, so the same person cannot be followed across days and
the IP address itself is never stored. No cookies, nothing sent to third parties.
Visits by logged-in staff, bots, and browsers with Do Not Track / Global Privacy
Control are not counted.
"""
import hashlib
import logging
import re
from datetime import date, timedelta
from functools import lru_cache
from urllib.parse import urlparse

from django.conf import settings

logger = logging.getLogger(__name__)

BOT_RE = re.compile(
    r"bot|crawl|spider|slurp|scrap|fetch|preview|monitor|uptime|headless|lighthouse|pingdom|curl|wget|python|"
    r"java/|go-http|okhttp|axios|node-fetch|facebookexternalhit|whatsapp|telegram|discord|semrush|ahrefs|mj12|"
    r"petal|yandex|baidu|bytespider|gptbot|claude|perplexity|ccbot|dataprovider|zgrab|masscan|nmap",
    re.I,
)
SKIP_PREFIXES = ("/admin", "/static", "/media", "/sitemap", "/robots", "/favicon", "/site.webmanifest", "/.well-known")
RETENTION_DAYS = 400
LANG_NAMES = {"en": "English", "de": "German", "fr": "French", "pt": "Portuguese", "es": "Spanish"}

SOURCES = [
    ("AI assistants", ("chatgpt.com", "openai.com", "perplexity.ai", "claude.ai", "gemini.google.com", "copilot.microsoft.com")),
    ("Email", ("mail.", "outlook.", "gmx.", "web.de")),
    ("Google", ("google.",)),
    ("Bing", ("bing.com",)),
    ("LinkedIn", ("linkedin.com", "lnkd.in")),
    ("Facebook / Instagram", ("facebook.com", "fb.com", "instagram.com")),
    ("X / Twitter", ("t.co", "twitter.com", "x.com")),
    ("Other search engines", ("duckduckgo.com", "yahoo.", "ecosia.org", "yandex.", "baidu.com", "brave.com")),
]


@lru_cache(maxsize=1)
def _reader():
    path = getattr(settings, "GEOIP_COUNTRY_DB", "")
    if not path:
        return None
    try:
        import maxminddb
        return maxminddb.open_database(path)
    except Exception:
        logger.info("Country database not available at %s; countries shown as Unknown", path)
        return None


def country_of(ip):
    """Return (ISO code, English name) for an IP, or ("", "") when unknown."""
    reader = _reader()
    if not reader or not ip:
        return "", ""
    try:
        rec = reader.get(ip) or {}
        c = rec.get("country") or {}
        return (c.get("iso_code") or "")[:2], ((c.get("names") or {}).get("en") or "")[:60]
    except Exception:
        return "", ""


def client_ip(request):
    ip = request.META.get("HTTP_X_REAL_IP") or ""
    if not ip:
        fwd = request.META.get("HTTP_X_FORWARDED_FOR", "")
        ip = fwd.split(",")[0].strip() if fwd else request.META.get("REMOTE_ADDR", "")
    return ip[:45]


def _host_matches(host, needle):
    """'google.' matches any Google domain (google.de, www.google.com); 'linkedin.com' matches it and its subdomains."""
    if needle.endswith("."):
        return host.startswith(needle) or f".{needle}" in f".{host}"
    return host == needle or host.endswith("." + needle)


def source_of(referrer, own_host):
    if not referrer:
        return "Direct / unknown", ""
    host = (urlparse(referrer).hostname or "").lower()
    if not host or host == own_host or host.endswith("tradegateconsultants.com"):
        return "", ""  # internal navigation: not a new source
    for name, needles in SOURCES:
        if any(_host_matches(host, n) for n in needles):
            return name, host[:120]
    return "Other websites", host[:120]


def device_of(ua):
    ua = ua.lower()
    if "ipad" in ua or "tablet" in ua:
        return "Tablet"
    if "mobi" in ua or "android" in ua or "iphone" in ua:
        return "Mobile"
    return "Desktop"


def visitor_code(ip, ua, day):
    salt = f"{settings.SECRET_KEY}:{day.isoformat()}"
    return hashlib.sha256(f"{salt}|{ip}|{ua}".encode()).hexdigest()[:16]


def should_count(request, response):
    if request.method != "GET" or response.status_code != 200:
        return False
    if not (response.get("Content-Type", "").startswith("text/html")):
        return False
    if request.path.startswith(SKIP_PREFIXES):
        return False
    if request.META.get("HTTP_DNT") == "1" or request.META.get("HTTP_SEC_GPC") == "1":
        return False
    ua = request.META.get("HTTP_USER_AGENT", "")
    if not ua or BOT_RE.search(ua):
        return False
    user = getattr(request, "user", None)
    if user is not None and getattr(user, "is_staff", False):
        return False
    return True


def record(request, response):
    from .models import PageVisit

    if not should_count(request, response):
        return
    try:
        from django.utils import timezone
        today = timezone.localdate()
        ip = client_ip(request)
        ua = request.META.get("HTTP_USER_AGENT", "")[:400]
        code, name = country_of(ip)
        source, ref_host = source_of(request.META.get("HTTP_REFERER", ""), request.get_host().split(":")[0].lower())
        PageVisit.objects.create(
            day=today,
            visitor=visitor_code(ip, ua, today),
            path=request.path[:200],
            country_code=code,
            country=name,
            source=source,
            referrer_host=ref_host,
            device=device_of(ua),
            language=getattr(request, "LANGUAGE_CODE", "en")[:5],
        )
    except Exception:
        logger.debug("Visit not recorded", exc_info=True)


def prune():
    from .models import PageVisit
    cutoff = date.today() - timedelta(days=RETENTION_DAYS)
    return PageVisit.objects.filter(day__lt=cutoff).delete()[0]


def summary(days=30):
    """Figures for the admin: visitors, page views, countries, sources, pages, devices, languages, daily series."""
    from django.db.models import Count
    from django.utils import timezone
    from .models import Inquiry, PageVisit, PartnerProfile

    today = timezone.localdate()
    start = today - timedelta(days=days - 1)
    qs = PageVisit.objects.filter(day__gte=start)

    def top(field, n=10, exclude_blank=True):
        q = qs
        if exclude_blank:
            q = q.exclude(**{field: ""})
        rows = q.values(field).annotate(visitors=Count("visitor", distinct=True), views=Count("id")).order_by("-visitors", "-views")[:n]
        total = max(1, sum(r["visitors"] for r in rows))
        return [{"label": r[field] or "Unknown", "visitors": r["visitors"], "views": r["views"],
                 "pct": round(100 * r["visitors"] / total)} for r in rows]

    daily = {r["day"]: r for r in qs.values("day").annotate(visitors=Count("visitor", distinct=True), views=Count("id"))}
    series = []
    peak = max([1] + [r["visitors"] for r in daily.values()])
    for i in range(days):
        d = start + timedelta(days=i)
        v = daily.get(d, {}).get("visitors", 0)
        series.append({"day": d, "visitors": v, "views": daily.get(d, {}).get("views", 0), "h": round(100 * v / peak)})

    def uniq(q):
        return q.values("visitor", "day").distinct().count()

    countries = top("country", 12, exclude_blank=False)
    hub_views = qs.filter(path__startswith="/partner-hub/").count()
    contact_views = qs.filter(path__startswith="/contact/").count()
    hub_regs = PartnerProfile.objects.filter(created_at__date__gte=start).count()
    enquiries = Inquiry.objects.filter(created_at__date__gte=start).count()
    return {
        "days": days,
        "visitors": uniq(qs),
        "views": qs.count(),
        "today": uniq(PageVisit.objects.filter(day=today)),
        "week": uniq(PageVisit.objects.filter(day__gte=today - timedelta(days=6))),
        "countries": countries,
        "country_count": qs.exclude(country="").values("country").distinct().count(),
        "sources": top("source", 10),
        "pages": top("path", 12),
        "devices": top("device", 3),
        "languages": [{**r, "label": LANG_NAMES.get(r["label"], r["label"])} for r in top("language", 5)],
        "series": series,
        "hub_views": hub_views,
        "hub_regs": hub_regs,
        "hub_rate": round(100 * hub_regs / hub_views, 1) if hub_views else 0,
        "contact_views": contact_views,
        "enquiries": enquiries,
        "contact_rate": round(100 * enquiries / contact_views, 1) if contact_views else 0,
        "has_geo": _reader() is not None,
    }
