"""Structured data (schema.org JSON-LD) helpers for search engines and AI assistants."""
import json
from html.parser import HTMLParser

from django.templatetags.static import static
from django.urls import reverse

LINKEDIN_COMPANY = "https://www.linkedin.com/company/tradegate-consultants/"
LINKEDIN_FOUNDER = "https://www.linkedin.com/in/ivan-nkomati-313637228"


def base_url(request):
    return f"{request.scheme}://{request.get_host()}"


def org_schema(request, site=None):
    """Who we are. Rendered on every page so search engines connect all pages to one business."""
    root = base_url(request)
    org_id = root + "/#organization"
    address = {"@type": "PostalAddress", "addressLocality": "Leipzig", "postalCode": "04179",
               "addressRegion": "Saxony", "addressCountry": "DE"}
    if site is not None:
        if getattr(site, "address_line1", ""):
            address["streetAddress"] = site.address_line1
        if getattr(site, "postal_code", ""):
            address["postalCode"] = site.postal_code
    same_as = [LINKEDIN_COMPANY]
    for field in ("facebook_url", "instagram_url", "x_url"):
        value = getattr(site, field, "") if site is not None else ""
        if value:
            same_as.append(value)
    org = {
        "@type": ["Organization", "ProfessionalService"],
        "@id": org_id,
        "name": "TradeGate Consultants",
        "url": root + "/",
        "logo": root + static("website/img/favicon-512.png"),
        "image": root + static("og-default.png"),
        "description": (
            "Leipzig-based consultancy helping international companies enter Germany and the EU: "
            "trade fair representation, distributor and partner search, local EU representation, "
            "market entry support and exhibitor recruitment for international trade fairs."
        ),
        "slogan": "Your gateway to Germany and the EU",
        "address": address,
        "geo": {"@type": "GeoCoordinates", "latitude": 51.3397, "longitude": 12.3731},
        "areaServed": [
            {"@type": "Country", "name": "Germany"},
            {"@type": "Place", "name": "European Union"},
            {"@type": "Place", "name": "Worldwide"},
        ],
        "knowsLanguage": ["en", "de"],
        "knowsAbout": [
            "Germany market entry", "EU market entry", "Trade fair representation in Germany",
            "Distributor search Germany", "Business partner search Germany", "EU local representative",
            "Exhibitor recruitment", "Trade fair follow-up and lead management", "German trade fairs",
        ],
        "founder": {"@type": "Person", "name": "Ivan Nkomati", "jobTitle": "Founder and Managing Partner",
                    "sameAs": [LINKEDIN_FOUNDER]},
        "sameAs": same_as,
        "priceRange": "€€",
        "contactPoint": {
            "@type": "ContactPoint", "contactType": "customer service",
            "url": root + reverse("contact"), "availableLanguage": ["English", "German"],
            "areaServed": ["DE", "EU"],
        },
    }
    email = getattr(site, "primary_email", "") if site is not None else ""
    if email:
        org["email"] = email
        org["contactPoint"]["email"] = email
    website = {
        "@type": "WebSite",
        "@id": root + "/#website",
        "url": root + "/",
        "name": "TradeGate Consultants",
        "inLanguage": "en",
        "publisher": {"@id": org_id},
    }
    return json.dumps({"@context": "https://schema.org", "@graph": [org, website]})


def breadcrumbs(request, *items):
    """items: (name, url_path) pairs after Home."""
    root = base_url(request)
    trail = [("Home", "/")] + list(items)
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i, "name": name, "item": root + path}
            for i, (name, path) in enumerate(trail, start=1)
        ],
    })


def faq_schema(pairs):
    pairs = [(q, a) for q, a in pairs if q and a]
    if not pairs:
        return ""
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in pairs
        ],
    })


class _FaqParser(HTMLParser):
    """Collects question/answer pairs from <details><summary>Q</summary>A</details> blocks."""

    def __init__(self):
        super().__init__()
        self.pairs, self._depth, self._in_summary, self._q, self._a = [], 0, False, [], []

    def handle_starttag(self, tag, attrs):
        if tag == "details":
            self._depth += 1
            self._q, self._a = [], []
        elif tag == "summary" and self._depth:
            self._in_summary = True

    def handle_endtag(self, tag):
        if tag == "summary":
            self._in_summary = False
        elif tag == "details" and self._depth:
            self._depth -= 1
            q = " ".join(" ".join(self._q).split())
            a = " ".join(" ".join(self._a).split())
            if q and a:
                self.pairs.append((q, a))

    def handle_data(self, data):
        if not self._depth:
            return
        (self._q if self._in_summary else self._a).append(data)


def faq_pairs_from_html(html):
    parser = _FaqParser()
    parser.feed(html)
    return parser.pairs
