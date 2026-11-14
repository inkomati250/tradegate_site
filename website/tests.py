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


class FounderAndContactTests(TestCase):
    def test_about_shows_photo_partners_and_linkedin(self):
        response = self.client.get(reverse("about"))
        self.assertContains(response, "/static/website/img/ivan-nkomati.webp")
        self.assertNotContains(response, "<img src=\"/static/website/img/ivan-nkomati.webp")
        self.assertContains(response, "you keep one contact throughout")
        self.assertContains(response, "linkedin.com/in/ivan-nkomati-313637228")

    def test_contact_form_keeps_optional_fields_folded(self):
        response = self.client.get(reverse("contact"))
        self.assertContains(response, "Add more details")
        self.assertContains(response, 'name="phone"')


class BrandingTests(TestCase):
    def test_header_uses_logo_and_favicon(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, "tradegate-logo-light.webp")
        self.assertContains(response, "favicon-32.png")


class TradeFairCalendarTests(TestCase):
    """Uses the seeded fairs from migration 0013."""

    def test_calendar_lists_german_fairs_and_hides_unpublished_partner_events(self):
        response = self.client.get(reverse("trade_fairs"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Fruit Logistica")
        self.assertContains(response, "AGRITECHNICA")
        self.assertNotContains(response, "Azerbaijan Mining Expo")
        self.assertContains(response, "not affiliated")

    def test_published_partner_event_appears_with_badge(self):
        from .models import TradeFair
        TradeFair.objects.filter(slug="ecowas-aviana-expo-2027").update(is_published=True)
        response = self.client.get(reverse("trade_fairs"))
        self.assertContains(response, "ECOWAS Aviana")
        self.assertContains(response, "Partner event")

    def test_unpublished_detail_is_404(self):
        response = self.client.get(reverse("trade_fair_detail", kwargs={"slug": "azerbaijan-mining-expo-2027"}))
        self.assertEqual(response.status_code, 404)

    def test_detail_page_has_cta_disclaimer_schema_and_official_link(self):
        response = self.client.get(reverse("trade_fair_detail", kwargs={"slug": "anuga-cologne-2027"}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "fair=anuga-cologne-2027")
        self.assertContains(response, '"@type": "Event"')
        self.assertContains(response, 'rel="noopener nofollow"')
        self.assertContains(response, "not affiliated")

    def test_ics_download(self):
        response = self.client.get(reverse("trade_fair_ics", kwargs={"slug": "itb-berlin-2027"}))
        self.assertEqual(response["Content-Type"], "text/calendar; charset=utf-8")
        body = response.content.decode()
        self.assertIn("DTSTART;VALUE=DATE:20270316", body)
        self.assertIn("DTEND;VALUE=DATE:20270319", body)

    def test_homepage_carousel_and_nav(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, "fair-track")
        self.assertContains(response, reverse("trade_fair_detail", kwargs={"slug": "bau-munich-2027"}))
        self.assertContains(response, "Trade fair calendar")

    def test_contact_prefill_from_fair(self):
        response = self.client.get(reverse("contact") + "?service=trade_fair&fair=prowein-duesseldorf-2027")
        self.assertContains(response, "Representation at ProWein")

    def test_about_uses_we_voice_and_invites_partners(self):
        response = self.client.get(reverse("about"))
        self.assertContains(response, "Partner with us")
        self.assertNotContains(response, "contact: me")


class AdminAndContentTests(TestCase):
    def setUp(self):
        from django.contrib.auth import get_user_model
        self.admin_user = get_user_model().objects.create_superuser("boss", "boss@example.com", "pass12345!")

    def test_admin_dashboard_is_branded_and_grouped(self):
        self.client.force_login(self.admin_user)
        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "tradegate-admin.css")
        self.assertContains(response, "New enquiries")
        self.assertContains(response, "Partner events waiting")
        for section in ["Enquiries", "Trade fairs", "Services and prices", "Team and company"]:
            self.assertContains(response, section)

    def test_admin_login_page_is_branded(self):
        response = self.client.get(reverse("admin:login"))
        self.assertContains(response, "tradegate-logo-light.webp")

    def test_admin_changelists_load(self):
        self.client.force_login(self.admin_user)
        for name in ["tradefair", "servicepackage", "teamprofile", "inquiry"]:
            response = self.client.get(reverse(f"admin:website_{name}_changelist"))
            self.assertEqual(response.status_code, 200, name)

    def test_partner_event_cannot_be_published_without_permission(self):
        from django.core.exceptions import ValidationError
        from .models import TradeFair
        fair = TradeFair.objects.get(slug="azerbaijan-mining-expo-2027")
        fair.is_published = True
        with self.assertRaises(ValidationError):
            fair.full_clean()
        fair.materials_permission = True
        fair.full_clean()

    def test_package_prices_come_from_admin(self):
        from .models import ServicePackage
        ServicePackage.objects.filter(name="Partner shortlist").update(price="€450")
        response = self.client.get(reverse("service_landing", kwargs={"slug": "find-business-partners-germany"}))
        self.assertContains(response, "€450")
        self.assertNotContains(response, ">€490<")

    def test_team_profile_from_admin(self):
        from .models import TeamProfile
        TeamProfile.objects.update(role="Managing Director")
        response = self.client.get(reverse("about"))
        self.assertContains(response, "Managing Director")

    def test_homepage_separates_partner_events_from_german_calendar(self):
        from .models import TradeFair
        TradeFair.objects.filter(slug="ecowas-aviana-expo-2027").update(is_published=True, materials_permission=True)
        response = self.client.get(reverse("home"))
        html = response.content.decode()
        self.assertIn("Our partner trade fairs", html)
        self.assertIn("Going to a trade fair in Germany?", html)
        partner_section = html.split('id="partner-events"')[1].split('id="opportunities"')[0]
        self.assertIn("ECOWAS Aviana", partner_section)
        calendar_section = html.split('id="opportunities"')[1].split("</section>")[0]
        self.assertNotIn("ECOWAS Aviana", calendar_section)


class ComprehensiveCalendarTests(TestCase):
    def test_calendar_lists_many_german_fairs_including_tbc(self):
        response = self.client.get(reverse("trade_fairs"))
        for name in ["BAU", "Heimtextil", "transport logistic", "automatica", "IAA MOBILITY", "productronica", "MEDICA"]:
            self.assertContains(response, name)
        self.assertContains(response, "Dates to be announced")

    def test_organiser_page_is_non_exclusive_and_international(self):
        response = self.client.get(reverse("service_landing", kwargs={"slug": "exhibitor-recruitment-germany"}))
        self.assertContains(response, "Germany, the EU and Beyond")
        self.assertContains(response, "Non-exclusive")


class PartnerEventBannerTests(TestCase):
    def _publish(self, slug):
        from .models import TradeFair
        TradeFair.objects.filter(slug=slug).update(is_published=True, materials_permission=True)
        return TradeFair.objects.get(slug=slug)

    def test_only_two_pending_partner_events_remain(self):
        from .models import TradeFair
        slugs = set(TradeFair.objects.filter(kind="represented").values_list("slug", flat=True))
        self.assertEqual(slugs, {"ecowas-aviana-expo-2027", "azerbaijan-mining-expo-2027"})
        self.assertFalse(TradeFair.objects.filter(kind="represented", is_published=True).exists())

    def test_placeholder_banner_until_official_banner_uploaded(self):
        fair = self._publish("azerbaijan-mining-expo-2027")
        self.assertTrue(fair.logo)
        r = self.client.get(reverse("trade_fair_detail", kwargs={"slug": fair.slug}))
        self.assertContains(r, "Official event banner")
        self.assertContains(r, fair.logo.url)
        self.assertContains(r, "€480 per m²")
        self.assertContains(r, "does not add to your price")
        fair.cover_image = "trade-fairs/covers/official.jpg"
        fair.save()
        r = self.client.get(reverse("trade_fair_detail", kwargs={"slug": fair.slug}))
        self.assertNotContains(r, "Official event banner")
        self.assertContains(r, "trade-fairs/covers/official.jpg")

    def test_price_list_image_is_shown(self):
        fair = self._publish("ecowas-aviana-expo-2027")
        fair.packages_image = "trade-fairs/packages/aviana-prices.jpg"
        fair.save()
        r = self.client.get(reverse("trade_fair_detail", kwargs={"slug": fair.slug}))
        self.assertContains(r, "trade-fairs/packages/aviana-prices.jpg")
        self.assertContains(r, "US$ 2,650")

    def test_banner_placeholder_on_listing_and_home(self):
        self._publish("ecowas-aviana-expo-2027")
        for url in (reverse("trade_fairs"), reverse("home")):
            r = self.client.get(url)
            self.assertContains(r, "Official banner coming soon")


class OfficialLinkTests(TestCase):
    def test_partner_event_never_links_to_organiser_site(self):
        from .models import TradeFair
        TradeFair.objects.filter(kind="represented").update(is_published=True, materials_permission=True)
        fair = TradeFair.objects.get(slug="azerbaijan-mining-expo-2027")
        self.assertEqual(fair.official_url, "")
        fair.official_url = "https://www.azerbaijanminingexpo.com/"
        fair.save()
        fair.refresh_from_db()
        self.assertEqual(fair.official_url, "")
        for slug, banned in [("azerbaijan-mining-expo-2027", ["azerbaijanminingexpo", "introfair", "thetrueexpo", "Intro Exhibition", "True Expo"]),
                             ("ecowas-aviana-expo-2027", ["ecowasavianavivexpo", "afpinfo", "aviananigeria"])]:
            for url in (reverse("trade_fair_detail", kwargs={"slug": slug}), reverse("trade_fairs"), reverse("home")):
                body = self.client.get(url).content.decode()
                for word in banned:
                    self.assertNotIn(word, body, f"{word} leaked on {url}")
        r = self.client.get(reverse("trade_fair_detail", kwargs={"slug": fair.slug}))
        self.assertNotContains(r, "Official event website")
        self.assertContains(r, "contact us")

    def test_german_fair_link_or_not_available(self):
        from .models import TradeFair
        fair = TradeFair.objects.filter(kind="germany", is_published=True).exclude(official_url="").first()
        r = self.client.get(reverse("trade_fair_detail", kwargs={"slug": fair.slug}))
        self.assertContains(r, fair.official_url)
        fair.official_url = ""
        fair.save()
        r = self.client.get(reverse("trade_fair_detail", kwargs={"slug": fair.slug}))
        self.assertContains(r, "Official link not available")
        self.assertNotContains(r, "Official event website")


class ContactDeliveryTests(TestCase):
    def _post(self, **extra):
        import time
        data = {
            "full_name": "Anna Example", "email": "anna@example.de", "company_name": "Example GmbH",
            "country": "Germany", "service_interest": "trade_fair", "contact_method": "email",
            "subject": "Stand at a trade fair", "message": "We would like help with a stand at a fair next year.",
            "consent": "on", "website_url": "", "form_started_at": str(int(time.time()) - 120),
        }
        data.update(extra)
        return self.client.post(reverse("contact"), data, follow=True)

    def test_valid_enquiry_is_saved_and_emailed(self):
        from django.core import mail
        from .models import Inquiry
        r = self._post()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(Inquiry.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Anna Example", mail.outbox[0].body)
        self.assertEqual(mail.outbox[0].reply_to, ["anna@example.de"])

    def test_new_service_choices_still_send(self):
        from django.core import mail
        for choice in ("exhibitor_recruitment", "exhibit_abroad", "partnership"):
            self._post(service_interest=choice, email=f"{choice}@example.de")
        self.assertEqual(len(mail.outbox), 3)


class SeoTests(TestCase):
    def test_every_page_has_title_description_canonical_and_org_schema(self):
        from .models import TradeFair
        fair = TradeFair.objects.filter(kind="germany", is_published=True).first()
        urls = [reverse("home"), reverse("about"), reverse("faq"), reverse("contact"), reverse("trade_fairs"),
                reverse("trade_fair_detail", kwargs={"slug": fair.slug})]
        urls += [reverse("service_landing", kwargs={"slug": s}) for s in SERVICE_PAGES]
        for url in urls:
            body = self.client.get(url).content.decode()
            self.assertIn("<title>", body, url)
            self.assertIn('name="description"', body, url)
            self.assertIn('rel="canonical"', body, url)
            self.assertIn('property="og:url"', body, url)
            self.assertIn('"ProfessionalService"', body, url)
            self.assertIn("/static/website/css/site.css", body, url)
            self.assertNotIn("cdn.tailwindcss.com", body, url)

    def test_breadcrumbs_and_faq_schema(self):
        body = self.client.get(reverse("faq")).content.decode()
        self.assertIn('"FAQPage"', body)
        self.assertIn('"BreadcrumbList"', body)
        slug = next(iter(SERVICE_PAGES))
        body = self.client.get(reverse("service_landing", kwargs={"slug": slug})).content.decode()
        self.assertIn('"FAQPage"', body)
        self.assertIn('"Service"', body)

    def test_sitemap_lists_fairs_and_calendar_but_not_hidden_partner_events(self):
        body = self.client.get("/sitemap.xml").content.decode()
        self.assertIn("/trade-fairs/", body)
        self.assertIn("/trade-fairs/hannover-messe-2027/", body)
        self.assertNotIn("azerbaijan-mining-expo", body)
        self.assertIn("/services/exhibitor-recruitment-germany/", body)

    def test_fair_title_has_year_once(self):
        from .models import TradeFair
        TradeFair.objects.filter(kind="represented").update(is_published=True, materials_permission=True)
        body = self.client.get(reverse("trade_fair_detail", kwargs={"slug": "azerbaijan-mining-expo-2027"})).content.decode()
        self.assertNotIn("2027 2027", body)

    def test_cdn_fallback_switch(self):
        from django.test import override_settings
        with override_settings(USE_TAILWIND_CDN=True):
            body = self.client.get(reverse("home")).content.decode()
        self.assertIn("cdn.tailwindcss.com", body)
