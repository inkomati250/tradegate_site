from django.db import models
from django.core.validators import FileExtensionValidator, MinLengthValidator, URLValidator
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
    ALLOWED_ANCHORS = ["pillars", "services", "opportunities", "process"]

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


class TradeFairOpportunity(TimeStampedModel):
    """
    Homepage/admin carousel for trade fair and market-access opportunities.

    It is intentionally lightweight: uploaded images are optional and an
    external image URL can be used as a fallback. If no records exist yet,
    views.py shows safe example opportunity cards instead of pretending they
    are completed TradeGate events.
    """

    title = models.CharField(max_length=140)
    slug = models.SlugField(max_length=160, unique=True)
    city_country = models.CharField(max_length=120, blank=True, default="")
    date_label = models.CharField(max_length=120, blank=True, default="")
    industry = models.CharField(max_length=140, blank=True, default="")
    summary = models.CharField(max_length=260)
    image = models.FileField(upload_to="event-opportunities/", blank=True, default="")
    image_url = models.URLField(blank=True, default="", validators=[URLValidator()])
    visual_label = models.CharField(max_length=20, blank=True, default="")
    cta_label = models.CharField(max_length=60, default="Request representation")
    cta_url = models.CharField(max_length=220, default="/contact/?service=trade_fair#contact-form")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def display_image_url(self):
        if self.image:
            try:
                return self.image.url
            except Exception:
                pass
        return self.image_url

    class Meta:
        ordering = ["order", "title"]
        verbose_name = "Trade Fair / Market Opportunity"
        verbose_name_plural = "Trade Fair & Market Opportunities"


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





class TradeFair(TimeStampedModel):
    """
    Trade fair calendar entry.

    Two kinds:
    - "represented": events TradeGate recruits exhibitors for, shown only
      after the organiser has given written permission (is_published).
    - "germany": major German trade fairs listed for information, with our
      own short description and a link to the organiser's official site.
    """

    KIND_REPRESENTED = "represented"
    KIND_GERMANY = "germany"
    KIND_CHOICES = [
        (KIND_REPRESENTED, "Event we recruit exhibitors for"),
        (KIND_GERMANY, "German trade fair (information listing)"),
    ]

    name = models.CharField(max_length=140)
    slug = models.SlugField(max_length=160, unique=True)
    kind = models.CharField(max_length=20, choices=KIND_CHOICES, default=KIND_GERMANY)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    date_note = models.CharField(
        max_length=120, blank=True, default="",
        help_text="Optional, e.g. 'Dates to be confirmed by the organiser'.",
    )
    city = models.CharField(max_length=80, blank=True, default="")
    country = models.CharField(max_length=80, blank=True, default="Germany")
    venue = models.CharField(max_length=160, blank=True, default="")
    organiser = models.CharField(max_length=160, blank=True, default="")
    sectors = models.CharField(max_length=220, blank=True, default="", help_text="Comma-separated.")
    summary = models.CharField(max_length=260, help_text="One or two sentences in our own words.")
    description = models.TextField(blank=True, default="", help_text="Our own words. Do not copy the organiser's text.")
    who_should_exhibit = models.TextField(blank=True, default="", help_text="One item per line.")
    who_should_visit = models.TextField(blank=True, default="", help_text="One item per line.")
    how_we_help = models.TextField(blank=True, default="", help_text="One item per line.")
    our_role = models.CharField(
        max_length=160, blank=True, default="",
        help_text="Represented events only, exactly as the agreement allows, e.g. 'Exhibitor recruitment partner for Germany'.",
    )
    official_url = models.URLField(blank=True, default="", validators=[URLValidator()])

    # Partner event materials (supplied by the organiser, used with permission)
    materials_permission = models.BooleanField(
        default=False,
        help_text="Partner events: the organiser has given written permission to show the event name, logo and materials on our website.",
    )
    logo = models.FileField(upload_to="trade-fairs/logos/", blank=True, default="", validators=[FileExtensionValidator(["png", "jpg", "jpeg", "webp", "svg"])])
    cover_image = models.FileField(upload_to="trade-fairs/covers/", blank=True, default="", validators=[FileExtensionValidator(["png", "jpg", "jpeg", "webp"])])
    brochure = models.FileField(upload_to="trade-fairs/brochures/", blank=True, default="", validators=[FileExtensionValidator(["pdf"])], help_text="PDF from the organiser, e.g. exhibitor brochure.")
    packages_text = models.TextField(
        blank=True, default="",
        help_text="Stand and sponsorship packages, one per line: Name | Price | Short description",
    )
    packages_image = models.FileField(
        upload_to="trade-fairs/packages/", blank=True, default="",
        validators=[FileExtensionValidator(["png", "jpg", "jpeg", "webp"])],
        help_text="Optional: the organiser's price list as an image (e.g. a brochure page). Shown with or instead of the package list.",
    )
    packages_note = models.CharField(
        max_length=260, blank=True,
        default="Prices are set by the organiser. Our fee is paid by the organiser, so booking through us does not add to your price.",
        help_text="Short note shown under the packages (currency, VAT, validity).",
    )

    is_published = models.BooleanField(
        default=False,
        help_text="Partner events: tick only once the organiser has given written permission to list the event.",
    )
    show_in_carousel = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["start_date", "order", "name"]
        verbose_name = "Trade fair (calendar)"
        verbose_name_plural = "Trade fair calendar"

    def __str__(self):
        return self.name

    @property
    def is_represented(self):
        return self.kind == self.KIND_REPRESENTED

    @property
    def sector_list(self):
        return [s.strip() for s in self.sectors.split(",") if s.strip()]

    def _lines(self, value):
        return [line.strip(" -•\t") for line in value.splitlines() if line.strip(" -•\t")]

    @property
    def exhibit_list(self):
        return self._lines(self.who_should_exhibit)

    @property
    def visit_list(self):
        return self._lines(self.who_should_visit)

    @property
    def help_list(self):
        return self._lines(self.how_we_help)

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.kind == self.KIND_REPRESENTED and self.is_published and not self.materials_permission:
            raise ValidationError({"is_published": "Partner events can only be published after the organiser's written permission is recorded (tick 'materials permission')."})

    @property
    def package_list(self):
        rows = []
        for line in self.packages_text.splitlines():
            parts = [p.strip() for p in line.split("|")]
            if parts and parts[0]:
                rows.append({"name": parts[0], "price": parts[1] if len(parts) > 1 else "", "details": parts[2] if len(parts) > 2 else ""})
        return rows

    @property
    def date_label(self):
        if not self.start_date:
            return self.date_note or "Dates to be announced"
        s, e = self.start_date, self.end_date or self.start_date
        if s == e:
            return s.strftime("%-d %B %Y")
        if s.year == e.year and s.month == e.month:
            return f"{s.day}–{e.day} {e.strftime('%B %Y')}"
        if s.year == e.year:
            return f"{s.strftime('%-d %B')} – {e.strftime('%-d %B %Y')}"
        return f"{s.strftime('%-d %B %Y')} – {e.strftime('%-d %B %Y')}"

    @property
    def has_official_banner(self):
        return bool(self.cover_image) and self.materials_permission

    @property
    def show_logo(self):
        return bool(self.logo) and (self.materials_permission or not self.is_represented)

    @property
    def place_label(self):
        return ", ".join([p for p in [self.city, self.country] if p])



class ServicePackage(TimeStampedModel):
    """Packages and prices shown on each service page. Editable in admin."""

    service_slug = models.SlugField(max_length=160, help_text="Which service page this package belongs to.")
    name = models.CharField(max_length=80)
    price = models.CharField(max_length=40, help_text="e.g. '€490', 'From €890', 'By quote'.")
    unit = models.CharField(max_length=80, blank=True, default="", help_text="e.g. 'one-off', 'per month, minimum 3 months'.")
    best_for = models.CharField(max_length=120, blank=True, default="")
    includes = models.TextField(blank=True, default="", help_text="One item per line.")
    featured = models.BooleanField(default=False, help_text="Highlight as 'Most chosen'.")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["service_slug", "order", "pk"]
        verbose_name = "Service package"
        verbose_name_plural = "Service packages and prices"

    def __str__(self):
        return f"{self.name} ({self.price})"

    @property
    def include_list(self):
        return [line.strip(" -•\t") for line in self.includes.splitlines() if line.strip(" -•\t")]


class TeamProfile(TimeStampedModel):
    """People shown on the About page."""

    name = models.CharField(max_length=120)
    role = models.CharField(max_length=120, blank=True, default="")
    location = models.CharField(max_length=120, blank=True, default="")
    photo = models.FileField(upload_to="team/", blank=True, default="", validators=[FileExtensionValidator(["png", "jpg", "jpeg", "webp"])], help_text="Shown view-only. Upload a web-size image (about 600 x 600 px).")
    photo_url = models.CharField(max_length=220, blank=True, default="", help_text="Used when no photo is uploaded.")
    linkedin_url = models.URLField(blank=True, default="")
    intro = models.TextField(blank=True, default="")
    partners_text = models.TextField(blank=True, default="", help_text="Short note on the partner network.")
    background = models.TextField(blank=True, default="")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "pk"]
        verbose_name = "Team profile"
        verbose_name_plural = "Team (About page)"

    def __str__(self):
        return self.name

    @property
    def display_photo_url(self):
        if self.photo:
            try:
                return self.photo.url
            except Exception:
                pass
        return self.photo_url
