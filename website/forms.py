import re
import time
from urllib.parse import urlparse

from django import forms


SERVICE_CHOICES = [
    ("", "Select service"),
    ("trade_fair", "Trade fair & event representation"),
    ("scouting", "Market entry & partner scouting"),
    ("distributor_search", "Distributor / reseller search"),
    ("local_presence", "Local EU presence without an office"),
    ("follow_up", "Trade fair follow-up & lead management"),
    ("other", "Other / Not sure yet"),
]

TIMELINE_CHOICES = [
    ("", "Select timeline"),
    ("asap", "ASAP (0–2 weeks)"),
    ("2_4_weeks", "2–4 weeks"),
    ("1_3_months", "1–3 months"),
    ("3_6_months", "3–6 months"),
    ("planning", "Just planning / researching"),
]

BUDGET_CHOICES = [
    ("", "Select budget range"),
    ("not_sure", "Not sure yet"),
    ("lt_1k", "Under €1,000"),
    ("1k_3k", "€1,000 – €3,000"),
    ("3k_10k", "€3,000 – €10,000"),
    ("10k_plus", "€10,000+"),
]

CONTACT_METHOD_CHOICES = [
    ("email", "Email"),
    ("phone", "Phone / WhatsApp"),
    ("video", "Video call"),
]

SUSPICIOUS_KEYWORDS = [
    "googlesearchindex",
    "google search index",
    "searchregister",
    "domain registration",
    "register your domain",
    "video promotion",
    "seo promotion",
    "backlinks",
    "guest post",
    "rank on google",
    "crypto investment",
    "casino",
    "loan offer",
    "whatsapp marketing",
]

FREE_EMAIL_DOMAINS = {
    "gmail.com", "googlemail.com", "yahoo.com", "outlook.com", "hotmail.com",
    "icloud.com", "aol.com", "proton.me", "protonmail.com", "gmx.com", "gmx.de",
}


class InquiryForm(forms.Form):
    # Honeypot: real visitors never see/fill this field.
    website_url = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "autocomplete": "off",
            "tabindex": "-1",
            "class": "sr-only",
        }),
    )
    # Lightweight timing check: bots often submit instantly.
    form_started_at = forms.CharField(required=False, widget=forms.HiddenInput())

    full_name = forms.CharField(
        label="Full name",
        max_length=120,
        error_messages={
            "required": "Please enter your full name.",
            "max_length": "Full name is too long.",
        },
        widget=forms.TextInput(attrs={
            "placeholder": "Your name",
            "autocomplete": "name",
        }),
    )

    email = forms.EmailField(
        label="Business email",
        error_messages={
            "required": "Please enter your email address.",
            "invalid": "Please enter a valid email address.",
        },
        widget=forms.EmailInput(attrs={
            "placeholder": "you@company.com",
            "autocomplete": "email",
        }),
    )

    role = forms.CharField(
        label="Your role (optional)",
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={
            "placeholder": "Founder, Export Manager, Sales Director…",
            "autocomplete": "organization-title",
        }),
    )

    company_name = forms.CharField(
        label="Company / Organization",
        required=False,
        max_length=160,
        widget=forms.TextInput(attrs={
            "placeholder": "Company / Organization",
            "autocomplete": "organization",
        }),
    )

    website = forms.URLField(
        label="Company website",
        required=False,
        error_messages={
            "invalid": "Please enter a valid website URL starting with http:// or https://",
        },
        widget=forms.URLInput(attrs={
            "placeholder": "https://…",
            "autocomplete": "url",
        }),
    )

    country = forms.CharField(
        label="Country / Region",
        required=False,
        max_length=80,
        widget=forms.TextInput(attrs={
            "placeholder": "e.g., Rwanda, UAE, India",
        }),
    )

    industry = forms.CharField(
        label="Industry / sector (optional)",
        required=False,
        max_length=120,
        widget=forms.TextInput(attrs={
            "placeholder": "Food, manufacturing, tourism, tech…",
        }),
    )

    target_market = forms.CharField(
        label="Target market (optional)",
        required=False,
        max_length=120,
        widget=forms.TextInput(attrs={
            "placeholder": "Germany, DACH, EU, specific trade fair…",
        }),
    )

    service_interest = forms.ChoiceField(
        label="What do you need?",
        choices=SERVICE_CHOICES,
        error_messages={
            "required": "Please select the type of support you need.",
        },
        widget=forms.Select(),
    )

    timeline = forms.ChoiceField(
        label="Timeline (optional)",
        choices=TIMELINE_CHOICES,
        required=False,
        widget=forms.Select(),
    )

    budget_range = forms.ChoiceField(
        label="Budget range (optional)",
        choices=BUDGET_CHOICES,
        required=False,
        widget=forms.Select(),
    )

    contact_method = forms.ChoiceField(
        label="Preferred contact method (optional)",
        choices=CONTACT_METHOD_CHOICES,
        required=False,
        initial="email",
        widget=forms.RadioSelect(),
    )

    phone = forms.CharField(
        label="Phone / WhatsApp (optional)",
        required=False,
        max_length=40,
        widget=forms.TextInput(attrs={
            "placeholder": "+49 …",
            "autocomplete": "tel",
        }),
    )

    subject = forms.CharField(
        label="Subject",
        max_length=140,
        error_messages={
            "required": "Please enter a subject.",
            "max_length": "Subject is too long.",
        },
        widget=forms.TextInput(attrs={
            "placeholder": "Short subject",
        }),
    )

    message = forms.CharField(
        label="Project details",
        error_messages={
            "required": "Please provide some project details.",
        },
        widget=forms.Textarea(attrs={
            "rows": 6,
            "placeholder": "Tell us what you want to achieve, what you sell, who you want to reach, and whether a trade fair or partner search is already planned.",
        }),
    )

    consent = forms.BooleanField(
        label="I agree that TradeGate may store my message to respond to my request (GDPR).",
        required=True,
        error_messages={
            "required": "Consent is required to submit this form.",
        },
    )

    def __init__(self, *args, **kwargs):
        initial = kwargs.setdefault("initial", {})
        initial.setdefault("form_started_at", str(int(time.time())))
        super().__init__(*args, **kwargs)

    def clean_website_url(self):
        val = (self.cleaned_data.get("website_url") or "").strip()
        if val:
            raise forms.ValidationError("Spam detected.")
        return val

    def clean_form_started_at(self):
        raw = (self.cleaned_data.get("form_started_at") or "").strip()
        try:
            started = int(float(raw))
        except (TypeError, ValueError):
            return raw

        elapsed = time.time() - started
        if elapsed < 3:
            raise forms.ValidationError("Please wait a few seconds before submitting.")
        if elapsed > 24 * 60 * 60:
            raise forms.ValidationError("This form session expired. Please refresh and try again.")
        return raw

    def clean_email(self):
        email = (self.cleaned_data.get("email") or "").strip().lower()
        # Do not block free email addresses, but the view will use this to score lead quality.
        return email

    def clean_website(self):
        website = (self.cleaned_data.get("website") or "").strip()
        if not website:
            return website
        parsed = urlparse(website)
        if parsed.netloc and any(bad in parsed.netloc.lower() for bad in ["searchregister", "googleindex", "seo"]):
            raise forms.ValidationError("Please provide your company website, not a promotional link.")
        return website

    def clean_message(self):
        msg = (self.cleaned_data.get("message") or "").strip()
        if len(msg) < 20:
            raise forms.ValidationError("Please provide a little more detail (at least 20 characters).")
        if len(re.sub(r"\s+", "", msg)) < 12:
            raise forms.ValidationError("Please provide a meaningful message.")
        return msg

    def clean(self):
        cleaned = super().clean()

        method = cleaned.get("contact_method")
        phone = (cleaned.get("phone") or "").strip()

        if method == "phone" and not phone:
            self.add_error("phone", "Please add a phone or WhatsApp number, or choose Email/Video call.")

        return cleaned

    def suspicious_reasons(self):
        """Return reasons that indicate a promotional/spam inquiry.

        We keep this separate from validation so suspicious submissions can be
        silently accepted but not emailed to the inbox.
        """
        if not self.is_valid():
            return ["invalid_form"]

        cd = self.cleaned_data
        text = " ".join([
            cd.get("subject", ""), cd.get("message", ""), cd.get("company_name", ""), cd.get("website", "")
        ]).lower()
        compact = text.replace("-", " ").replace("_", " ")

        reasons = []
        for keyword in SUSPICIOUS_KEYWORDS:
            if keyword in compact:
                reasons.append(f"keyword:{keyword}")

        # Classic bot / lead-seller patterns from the examples you received.
        if cd.get("service_interest") in {"follow_up", "local_presence"} and any(x in compact for x in ["video", "seo", "index", "domain"]):
            reasons.append("service_mismatch_promotion")

        if len(re.findall(r"https?://", compact)) >= 2:
            reasons.append("multiple_links")

        return reasons

    def quality_label(self):
        if not self.is_valid():
            return "Unqualified"
        cd = self.cleaned_data
        score = 0
        if cd.get("company_name"):
            score += 1
        if cd.get("website"):
            score += 1
        if cd.get("country"):
            score += 1
        if cd.get("industry"):
            score += 1
        if cd.get("target_market"):
            score += 1
        if cd.get("budget_range") and cd.get("budget_range") != "not_sure":
            score += 1
        if cd.get("timeline") and cd.get("timeline") != "planning":
            score += 1
        domain = cd.get("email", "").split("@")[-1]
        if domain and domain not in FREE_EMAIL_DOMAINS:
            score += 1
        if len(cd.get("message", "")) > 180:
            score += 1

        if score >= 6:
            return "Qualified"
        if score >= 3:
            return "Needs review"
        return "Low information"
