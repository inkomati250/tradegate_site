from __future__ import annotations

import json
from typing import Any

from .models import SiteSettings
from .content import ORGANISER_NAV, SERVICE_NAV

# Navigation model may not exist yet (or migrations not applied yet).
# We import it safely to avoid breaking the project.
try:
    from .models import NavigationItem  # type: ignore
except Exception:
    NavigationItem = None  # type: ignore


def _asset_version() -> str:
    """Short hash of our CSS files, added as ?v=... so browsers fetch new CSS after each deploy
    (nginx tells browsers to cache /static/ for 30 days)."""
    global _ASSET_V
    if _ASSET_V is None:
        import hashlib
        from pathlib import Path
        base = Path(__file__).resolve().parent / "static" / "website"
        h = hashlib.md5()
        for rel in ("css/site.css", "admin/tradegate-admin.css"):
            try:
                h.update((base / rel).read_bytes())
            except OSError:
                pass
        _ASSET_V = h.hexdigest()[:10]
    return _ASSET_V


_ASSET_V = None


def site_settings(request) -> dict[str, Any]:
    site = SiteSettings.objects.first()

    nav_items = []
    nav_cta = None

    # NavigationItem is optional until you add the model and run migrations.
    # If not available yet, nav_items stays empty and templates can fall back.
    if NavigationItem is not None:
        try:
            qs = NavigationItem.objects.filter(is_visible=True).order_by("order", "label")
            nav_cta = qs.filter(is_cta=True).first()
            nav_items = list(qs)
        except Exception:
            nav_items = []
            nav_cta = None

    from django.conf import settings

    from .seo import org_schema
    from . import i18n

    lang = getattr(request, "LANGUAGE_CODE", i18n.DEFAULT)
    params = request.GET.copy()
    lang_links = []
    for code, info in i18n.LANGS.items():
        params["lang"] = code
        lang_links.append({"code": code, "name": info["name"], "flag": info["flag"],
                           "url": f"{request.path}?{params.urlencode()}", "current": code == lang})

    from .whatsapp import chat_link, qr_svg
    wa_link = chat_link(site.whatsapp_url if site else "")

    return {
        "asset_v": _asset_version(),
        "wa_link": wa_link,
        "wa_qr": qr_svg(wa_link),
        "wa_link_json": json.dumps(wa_link),
        "org_schema_json": org_schema(request, site),
        "lang": lang,
        "lang_name": i18n.LANGS[lang]["name"],
        "lang_flag": i18n.LANGS[lang]["flag"],
        "lang_og": i18n.LANGS[lang]["og"],
        "lang_suffix": "" if lang == i18n.DEFAULT else f"?lang={lang}",
        "lang_links": lang_links,
        "lang_codes": list(i18n.LANGS),
        "google_site_verification": getattr(settings, "GOOGLE_SITE_VERIFICATION", ""),
        "bing_site_verification": getattr(settings, "BING_SITE_VERIFICATION", ""),
        "use_tailwind_cdn": getattr(settings, "USE_TAILWIND_CDN", False),
        "site": site,
        "site_name": (site.site_name if site and site.site_name else "TradeGate"),
        "nav_items": nav_items,
        "nav_cta": nav_cta,  # NEW: lets base.html render a single CTA button cleanly
        "global_service_nav": SERVICE_NAV,
        "global_organiser_nav": ORGANISER_NAV,
    }
