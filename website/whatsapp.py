"""WhatsApp contact: a QR code (scan with the phone) instead of sending desktop visitors to an external page."""
from functools import lru_cache
from urllib.parse import quote, urlparse, parse_qs, urlencode, urlunparse

GREETING = "Hello TradeGate, I found you on your website and would like to talk about "


def chat_link(url):
    """The owner's wa.me link with a friendly first message filled in (unless one is already set)."""
    if not url:
        return ""
    parts = urlparse(url)
    query = parse_qs(parts.query)
    if "text" not in query:
        query["text"] = [GREETING]
    return urlunparse(parts._replace(query=urlencode(query, doseq=True, quote_via=quote)))


@lru_cache(maxsize=4)
def qr_svg(link):
    if not link:
        return ""
    try:
        import segno
        return segno.make(link, error="m").svg_inline(scale=6, border=2, omitsize=True, dark="#07111F", light="#ffffff",
                                                       title="WhatsApp QR code")
    except Exception:
        return ""
