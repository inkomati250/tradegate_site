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

from .content import DEFAULT_OPPORTUNITIES, SERVICE_NAV, SERVICE_PAGES
from .forms import InquiryForm
from .models import SiteSettings, Service, Industry, ProcessStep, LegalPage, Inquiry, TradeFairOpportunity

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


def service_landing(request, slug):
    page = SERVICE_PAGES.get(slug)
    if not page:
        return redirect("home")

    related_pages = [SERVICE_PAGES[item] for item in page.get("related", []) if item in SERVICE_PAGES]
    context = {
        "page": page,
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
    }
    return render(request, "website/about.html", context)


def faq(request):
    page_meta = {
        "title": "FAQs",
        "description": "Frequently asked questions about TradeGate Consultants: EU representation, trade fairs, market entry, partner search, deliverables and pricing.",
        "canonical": request.build_absolute_uri(),
    }
    return render(request, "website/faq.html", {"page_meta": page_meta, "service_nav": SERVICE_NAV})
