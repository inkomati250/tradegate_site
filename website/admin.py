from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import (
    SiteSettings,
    NavigationItem,
    Service,
    Industry,
    ProcessStep,
    LegalPage,
    TradeFairOpportunity,
    TradeFair,
    ServicePackage,
    TeamProfile,
    Inquiry,
)

# -------------------------
# Hide clutter you don't use
# -------------------------
# Keep sites framework installed, but remove it from admin to reduce confusion
try:
    admin.site.unregister(Site)
except admin.sites.NotRegistered:
    pass

try:
    admin.site.unregister(Group)
except admin.sites.NotRegistered:
    pass


# =========================
# 1) Site Settings (Singleton)
# =========================
@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """
    True singleton-style admin:
    - Only 1 SiteSettings row exists
    - No delete
    - Clicking 'Site Settings' goes straight to edit view
    """
    list_display = ("site_name", "primary_email", "phone", "updated_at")
    readonly_fields = ("updated_at",)

    fieldsets = (
        ("Brand", {"fields": ("site_name", "tagline", "brand_primary", "brand_accent", "brand_muted")}),
        ("Contact", {"fields": ("primary_email", "phone")}),
        ("Address (optional)", {"fields": ("address", "address_line1", "address_line2", "postal_code", "city", "country")}),
        ("Social links (footer)", {"fields": ("facebook_url", "instagram_url", "x_url", "whatsapp_url")}),
        ("Homepage hero", {"fields": ("hero_title", "hero_subtitle", "hero_cta_label", "hero_cta_url")}),
        ("SEO defaults", {"fields": ("meta_title", "meta_description", "og_image_url")}),
        ("System", {"fields": ("updated_at",)}),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = SiteSettings.objects.first()
        if obj:
            url = reverse("admin:website_sitesettings_change", args=(obj.pk,))
            return HttpResponseRedirect(url)
        return super().changelist_view(request, extra_context=extra_context)


# =========================
# 2) Navigation (CMS-driven)
# =========================
@admin.register(NavigationItem)
class NavigationItemAdmin(admin.ModelAdmin):
    list_display = ("order", "label", "kind", "is_visible", "is_cta", "updated_at")
    list_display_links = ("label",)  # ✅ fixes admin.E124 with list_editable
    list_editable = ("order", "is_visible", "is_cta")
    list_filter = ("kind", "is_visible", "is_cta")
    search_fields = ("label", "anchor", "url_name", "external_url")
    ordering = ("order", "label")
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Display", {"fields": ("label", "order", "is_visible", "is_cta")}),
        ("Link target", {"fields": ("kind", "anchor", "url_name", "external_url")}),
        ("System", {"fields": ("created_at", "updated_at")}),
    )


# =========================
# 3) Services / Industries / Process Steps
# =========================
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("order", "title", "is_active", "updated_at")
    list_display_links = ("title",)
    list_editable = ("order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("title", "short_description")
    ordering = ("order", "title")


@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):
    list_display = ("order", "name", "is_active", "updated_at")
    list_display_links = ("name",)
    list_editable = ("order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "short_description")
    ordering = ("order", "name")


@admin.register(ProcessStep)
class ProcessStepAdmin(admin.ModelAdmin):
    list_display = ("order", "title", "updated_at")
    list_display_links = ("title",)
    list_editable = ("order",)
    search_fields = ("title", "description")
    ordering = ("order",)


# =========================
# 4) Legal Pages
# =========================
@admin.register(LegalPage)
class LegalPageAdmin(admin.ModelAdmin):
    list_display = ("key", "title", "updated_at")
    list_display_links = ("key",)
    search_fields = ("key", "title", "content")
    ordering = ("key",)

    # ✅ add this
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Identity", {"fields": ("key", "title")}),
        ("Content", {"fields": ("content",)}),
        ("SEO", {"fields": ("meta_title", "meta_description")}),
        ("System", {"fields": ("created_at", "updated_at")}),
    )

    def save_model(self, request, obj, form, change):
        if not change and LegalPage.objects.filter(key=obj.key).exists():
            raise ValidationError("This legal page key already exists. Please edit the existing page.")
        super().save_model(request, obj, form, change)



# =========================
# 4b) Trade fair / market opportunity carousel
# =========================
class TradeFairOpportunityAdmin(admin.ModelAdmin):
    list_display = ("order", "title", "city_country", "industry", "is_active", "updated_at")
    list_display_links = ("title",)
    list_editable = ("order", "is_active")
    list_filter = ("is_active", "industry")
    search_fields = ("title", "city_country", "industry", "summary")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at")
    ordering = ("order", "title")

    fieldsets = (
        ("Opportunity", {"fields": ("title", "slug", "city_country", "date_label", "industry", "summary")}),
        ("Visual", {"fields": ("image", "image_url", "visual_label")}),
        ("Call to action", {"fields": ("cta_label", "cta_url")}),
        ("Display", {"fields": ("order", "is_active")}),
        ("System", {"fields": ("created_at", "updated_at")}),
    )


# =========================
# 5) Inquiries (Ops-ready)
# =========================
@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ("created_at", "full_name", "email", "subject", "is_handled")
    list_filter = ("is_handled", "created_at")
    search_fields = ("full_name", "email", "subject", "message", "company_name", "country")
    readonly_fields = ("created_at", "updated_at", "ip_address", "user_agent")
    list_editable = ("is_handled",)
    date_hierarchy = "created_at"
    ordering = ("-created_at",)

    actions = ("mark_handled", "mark_unhandled")

    fieldsets = (
        ("Status", {"fields": ("is_handled",)}),
        ("Contact", {"fields": ("full_name", "email", "phone", "contact_method")}),
        ("Company", {"fields": ("company_name", "website", "country")}),
        ("Request", {"fields": ("service_interest", "timeline", "budget_range")}),
        ("Message", {"fields": ("subject", "message", "consent")}),
        ("System", {"fields": ("created_at", "updated_at", "ip_address", "user_agent")}),
    )

    @admin.action(description="Mark selected inquiries as handled")
    def mark_handled(self, request, queryset):
        queryset.update(is_handled=True)

    @admin.action(description="Mark selected inquiries as NOT handled")
    def mark_unhandled(self, request, queryset):
        queryset.update(is_handled=False)





@admin.register(TradeFair)
class TradeFairAdmin(admin.ModelAdmin):
    list_display = ("name", "kind", "start_date", "end_date", "city", "is_published", "show_in_carousel")
    list_filter = ("kind", "is_published", "show_in_carousel", "country")
    list_editable = ("is_published", "show_in_carousel")
    search_fields = ("name", "city", "sectors", "organiser")
    prepopulated_fields = {"slug": ("name",)}
    fieldsets = (
        ("Event", {"fields": ("name", "slug", "kind", "is_published", "show_in_carousel", "order")}),
        ("When and where", {"fields": ("start_date", "end_date", "date_note", "city", "country", "venue", "organiser", "official_url")}),
        ("Content (our own words)", {"fields": ("sectors", "summary", "description", "who_should_exhibit", "who_should_visit", "how_we_help")}),
        ("Partner events only: role and permission", {
            "description": "Only tick 'materials permission' once the organiser has confirmed in writing that we may show their event, logo and materials. Partner events stay hidden on the website until both 'materials permission' and 'published' are ticked.",
            "fields": ("our_role", "materials_permission"),
        }),
        ("Partner events only: logo and banner", {
            "description": "Cover image = the organiser's official banner (wide image, about 1600 × 600 px). While it is empty, the website shows a branded placeholder with the event logo, dates and an 'Official banner coming soon' ribbon. Upload the banner here and it replaces the placeholder automatically.",
            "fields": ("logo", "cover_image", "brochure"),
        }),
        ("Partner events only: prices and packages", {
            "description": "Type the packages as figures (one per line: Name | Price | Details), upload the organiser's price list as an image, or both.",
            "fields": ("packages_text", "packages_image", "packages_note"),
        }),
    )
    list_display = ("name", "kind", "start_date", "city", "is_published", "materials_permission", "show_in_carousel")


@admin.register(ServicePackage)
class ServicePackageAdmin(admin.ModelAdmin):
    list_display = ("name", "service_slug", "price", "unit", "featured", "is_active", "order")
    list_filter = ("service_slug", "featured", "is_active")
    list_editable = ("price", "featured", "is_active", "order")
    search_fields = ("name", "service_slug")

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == "service_slug":
            from django import forms
            from .content import SERVICE_PAGES
            choices = [(slug, page["title"]) for slug, page in SERVICE_PAGES.items() if page.get("audience") != "organisers"]
            return forms.ChoiceField(choices=choices, label="Service page")
        return super().formfield_for_dbfield(db_field, request, **kwargs)


@admin.register(TeamProfile)
class TeamProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "location", "is_active", "order")
    list_editable = ("is_active", "order")
    fieldsets = (
        (None, {"fields": ("name", "role", "location", "is_active", "order")}),
        ("Photo", {"fields": ("photo", "photo_url"), "description": "The photo is shown view-only on the website (no right-click or long-press saving)."}),
        ("Text", {"fields": ("intro", "partners_text", "background", "linkedin_url")}),
    )


# -------------------------
# Admin branding, sections and dashboard
# -------------------------
admin.site.site_header = "TradeGate Admin"
admin.site.site_title = "TradeGate Admin"
admin.site.index_title = "Dashboard"
admin.site.index_template = "admin/tradegate_index.html"

ADMIN_SECTIONS = [
    ("Enquiries", "enquiries", ["Inquiry"]),
    ("Trade fairs", "trade-fairs", ["TradeFair"]),
    ("Services and prices", "services", ["ServicePackage", "Service", "Industry", "ProcessStep"]),
    ("Team and company", "company", ["TeamProfile", "SiteSettings"]),
    ("Website structure", "structure", ["NavigationItem", "LegalPage"]),
]


def _tradegate_app_list(request, app_label=None):
    original = admin.AdminSite.get_app_list(admin.site, request, app_label)
    if app_label:
        return original
    models_by_name = {}
    others = []
    for app in original:
        for model in app["models"]:
            if app["app_label"] == "website":
                models_by_name[model["object_name"]] = model
            else:
                others.append(model)
    sections = []
    for title, label, names in ADMIN_SECTIONS:
        models = [models_by_name.pop(n) for n in names if n in models_by_name]
        if models:
            sections.append({"name": title, "app_label": "website", "app_url": models[0]["admin_url"], "has_module_perms": True, "models": models})
    leftover = list(models_by_name.values())
    if leftover:
        sections.append({"name": "Other content", "app_label": "website", "app_url": leftover[0]["admin_url"], "has_module_perms": True, "models": leftover})
    if others:
        sections.append({"name": "Users and access", "app_label": "auth", "app_url": others[0]["admin_url"], "has_module_perms": True, "models": others})
    return sections


admin.site.get_app_list = _tradegate_app_list

_original_index = admin.site.index


def _tradegate_index(request, extra_context=None):
    from django.utils import timezone
    today = timezone.localdate()
    context = {}
    try:
        context = {
            "tg_new_enquiries": Inquiry.objects.filter(is_handled=False).count(),
            "tg_recent_enquiries": Inquiry.objects.filter(is_handled=False).order_by("-created_at")[:5],
            "tg_upcoming_fairs": TradeFair.objects.filter(is_published=True).exclude(end_date__lt=today).count(),
            "tg_partner_waiting": TradeFair.objects.filter(kind=TradeFair.KIND_REPRESENTED, is_published=False).count(),
        }
    except Exception:
        pass
    context.update(extra_context or {})
    return _original_index(request, context)


admin.site.index = _tradegate_index
