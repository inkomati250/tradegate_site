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
    full_name = forms.CharField(
        label="Full name",
        max_length=120,
        widget=forms.TextInput(attrs={"placeholder": "Your name"})
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"placeholder": "you@company.com"})
    )

    company_name = forms.CharField(
        label="Company (optional)",
        required=False,
        max_length=160,
        widget=forms.TextInput(attrs={"placeholder": "Company / Organization"})
    )
    website = forms.URLField(
        label="Website (optional)",
        required=False,
        widget=forms.URLInput(attrs={"placeholder": "https://…"})
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
        label="Timeline",
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
        label="Preferred contact method",
        choices=CONTACT_METHOD_CHOICES,
        widget=forms.RadioSelect(),
        required=False,
        initial="email",
    )

    phone = forms.CharField(
        label="Phone / WhatsApp (optional)",
        required=False,
        max_length=40,
        widget=forms.TextInput(attrs={"placeholder": "+49 …"})
    )

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

    consent = forms.BooleanField(
        label="I agree that TradeGate may store my message to respond to my request (GDPR).",
        required=True
    )

    def clean(self):
        cleaned = super().clean()
        # If they pick phone/whatsapp but provide no phone, nudge them.
        method = cleaned.get("contact_method")
        phone = (cleaned.get("phone") or "").strip()
        if method == "phone" and not phone:
            self.add_error("phone", "Please add a phone/WhatsApp number, or choose Email/Video call.")
        return cleaned
