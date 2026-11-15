from django.urls import path
from . import views

urlpatterns = [
    # Homepage (root, canonical)
    path("", views.home, name="home"),

    # Core pages
    path("about/", views.about, name="about"),
    path("faq/", views.faq, name="faq"),
    path("contact/", views.contact, name="contact"),
    path("partner-hub/", views.partner_pool, name="partner_pool"),

    # Trade fair calendar
    path("trade-fairs/", views.trade_fairs, name="trade_fairs"),
    path("trade-fairs/<slug:slug>/", views.trade_fair_detail, name="trade_fair_detail"),
    path("trade-fairs/<slug:slug>/calendar.ics", views.trade_fair_ics, name="trade_fair_ics"),

    # SEO service landing pages
    path("services/<slug:slug>/", views.service_landing, name="service_landing"),

    # Legal pages (Impressum, Datenschutz, etc.)
    path("legal/<slug:key>/", views.legal_page, name="legal_page"),
]
