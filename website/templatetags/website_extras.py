from django import template

register = template.Library()


@register.filter
def get_item(mapping, key):
    """Look up a dictionary value by key in a template."""
    if not mapping:
        return None
    return mapping.get(key)


@register.filter
def rgb_channels(value, fallback="7 17 31"):
    """'#D6B36A' -> '214 179 106' for CSS variables used by the compiled stylesheet."""
    value = (value or "").strip().lstrip("#")
    if len(value) == 3:
        value = "".join(c * 2 for c in value)
    try:
        return " ".join(str(int(value[i:i + 2], 16)) for i in (0, 2, 4)) if len(value) == 6 else fallback
    except ValueError:
        return fallback


# --- Contact details: readable for people, not for address-harvesting bots -------------
import re as _re

from django.utils.html import conditional_escape as _esc
from django.utils.safestring import mark_safe as _safe

_EMAIL_RE = _re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
_PHONE_RE = _re.compile(r"\+?\(?\d[\d\s()/.-]{7,}\d")


def _entities(text):
    return "".join(f"&#{ord(c)};" for c in text)


@register.filter
def protect_contacts(value):
    """Escape text, then write email addresses and phone numbers as HTML character codes.

    People see and can copy the normal text; simple harvesting bots that search the page
    source for '@' or '+49 ...' patterns find nothing. Dates such as 15.11.2026 are left alone.
    """
    html = str(_esc(value or ""))

    def phone(m):
        digits = _re.sub(r"\D", "", m.group(0))
        return _entities(m.group(0)) if len(digits) >= 9 else m.group(0)

    html = _EMAIL_RE.sub(lambda m: _entities(m.group(0)), html)
    html = _PHONE_RE.sub(phone, html)
    return _safe(html)


@register.filter
def obfuscate(value):
    """Write a short value (an email address in a mailto: link) as HTML character codes."""
    return _safe(_entities(str(value or "")))
