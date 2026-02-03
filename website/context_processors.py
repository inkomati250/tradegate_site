from __future__ import annotations

from typing import Any

from .models import SiteSettings

# Navigation model may not exist yet (or migrations not applied yet).
# We import it safely to avoid breaking the project.
try:
    from .models import NavigationItem  # type: ignore
except Exception:
    NavigationItem = None  # type: ignore


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

    return {
        "site": site,
        "site_name": (site.site_name if site and site.site_name else "TradeGate"),
        "nav_items": nav_items,
        "nav_cta": nav_cta,  # NEW: lets base.html render a single CTA button cleanly
    }
