from django import forms

SERVICE_CHOICES = [
    ("trade_fair", "Trade fair & event representation"),
    ("scouting", "Market entry & partner scouting"),
    ("local_presence", "Local presence without an office"),
    ("follow_up", "Relationship & follow-up management"),
    ("other", "Other / Not sure yet"),
]

TIMELINE_CHOICES = [
    ("asap", "ASAP (0–2 weeks)"),
    ("2_4_weeks", "2–4 weeks"),
    ("1_3_months", "1–3 months"),
    ("3_6_months", "3–6 months"),
    ("planning", "Just planning / researching"),
]

BUDGET_CHOICES = [
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


class InquiryForm(forms.Form):
    # ---------------------------
    # Anti-spam honeypot
    # (hidden field that humans won't fill)
    # ---------------------------
    website_url = forms.CharField(required=False, widget=forms.TextInput(attrs={"autocomplete": "off"}))

    # ---------------------------
    # Required contact fields
    # ---------------------------
    full_name = forms.CharField(
        label="Full name",
        max_length=120,
        widget=forms.TextInput(attrs={"placeholder": "Your name", "autocomplete": "name"})
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"placeholder": "you@company.com", "autocomplete": "email"})
    )

    # ---------------------------
    # Optional details
    # ---------------------------
    company_name = forms.CharField(
        label="Company (optional)",
        required=False,
        max_length=160,
        widget=forms.TextInput(attrs={"placeholder": "Company / Organization", "autocomplete": "organization"})
    )
    website = forms.URLField(
        label="Website (optional)",
        required=False,
        widget=forms.URLInput(attrs={"placeholder": "https://…", "autocomplete": "url"})
    )

    country = forms.CharField(
        label="Country / Region (optional)",
        required=False,
        max_length=80,
        widget=forms.TextInput(attrs={"placeholder": "e.g., Rwanda, UAE, India"})
    )

    service_interest = forms.ChoiceField(
        label="What do you need?",
        choices=SERVICE_CHOICES,
        widget=forms.Select(),
    )

    timeline = forms.ChoiceField(
        label="Timeline (optional)",
        choices=TIMELINE_CHOICES,
        widget=forms.Select(),
        required=False,
    )

    budget_range = forms.ChoiceField(
        label="Budget range (optional)",
        choices=BUDGET_CHOICES,
        widget=forms.Select(),
        required=False,
    )

    contact_method = forms.ChoiceField(
        label="Preferred contact method (optional)",
        choices=CONTACT_METHOD_CHOICES,
        widget=forms.RadioSelect(),
        required=False,
        initial="email",
    )

    phone = forms.CharField(
        label="Phone / WhatsApp (optional)",
        required=False,
        max_length=40,
        widget=forms.TextInput(attrs={"placeholder": "+49 …", "autocomplete": "tel"})
    )

    # ---------------------------
    # Message (required)
    # ---------------------------
    subject = forms.CharField(
        label="Subject",
        max_length=140,
        widget=forms.TextInput(attrs={"placeholder": "Short subject"})
    )

    message = forms.CharField(
        label="Project details",
        widget=forms.Textarea(attrs={
            "rows": 6,
            "placeholder": "Tell us what you want to achieve, your product/service, target customers, and any upcoming trade fairs or meetings."
        })
    )

    # ---------------------------
    # Consent (required)
    # ---------------------------
    consent = forms.BooleanField(
        label="I agree that TradeGate may store my message to respond to my request (GDPR).",
        required=True,
        error_messages={"required": "Consent is required to submit this form."}
    )

    # ---------------------------
    # Validation
    # ---------------------------
    def clean_website_url(self):
        # Honeypot should stay empty
        val = (self.cleaned_data.get("website_url") or "").strip()
        if val:
            raise forms.ValidationError("Spam detected.")
        return val

    def clean_message(self):
        msg = (self.cleaned_data.get("message") or "").strip()
        if len(msg) < 10:
            raise forms.ValidationError("Please provide a little more detail (at least 10 characters).")
        return msg

    def clean(self):
        cleaned = super().clean()

        method = cleaned.get("contact_method")
        phone = (cleaned.get("phone") or "").strip()

        # If they pick phone, require number
        if method == "phone" and not phone:
            self.add_error("phone", "Please add a phone/WhatsApp number, or choose Email/Video call.")

        return cleaned
