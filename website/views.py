from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .forms import InquiryForm
from .models import SiteSettings, Service, Industry, ProcessStep, LegalPage, Inquiry


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
        "site": site,
        "site_name": _site_name(site),
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
        "site": site,
        "site_name": _site_name(site),
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

            receiver = getattr(settings, "CONTACT_RECEIVER_EMAIL", None) or (site.primary_email if site else None)

            if receiver:
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

                send_mail(
                    subject=subject,
                    message=body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[receiver],
                    fail_silently=True,
                )

            return redirect(reverse("contact") + "?sent=1")
    else:
        form = InquiryForm()

    context = {
        "site": site,
        "site_name": _site_name(site),
        "form": form,
        "sent": request.GET.get("sent") == "1",
        "page_meta": {
            "title": "Contact",
            "description": "Get in touch with TradeGate Consultants.",
            "canonical": request.build_absolute_uri("/contact/"),
        }
    }
    return render(request, "website/contact.html", context)


def about(request):
    site = _get_settings()
    context = {
        "site": site,
        "site_name": _site_name(site),
        "page_meta": {
            "title": "About",
            "description": "Learn about TradeGate and our EU business representation services.",
            "canonical": request.build_absolute_uri("/about/"),
        }
    }
    return render(request, "website/about.html", context)


def faq(request):
    site = _get_settings()
    page_meta = {
        "title": "FAQs",
        "description": "Frequently asked questions about TradeGate Consultants: EU representation, trade fairs, market entry, and deliverables.",
        "canonical": request.build_absolute_uri(),
    }
    return render(
        request,
        "website/faq.html",
        {"site": site, "site_name": _site_name(site), "page_meta": page_meta},
    )



