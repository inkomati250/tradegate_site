from django.urls import path
from . import views

urlpatterns = [
    # Homepage (root, canonical)
    path("", views.home, name="home"),

    # Core pages
    path("about/", views.about, name="about"),
    path("faq/", views.faq, name="faq"),
    path("contact/", views.contact, name="contact"),

    # SEO service landing pages
    path("services/<slug:slug>/", views.service_landing, name="service_landing"),

    # Legal pages (Impressum, Datenschutz, etc.)
    path("legal/<slug:key>/", views.legal_page, name="legal_page"),
]
