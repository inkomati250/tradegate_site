import json
import logging
from django.conf import settings
from django.contrib import messages
from django.core.cache import cache
from django.core.mail import EmailMessage
from django.db import DatabaseError, OperationalError, ProgrammingError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .content import DEFAULT_OPPORTUNITIES, FAIR_CATEGORIES, FAIR_DISCLAIMER, fair_categories, FOUNDER, PRICING_NOTE, SERVICE_NAV, SERVICE_PAGES
from .forms import InquiryForm
from datetime import date, timedelta

from django.http import HttpResponse
from django.utils import timezone

from .models import SiteSettings, Service, Industry, ProcessStep, LegalPage, Inquiry, ServicePackage, TeamProfile, TradeFair, TradeFairOpportunity

logger = logging.getLogger(__name__)


def _get_settings():
    return SiteSettings.objects.first()


def _site_name(site):
    return site.site_name if site and site.site_name else "TradeGate"


def _get_client_ip(request):
    """Best-effort client IP without changing proxy/settings files.

    In production behind nginx, REMOTE_ADDR can be 127.0.0.1. If nginx sends
    X-Forwarded-For, use the first public value for logging and light spam checks.
    """
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if forwarded:
        return forwarded.split(",")[0].strip()[:45]
    return (request.META.get("REMOTE_ADDR") or "")[:45]


def _is_rate_limited(request, email=""):
    """Small, dependency-free throttle for contact abuse.

    It avoids blocking the whole site when REMOTE_ADDR is localhost behind nginx.
    Suspicious submissions are silently accepted but not mailed.
    """
    reasons = []
    ip = _get_client_ip(request)
    keys = []

    if ip and ip not in {"127.0.0.1", "::1"}:
        keys.append((f"tg-contact-ip:{ip}", 8, 15 * 60, "ip_rate"))
    if email:
        keys.append((f"tg-contact-email:{email.lower()}", 4, 30 * 60, "email_rate"))

    for key, limit, ttl, reason in keys:
        try:
            count = cache.get(key, 0) + 1
            cache.set(key, count, ttl)
            if count > limit:
                reasons.append(reason)
        except Exception:
            logger.debug("Contact rate cache unavailable", exc_info=True)
    return reasons


def _get_opportunities():
    try:
        items = list(TradeFairOpportunity.objects.filter(is_active=True).order_by("order", "title")[:8])
        return items or DEFAULT_OPPORTUNITIES
    except (OperationalError, ProgrammingError, DatabaseError):
        # Keeps public pages alive if code is deployed before the new migration runs.
        logger.warning("TradeFairOpportunity table not ready; using default opportunities.", exc_info=True)
        return DEFAULT_OPPORTUNITIES


def _upcoming_fairs():
    """Published fairs that have not ended yet, soonest first."""
    try:
        today = timezone.localdate()
        qs = TradeFair.objects.filter(is_published=True)
        fairs = [f for f in qs if not f.end_date or f.end_date >= today]
        return sorted(fairs, key=lambda f: (f.start_date is None, f.start_date or today, f.order, f.name))
    except (OperationalError, ProgrammingError, DatabaseError):
        logger.warning("TradeFair table not ready.", exc_info=True)
        return []


def trade_fairs(request):
    fairs = _upcoming_fairs()
    represented = [f for f in fairs if f.is_represented]
    germany = [f for f in fairs if not f.is_represented]
    months = []
    for f in germany:
        key = f.start_date.strftime("%B %Y") if f.start_date else "Dates to be announced"
        if not months or months[-1][0] != key:
            months.append((key, []))
        months[-1][1].append(f)
    for f in fairs:
        f.categories = fair_categories(f.sectors)
    used = {c for f in fairs for c in f.categories}
    sectors = [name for name, _ in FAIR_CATEGORIES if name in used]
    context = {
        "represented": represented,
        "months": months,
        "sectors": sectors,
        "disclaimer": FAIR_DISCLAIMER,
        "service_nav": SERVICE_NAV,
        "page_meta": {
            "title": "Trade Fair Calendar Germany 2027",
            "description": "Major German trade fairs in 2027 with dates, sectors and who should exhibit, plus international events we recruit German exhibitors for.",
            "canonical": request.build_absolute_uri(reverse("trade_fairs")),
        },
    }
    return render(request, "website/trade_fairs.html", context)


def _fair_schema(request, fair):
    data = {
        "@context": "https://schema.org",
        "@type": "Event",
        "name": fair.name,
        "description": fair.summary,
        "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
        "eventStatus": "https://schema.org/EventScheduled",
        "location": {
            "@type": "Place",
            "name": fair.venue or fair.city,
            "address": {"@type": "PostalAddress", "addressLocality": fair.city, "addressCountry": fair.country},
        },
        "url": request.build_absolute_uri(reverse("trade_fair_detail", kwargs={"slug": fair.slug})),
    }
    if fair.start_date:
        data["startDate"] = fair.start_date.isoformat()
        data["endDate"] = (fair.end_date or fair.start_date).isoformat()
    if fair.organiser and not fair.is_represented:
        data["organizer"] = {"@type": "Organization", "name": fair.organiser, "url": fair.public_official_url or None}
    return json.dumps(data)


def trade_fair_detail(request, slug):
    fair = get_object_or_404(TradeFair, slug=slug, is_published=True)
    others = [f for f in _upcoming_fairs() if f.pk != fair.pk][:3]
    context = {
        "fair": fair,
        "others": others,
        "disclaimer": FAIR_DISCLAIMER,
        "service_nav": SERVICE_NAV,
        "page_meta": {
            "title": f"{fair.name} {fair.start_date.year if fair.start_date else ''}".strip() + (" – exhibit through TradeGate" if fair.is_represented else " – representation and buyer meetings"),
            "description": fair.summary,
            "canonical": request.build_absolute_uri(reverse("trade_fair_detail", kwargs={"slug": slug})),
        },
        "structured_data_json": _fair_schema(request, fair),
    }
    return render(request, "website/trade_fair_detail.html", context)


def trade_fair_ics(request, slug):
    fair = get_object_or_404(TradeFair, slug=slug, is_published=True)
    if not fair.start_date:
        return redirect("trade_fair_detail", slug=slug)
    end = (fair.end_date or fair.start_date) + timedelta(days=1)
    url = request.build_absolute_uri(reverse("trade_fair_detail", kwargs={"slug": slug}))
    def esc(s):
        return s.replace("\\", "\\\\").replace(",", "\\,").replace(";", "\\;").replace("\n", "\\n")
    body = "\r\n".join([
        "BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//TradeGate Consultants//Trade fair calendar//EN",
        "BEGIN:VEVENT",
        f"UID:{fair.slug}@tradegateconsultants.com",
        f"DTSTAMP:{timezone.now().strftime('%Y%m%dT%H%M%SZ')}",
        f"DTSTART;VALUE=DATE:{fair.start_date.strftime('%Y%m%d')}",
        f"DTEND;VALUE=DATE:{end.strftime('%Y%m%d')}",
        f"SUMMARY:{esc(fair.name)}",
        f"LOCATION:{esc(fair.place_label)}",
        f"DESCRIPTION:{esc(fair.summary + ' Details: ' + url)}",
        f"URL:{url}",
        "END:VEVENT", "END:VCALENDAR", "",
    ])
    response = HttpResponse(body, content_type="text/calendar; charset=utf-8")
    response["Content-Disposition"] = f'attachment; filename="{fair.slug}.ics"'
    return response


def _service_schema(request, page):
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "Service",
        "name": page["title"],
        "description": page["subtitle"],
        "provider": {
            "@type": "Organization",
            "name": "TradeGate Consultants",
            "url": request.build_absolute_uri(reverse("home")),
            "address": {
                "@type": "PostalAddress",
                "addressLocality": "Leipzig",
                "addressCountry": "DE",
            },
        },
        "areaServed": ["Germany", "European Union"],
        "audience": {
            "@type": "BusinessAudience",
            "audienceType": "International SMEs seeking Germany/EU market entry",
        },
    })


def home(request):
    site = _get_settings()

    services = Service.objects.filter(is_active=True).order_by("order", "title")
    industries = Industry.objects.filter(is_active=True).order_by("order", "name")
    steps = ProcessStep.objects.all().order_by("order")
    opportunities = _get_opportunities()

    context = {
        "services": services,
        "industries": industries,
        "steps": steps,
        "service_nav": SERVICE_NAV,
        "service_pages": SERVICE_PAGES,
        "opportunities": opportunities,
        "carousel_fairs": [f for f in _upcoming_fairs() if f.show_in_carousel and not f.is_represented and f.start_date][:15],
        "partner_fairs": [f for f in _upcoming_fairs() if f.is_represented],
        "page_meta": {
            "title": site.meta_title if site and site.meta_title else "Germany & EU Market Entry Support for International SMEs",
            "description": site.meta_description if site and site.meta_description else "TradeGate Consultants helps international SMEs with Germany/EU market entry, trade fair representation, partner search and local presence from Leipzig.",
            "og_image": site.og_image_url if site else "",
            "canonical": request.build_absolute_uri("/"),
        },
        "structured_data_json": json.dumps({
            "@context": "https://schema.org",
            "@type": "Organization",
            "name": "TradeGate Consultants",
            "url": request.build_absolute_uri("/"),
            "description": "Germany and EU market-entry support, trade fair representation and partner search for international SMEs.",
            "address": {"@type": "PostalAddress", "addressLocality": "Leipzig", "addressCountry": "DE"},
        }),
    }
    return render(request, "website/home.html", context)


def _db_packages(slug):
    try:
        rows = ServicePackage.objects.filter(service_slug=slug, is_active=True)
        return [
            {"name": p.name, "price": p.price, "unit": p.unit, "best_for": p.best_for,
             "featured": p.featured, "includes": p.include_list}
            for p in rows
        ]
    except (OperationalError, ProgrammingError, DatabaseError):
        return []


def _team():
    try:
        people = list(TeamProfile.objects.filter(is_active=True))
    except (OperationalError, ProgrammingError, DatabaseError):
        people = []
    if not people:
        return [FOUNDER]
    return [
        {"name": p.name, "role": p.role, "location": p.location, "photo_url": p.display_photo_url,
         "linkedin_url": p.linkedin_url, "intro": p.intro, "partners": p.partners_text, "background": p.background}
        for p in people
    ]


def service_landing(request, slug):
    page = SERVICE_PAGES.get(slug)
    if not page:
        return redirect("home")
    db_packages = _db_packages(slug)
    if db_packages:
        page = {**page, "packages": db_packages}

    related_pages = [SERVICE_PAGES[item] for item in page.get("related", []) if item in SERVICE_PAGES]
    context = {
        "page": page,
        "pricing_note": PRICING_NOTE,
        "service_nav": SERVICE_NAV,
        "related_pages": related_pages,
        "page_meta": {
            "title": page["meta_title"].replace(" | TradeGate Consultants", ""),
            "description": page["meta_description"],
            "canonical": request.build_absolute_uri(reverse("service_landing", kwargs={"slug": slug})),
        },
        "structured_data_json": _service_schema(request, page),
    }
    return render(request, "website/service_landing.html", context)


def legal_page(request, key):
    page = get_object_or_404(LegalPage, key=key)
    site = _get_settings()

    context = {
        "page": page,
        "page_meta": {
            "title": page.meta_title or page.title,
            "description": page.meta_description or (site.meta_description if site else ""),
            "og_image": site.og_image_url if site else "",
            "canonical": request.build_absolute_uri(page.get_absolute_url()),
        },
    }
    return render(request, "website/legal_page.html", context)


@require_http_methods(["GET", "POST"])
def contact(request):
    site = _get_settings()

    initial = {}
    service = request.GET.get("service")
    if service:
        initial["service_interest"] = service
    event = request.GET.get("event")
    if event:
        initial["subject"] = f"Trade fair support: {event.replace('-', ' ').title()}"
    fair_slug = (request.GET.get("fair") or "").strip()[:160]
    if fair_slug:
        fair = TradeFair.objects.filter(slug=fair_slug, is_published=True).first()
        if fair:
            initial["subject"] = (f"Stand enquiry: {fair.name}" if fair.is_represented else f"Representation at {fair.name}")[:160]
    package = (request.GET.get("package") or "").strip()[:80]
    if package:
        initial["subject"] = f"Package enquiry: {package}"

    if request.method == "POST":
        form = InquiryForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            suspicious_reasons = form.suspicious_reasons()
            suspicious_reasons += _is_rate_limited(request, cd.get("email", ""))
            is_suspicious = bool(suspicious_reasons)

            enriched_message = (
                f"{cd['message']}\n\n"
                "--- Lead qualification ---\n"
                f"Role: {cd.get('role', '')}\n"
                f"Industry/Sector: {cd.get('industry', '')}\n"
                f"Target market: {cd.get('target_market', '')}\n"
                f"Lead quality: {form.quality_label()}\n"
            )

            if is_suspicious:
                logger.warning(
                    "Suspicious contact submission suppressed: reasons=%s email=%s subject=%s ip=%s",
                    suspicious_reasons,
                    cd.get("email"),
                    cd.get("subject"),
                    _get_client_ip(request),
                )
                # Silent success keeps the inbox clean and avoids training bots to retry.
                messages.success(
                    request,
                    "Thanks — your message has been received. We’ll respond if it matches our services.",
                )
                return redirect(reverse("contact") + "#contact-form")

            inquiry = Inquiry.objects.create(
                full_name=cd["full_name"],
                email=cd["email"],
                subject=cd["subject"],
                message=enriched_message,
                company_name=cd.get("company_name", "") or "",
                website=cd.get("website", "") or "",
                country=cd.get("country", "") or "",
                service_interest=cd.get("service_interest", "") or "",
                timeline=cd.get("timeline", "") or "",
                budget_range=cd.get("budget_range", "") or "",
                contact_method=cd.get("contact_method", "") or "",
                phone=cd.get("phone", "") or "",
                consent=cd.get("consent", False),
                ip_address=_get_client_ip(request) or None,
                user_agent=(request.META.get("HTTP_USER_AGENT") or "")[:255],
            )

            receiver = getattr(settings, "CONTACT_RECIPIENT_EMAIL", "") or "contact@tradegateconsultants.com"
            from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "") or "no-reply@tradegateconsultants.com"

            quality = form.quality_label()
            country = cd.get("country") or "Unknown country"
            service_label = dict(InquiryForm.base_fields["service_interest"].choices).get(cd.get("service_interest"), cd.get("service_interest"))
            email_subject = f"[{_site_name(site)}] {quality} inquiry: {service_label} — {country}"
            email_body = (
                "New qualified inquiry received\n\n"
                f"Lead quality: {quality}\n"
                f"Name: {inquiry.full_name}\n"
                f"Role: {cd.get('role', '')}\n"
                f"Email: {inquiry.email}\n"
                f"Company: {inquiry.company_name}\n"
                f"Website: {inquiry.website}\n"
                f"Country/Region: {inquiry.country}\n"
                f"Industry/Sector: {cd.get('industry', '')}\n"
                f"Target market: {cd.get('target_market', '')}\n\n"
                f"Service interest: {service_label}\n"
                f"Timeline: {inquiry.timeline}\n"
                f"Budget range: {inquiry.budget_range}\n"
                f"Preferred contact method: {inquiry.contact_method}\n"
                f"Phone/WhatsApp: {inquiry.phone}\n\n"
                f"Subject: {inquiry.subject}\n\n"
                "Message:\n"
                f"{cd['message']}\n\n"
                f"IP: {inquiry.ip_address}\n"
                f"User-Agent: {inquiry.user_agent}\n"
            )

            email_sent = False

            try:
                msg = EmailMessage(
                    subject=email_subject,
                    body=email_body,
                    from_email=from_email,
                    to=[receiver],
                    reply_to=[inquiry.email],
                )
                msg.send(fail_silently=False)
                email_sent = True
                logger.info("Contact email sent successfully for inquiry_id=%s to=%s", inquiry.id, receiver)
            except Exception:
                logger.exception("Contact email failed for inquiry_id=%s", inquiry.id)

            if email_sent:
                messages.success(request, "Thanks — your message has been sent successfully. We’ll respond within 24–48 hours.")
            else:
                messages.warning(request, "Your message was received successfully, but our email notification had a temporary issue. We will still respond within 24–48 hours.")

            return redirect(reverse("contact") + "#contact-form")

        logger.warning("Contact form invalid: %s", form.errors.as_json())
        messages.error(request, "Please correct the highlighted fields and try again.")

    else:
        form = InquiryForm(initial=initial)

    context = {
        "form": form,
        "page_meta": {
            "title": "Contact TradeGate Consultants",
            "description": "Contact TradeGate Consultants for Germany/EU market entry, trade fair representation, partner search and local presence support.",
            "canonical": request.build_absolute_uri("/contact/"),
        },
    }
    return render(request, "website/contact.html", context)


def about(request):
    context = {
        "page_meta": {
            "title": "About TradeGate Consultants",
            "description": "TradeGate Consultants is a Leipzig-based Germany/EU market-entry partner for international SMEs seeking representation, partners and trade fair support.",
            "canonical": request.build_absolute_uri("/about/"),
        },
        "service_nav": SERVICE_NAV,
        "founder": _team()[0],
        "team": _team(),
    }
    return render(request, "website/about.html", context)


def faq(request):
    page_meta = {
        "title": "FAQs",
        "description": "Frequently asked questions about TradeGate Consultants: EU representation, trade fairs, market entry, partner search, deliverables and pricing.",
        "canonical": request.build_absolute_uri(),
    }
    return render(request, "website/faq.html", {"page_meta": page_meta, "service_nav": SERVICE_NAV})
