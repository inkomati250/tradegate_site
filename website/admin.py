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



