from django.test import TestCase
from django.urls import reverse

from .content import SERVICE_NAV, SERVICE_PAGES


class ServicePagesTests(TestCase):
    def test_every_service_page_renders_details(self):
        for slug, page in SERVICE_PAGES.items():
            with self.subTest(slug=slug):
                response = self.client.get(reverse("service_landing", kwargs={"slug": slug}))
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, "What we need from you")
                self.assertContains(response, "What is not included")

    def test_exporter_services_show_packages(self):
        for _label, slug in SERVICE_NAV:
            with self.subTest(slug=slug):
                response = self.client.get(reverse("service_landing", kwargs={"slug": slug}))
                self.assertContains(response, 'id="packages"')
                for pkg in SERVICE_PAGES[slug]["packages"]:
                    self.assertContains(response, pkg["name"])

    def test_exhibitor_recruitment_shows_commission_terms(self):
        response = self.client.get(reverse("service_landing", kwargs={"slug": "exhibitor-recruitment-germany"}))
        self.assertContains(response, "How commission works")
        self.assertNotContains(response, 'id="packages"')

    def test_homepage_cards_link_to_description_and_packages(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        for _label, slug in SERVICE_NAV:
            url = reverse("service_landing", kwargs={"slug": slug})
            self.assertContains(response, f'href="{url}"')
            self.assertContains(response, f'href="{url}#packages"')
            self.assertContains(response, SERVICE_PAGES[slug]["card_summary"])

    def test_package_link_prefills_contact_subject(self):
        response = self.client.get(reverse("contact") + "?service=scouting&package=Partner%20shortlist")
        self.assertContains(response, "Package enquiry: Partner shortlist")

    def test_about_shows_founder(self):
        response = self.client.get(reverse("about"))
        self.assertContains(response, "Ivan Nkomati")
