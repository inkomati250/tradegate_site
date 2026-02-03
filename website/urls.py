from django.urls import path
from . import views

urlpatterns = [
    # Homepage (root, canonical)
    path("", views.home, name="home"),

    # Core pages
    path("about/", views.about, name="about"),
    path("faq/", views.faq, name="faq"),
    path("contact/", views.contact, name="contact"),

    # Legal pages (Impressum, Datenschutz, etc.)
    # Kept exactly as legal_page.html expects
    path("legal/<slug:key>/", views.legal_page, name="legal_page"),
]


