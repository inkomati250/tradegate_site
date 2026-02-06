import logging

from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .forms import InquiryForm
from .models import SiteSettings, Service, Industry, ProcessStep, LegalPage, Inquiry

logger = logging.getLogger(__name__)


def _get_settings():
    return SiteSettings.objects.first()


def _site_name(site):
    return site.site_name if site and site.site_name else "TradeGate"


def home(request):
    site = _get_settings()

    services = Service.objects.filter(is_active=True).order_by("order", "title")
    industries = Industry.objects.filter(is_active=True).order_by("order", "name")
    steps = ProcessStep.objects.all().order_by("order")

    context = {
        "services": services,
        "industries": industries,
        "steps": steps,
        "page_meta": {
            "title": (site.meta_title if site and site.meta_title else _site_name(site)),
            "description": (site.meta_description if site else ""),
            "og_image": (site.og_image_url if site else ""),
            "canonical": request.build_absolute_uri("/"),
        }
    }
    return render(request, "website/home.html", context)


def legal_page(request, key):
    page = get_object_or_404(LegalPage, key=key)
    site = _get_settings()

    context = {
        "page": page,
        "page_meta": {
            "title": page.meta_title or page.title,
            "description": page.meta_description or (site.meta_description if site else ""),
            "og_image": (site.og_image_url if site else ""),
            "canonical": request.build_absolute_uri(page.get_absolute_url()),
        }
    }
    return render(request, "website/legal_page.html", context)


@require_http_methods(["GET", "POST"])
def contact(request):
    site = _get_settings()

    if request.method == "POST":
        form = InquiryForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data

            # Save inquiry to DB (single source of truth)
            inquiry = Inquiry.objects.create(
                full_name=cd["full_name"],
                email=cd["email"],
                subject=cd["subject"],
                message=cd["message"],

                company_name=cd.get("company_name", "") or "",
                website=cd.get("website", "") or "",
                country=cd.get("country", "") or "",
                service_interest=cd.get("service_interest", "") or "",
                timeline=cd.get("timeline", "") or "",
                budget_range=cd.get("budget_range", "") or "",
                contact_method=cd.get("contact_method", "") or "",
                phone=cd.get("phone", "") or "",
                consent=cd.get("consent", False),

                ip_address=request.META.get("REMOTE_ADDR"),
                user_agent=(request.META.get("HTTP_USER_AGENT") or "")[:255],
            )

            receiver = getattr(settings, "CONTACT_RECEIVER_EMAIL", None) or "contact@tradegateconsultants.com"

            subject = f"[{_site_name(site)}] New inquiry: {inquiry.subject}"
            body = (
                "New inquiry received\n\n"
                f"Name: {inquiry.full_name}\n"
                f"Email: {inquiry.email}\n"
                f"Company: {inquiry.company_name}\n"
                f"Website: {inquiry.website}\n"
                f"Country/Region: {inquiry.country}\n\n"
                f"Service interest: {inquiry.service_interest}\n"
                f"Timeline: {inquiry.timeline}\n"
                f"Budget range: {inquiry.budget_range}\n"
                f"Preferred contact method: {inquiry.contact_method}\n"
                f"Phone/WhatsApp: {inquiry.phone}\n\n"
                f"Subject: {inquiry.subject}\n\n"
                "Message:\n"
                f"{inquiry.message}\n\n"
                f"IP: {inquiry.ip_address}\n"
            )

            # Email notification: do not fail silently; log instead.
            try:
                msg = EmailMessage(
                    subject=subject,
                    body=body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[receiver],
                    reply_to=[inquiry.email],  # replying goes to the sender
                )
                msg.send(fail_silently=False)
            except Exception:
                logger.exception("Contact email failed for inquiry_id=%s", inquiry.id)
                messages.warning(
                    request,
                    "Your message was received, but our email notification had a temporary issue. "
                    "We will still respond within 24–48 hours."
                )

            messages.success(request, "Message received ✅ Thanks — we’ll respond within 24–48 hours.")
            return redirect(reverse("contact") + "#contact-form")

        # Invalid form: show clear banner; field errors already render below each field.
        messages.error(request, "Please fix the highlighted fields and try again.")

    else:
        form = InquiryForm()

    context = {
        "form": form,
        "page_meta": {
            "title": "Contact",
            "description": "Get in touch with TradeGate Consultants.",
            "canonical": request.build_absolute_uri("/contact/"),
        }
    }
    return render(request, "website/contact.html", context)


def about(request):
    context = {
        "page_meta": {
            "title": "About",
            "description": "Learn about TradeGate and our EU business representation services.",
            "canonical": request.build_absolute_uri("/about/"),
        }
    }
    return render(request, "website/about.html", context)


def faq(request):
    page_meta = {
        "title": "FAQs",
        "description": "Frequently asked questions about TradeGate Consultants: EU representation, trade fairs, market entry, and deliverables.",
        "canonical": request.build_absolute_uri(),
    }
    return render(request, "website/faq.html", {"page_meta": page_meta})





