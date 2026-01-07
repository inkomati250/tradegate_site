from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("contact/", views.contact, name="contact"),
    path("legal/<slug:key>/", views.legal_page, name="legal_page"),
    path("about/", views.about, name="about"),
    path("faq/", views.faq, name="faq"),
]

