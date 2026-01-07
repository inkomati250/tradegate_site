from django.contrib import admin
from django.core.exceptions import ValidationError

from .models import SiteSettings, Service, Industry, ProcessStep, LegalPage, Inquiry


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("site_name", "primary_email", "phone")

    def has_add_permission(self, request):
        # only allow one
        if SiteSettings.objects.exists():
            return False
        return True


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "order", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("title", "short_description")
    list_editable = ("is_active", "order")


@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "order", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("name", "short_description")
    list_editable = ("is_active", "order")


@admin.register(ProcessStep)
class ProcessStepAdmin(admin.ModelAdmin):
    list_display = ("order", "title", "updated_at")
    list_editable = ("order",)
    # Django admin requires a clickable field when the first column is editable.
    # Make "title" the link to the change form.
    list_display_links = ("title",)
    search_fields = ("title", "description")


@admin.register(LegalPage)
class LegalPageAdmin(admin.ModelAdmin):
    list_display = ("key", "title", "updated_at")
    search_fields = ("key", "title", "content")

    def save_model(self, request, obj, form, change):
        # enforce one per key
        if not change and LegalPage.objects.filter(key=obj.key).exists():
            raise ValidationError("This legal page already exists.")
        super().save_model(request, obj, form, change)


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "subject", "created_at", "is_handled")
    list_filter = ("is_handled", "created_at")
    search_fields = ("full_name", "email", "subject", "message")
    readonly_fields = ("created_at", "updated_at", "ip_address", "user_agent")
    list_editable = ("is_handled",)
