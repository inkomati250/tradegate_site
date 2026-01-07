from django.db import models
from django.core.validators import MinLengthValidator
from django.urls import reverse


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SiteSettings(models.Model):
    """
    Singleton-ish site settings.
    We'll enforce in admin (only one record).
    """
    site_name = models.CharField(max_length=120, default="TradeGate Consultants")
    tagline = models.CharField(max_length=180, blank=True, default="Strategy. Execution. Growth.")
    primary_email = models.EmailField(blank=True, default="")
    phone = models.CharField(max_length=40, blank=True, default="")
    address = models.TextField(blank=True, default="")

    # Homepage hero
    hero_title = models.CharField(max_length=120, default="Cross-border growth with clarity.")
    hero_subtitle = models.CharField(
        max_length=220,
        default="We help companies enter markets, build partnerships, and execute with confidence."
    )
    hero_cta_label = models.CharField(max_length=40, default="Contact us")
    hero_cta_url = models.CharField(max_length=200, default="/contact/")

    # SEO defaults
    meta_title = models.CharField(max_length=70, blank=True, default="")
    meta_description = models.CharField(max_length=160, blank=True, default="")
    og_image_url = models.URLField(blank=True, default="")

    # Branding colors (optional hooks)
    brand_primary = models.CharField(max_length=20, default="#0B1220")     # deep navy
    brand_accent = models.CharField(max_length=20, default="#C6A15B")      # warm gold
    brand_muted = models.CharField(max_length=20, default="#94A3B8")       # slate-ish

    def __str__(self):
        return self.site_name

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"


class Service(TimeStampedModel):
    title = models.CharField(max_length=120)
    short_description = models.CharField(max_length=220)
    icon = models.CharField(max_length=40, blank=True, default="Briefcase")  # optional label
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
    content = models.TextField(validators=[MinLengthValidator(20)], help_text="You can paste formatted text here.")
    meta_title = models.CharField(max_length=70, blank=True, default="")
    meta_description = models.CharField(max_length=160, blank=True, default="")

    def __str__(self):
        return self.get_key_display()

    def get_absolute_url(self):
        return reverse("legal_page", kwargs={"key": self.key})

    class Meta:
        ordering = ["key"]


class Inquiry(TimeStampedModel):
    # Core fields (existing)
    full_name = models.CharField(max_length=120)
    email = models.EmailField()
    subject = models.CharField(max_length=160)
    message = models.TextField(validators=[MinLengthValidator(10)])

    # NEW: professional lead capture fields
    company_name = models.CharField(max_length=160, blank=True, default="")
    website = models.URLField(blank=True, default="")
    country = models.CharField(max_length=80, blank=True, default="")
    service_interest = models.CharField(max_length=40, blank=True, default="")
    timeline = models.CharField(max_length=40, blank=True, default="")
    budget_range = models.CharField(max_length=40, blank=True, default="")
    contact_method = models.CharField(max_length=20, blank=True, default="")
    phone = models.CharField(max_length=40, blank=True, default="")
    consent = models.BooleanField(default=False)

    # Technical meta (existing)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.CharField(max_length=255, blank=True, default="")

    is_handled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.full_name} — {self.subject}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Inquiries"
