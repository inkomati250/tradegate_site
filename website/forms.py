from django import forms

SERVICE_CHOICES = [
    ("trade_fair", "Trade fair & event representation"),
    ("scouting", "Market entry & partner scouting"),
    ("local_presence", "Local presence without an office"),
    ("follow_up", "Relationship & follow-up management"),
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


class InquiryForm(forms.Form):
    website_url = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "autocomplete": "off",
            "tabindex": "-1",
        })
    )

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
        label="Email",
        error_messages={
            "required": "Please enter your email address.",
            "invalid": "Please enter a valid email address.",
        },
        widget=forms.EmailInput(attrs={
            "placeholder": "you@company.com",
            "autocomplete": "email",
        }),
    )

    company_name = forms.CharField(
        label="Company (optional)",
        required=False,
        max_length=160,
        widget=forms.TextInput(attrs={
            "placeholder": "Company / Organization",
            "autocomplete": "organization",
        }),
    )

    website = forms.URLField(
        label="Website (optional)",
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
        label="Country / Region (optional)",
        required=False,
        max_length=80,
        widget=forms.TextInput(attrs={
            "placeholder": "e.g., Rwanda, UAE, India",
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
            "placeholder": "Tell us what you want to achieve, your product/service, target customers, and any upcoming trade fairs or meetings.",
        }),
    )

    consent = forms.BooleanField(
        label="I agree that TradeGate may store my message to respond to my request (GDPR).",
        required=True,
        error_messages={
            "required": "Consent is required to submit this form.",
        },
    )

    def clean_website_url(self):
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

        if method == "phone" and not phone:
            self.add_error("phone", "Please add a phone or WhatsApp number, or choose Email/Video call.")

        return cleaned