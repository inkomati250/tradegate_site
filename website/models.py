from django.db import models
from django.core.validators import MinLengthValidator, URLValidator
from django.core.exceptions import ValidationError
from django.urls import reverse


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SiteSettings(models.Model):
    """
    Singleton-ish site settings (enforced in admin).

    IMPORTANT:
    - We keep your existing fields to avoid breaking templates.
    - We ADD ops-ready fields: structured address + socials.
    - We ADD updated_at to support admin display/read-only and avoid admin errors.
    """

    # --- Brand / header ---
    site_name = models.CharField(max_length=120, default="TradeGate Consultants")
    tagline = models.CharField(max_length=180, blank=True, default="Strategy. Execution. Growth.")

    # Existing contact fields (kept)
    primary_email = models.EmailField(blank=True, default="")
    phone = models.CharField(max_length=40, blank=True, default="")

    # Existing address field (kept so base.html doesn't break)
    address = models.TextField(blank=True, default="")

    # NEW: structured address (optional; can be used in templates later)
    address_line1 = models.CharField(max_length=160, blank=True, default="")
    address_line2 = models.CharField(max_length=160, blank=True, default="")
    postal_code = models.CharField(max_length=20, blank=True, default="")
    city = models.CharField(max_length=80, blank=True, default="")
    country = models.CharField(max_length=80, blank=True, default="Germany")

    # --- Footer socials (NEW) ---
    facebook_url = models.URLField(blank=True, default="", validators=[URLValidator()])
    instagram_url = models.URLField(blank=True, default="", validators=[URLValidator()])
    x_url = models.URLField(blank=True, default="", validators=[URLValidator()])         # Twitter/X
    whatsapp_url = models.URLField(blank=True, default="", validators=[URLValidator()])  # wa.me or api.whatsapp.com

    # Homepage hero (existing)
    hero_title = models.CharField(max_length=120, default="Cross-border growth with clarity.")
    hero_subtitle = models.CharField(
        max_length=220,
        default="We help companies enter markets, build partnerships, and execute with confidence.",
    )
    hero_cta_label = models.CharField(max_length=40, default="Contact us")
    hero_cta_url = models.CharField(max_length=200, default="/contact/")

    # SEO defaults (existing)
    meta_title = models.CharField(max_length=70, blank=True, default="")
    meta_description = models.CharField(max_length=160, blank=True, default="")
    og_image_url = models.URLField(blank=True, default="")

    # Branding colors (existing)
    brand_primary = models.CharField(max_length=20, default="#0B1220")  # deep navy
    brand_accent = models.CharField(max_length=20, default="#C6A15B")   # warm gold
    brand_muted = models.CharField(max_length=20, default="#94A3B8")    # slate-ish

    # ✅ NEW: prevents your admin “updated_at not found” errors
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.site_name or "TradeGate"

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"


class NavigationItem(TimeStampedModel):
    """
    CMS-driven navigation with stable anchor rule.

    - Admin can change label/order/visibility
    - But anchors are controlled so your one-page layout can't break.
    """

    KIND_CHOICES = (
        ("anchor", "Homepage section (#anchor)"),
        ("internal", "Internal page (named URL)"),
        ("external", "External URL"),
    )

    # Keep this list tight to prevent broken layout.
    # Add more anchors only when they exist in home.html.
    ALLOWED_ANCHORS = ["pillars", "services", "process"]

    label = models.CharField(max_length=50)
    kind = models.CharField(max_length=20, choices=KIND_CHOICES, default="anchor")

    # For kind="anchor"
    anchor = models.SlugField(max_length=50, blank=True, default="")

    # For kind="internal" (must match named url patterns)
    url_name = models.CharField(max_length=80, blank=True, default="")

    # For kind="external"
    external_url = models.URLField(blank=True, default="", validators=[URLValidator()])

    is_visible = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=10)

    # Optional: CTA button in nav (e.g. "Book a call")
    is_cta = models.BooleanField(default=False)

    class Meta:
        ordering = ("order", "label")
        verbose_name = "Navigation Item"
        verbose_name_plural = "Navigation"

    def __str__(self):
        return self.label

    def clean(self):
        # Enforce stable anchors
        if self.kind == "anchor":
            if not self.anchor:
                raise ValidationError({"anchor": "Anchor is required when kind = anchor."})
            if self.anchor not in self.ALLOWED_ANCHORS:
                raise ValidationError(
                    {"anchor": f"Anchor must be one of: {', '.join(self.ALLOWED_ANCHORS)}"}
                )

        if self.kind == "internal" and not self.url_name:
            raise ValidationError({"url_name": "url_name is required when kind = internal."})

        if self.kind == "external" and not self.external_url:
            raise ValidationError({"external_url": "external_url is required when kind = external."})

        # Only one CTA item at a time
        if self.is_cta:
            qs = NavigationItem.objects.filter(is_cta=True)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            if qs.exists():
                raise ValidationError({"is_cta": "Only one NavigationItem can be CTA at a time."})

    def get_href(self):
        if self.kind == "anchor" and self.anchor:
            return f"/#{self.anchor}"
        if self.kind == "internal" and self.url_name:
            try:
                return reverse(self.url_name)
            except Exception:
                return "/"
        if self.kind == "external" and self.external_url:
            return self.external_url
        return "/"


class Service(TimeStampedModel):
    title = models.CharField(max_length=120)
    short_description = models.CharField(max_length=220)
    icon = models.CharField(max_length=40, blank=True, default="Briefcase")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["order", "title"]


class Industry(TimeStampedModel):
    name = models.CharField(max_length=120)
    short_description = models.CharField(max_length=220, blank=True, default="")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["order", "name"]
        verbose_name_plural = "Industries"


class ProcessStep(TimeStampedModel):
    title = models.CharField(max_length=120)
    description = models.CharField(max_length=240)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.order}. {self.title}"

    class Meta:
        ordering = ["order"]


class LegalPage(TimeStampedModel):
    """
    Two records: impressum, datenschutz (but can support more).
    """
    KEY_CHOICES = (
        ("impressum", "Impressum"),
        ("datenschutz", "Datenschutz"),
    )

    key = models.CharField(max_length=40, choices=KEY_CHOICES, unique=True)
    title = models.CharField(max_length=120)
    content = models.TextField(
        validators=[MinLengthValidator(20)],
        help_text="You can paste formatted text here.",
    )
    meta_title = models.CharField(max_length=70, blank=True, default="")
    meta_description = models.CharField(max_length=160, blank=True, default="")

    def __str__(self):
        return self.get_key_display()

    def get_absolute_url(self):
        return reverse("legal_page", kwargs={"key": self.key})

    class Meta:
        ordering = ["key"]


class Inquiry(TimeStampedModel):
    full_name = models.CharField(max_length=120)
    email = models.EmailField()
    subject = models.CharField(max_length=160)
    message = models.TextField(validators=[MinLengthValidator(10)])

    company_name = models.CharField(max_length=160, blank=True, default="")
    website = models.URLField(blank=True, default="")
    country = models.CharField(max_length=80, blank=True, default="")
    service_interest = models.CharField(max_length=40, blank=True, default="")
    timeline = models.CharField(max_length=40, blank=True, default="")
    budget_range = models.CharField(max_length=40, blank=True, default="")
    contact_method = models.CharField(max_length=20, blank=True, default="")
    phone = models.CharField(max_length=40, blank=True, default="")
    consent = models.BooleanField(default=False)

    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.CharField(max_length=255, blank=True, default="")

    is_handled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.full_name} — {self.subject}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Inquiries"



