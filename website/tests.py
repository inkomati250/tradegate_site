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
        self.assertContains(response, "/favicon.ico")
        self.assertNotContains(response, "<link rel=\"icon\" type=\"image/svg+xml\"")


class TradeFairCalendarTests(TestCase):
    """Uses the seeded fairs from migration 0013."""

    def test_calendar_lists_german_fairs_and_hides_unpublished_partner_events(self):
        from .models import TradeFair as _TF
        _TF.objects.filter(kind="represented").update(is_published=False, materials_permission=False)
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
        from .models import TradeFair as _TF
        _TF.objects.filter(kind="represented").update(is_published=False, materials_permission=False)
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
        self.assertContains(response, "Open enquiries")
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
        from .models import TradeFair as _TF
        _TF.objects.filter(kind="represented").update(is_published=False, materials_permission=False)
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
        from .models import TradeFair as _TF
        _TF.objects.filter(kind="represented").update(is_published=False, materials_permission=False)
        from .models import TradeFair
        slugs = set(TradeFair.objects.filter(kind="represented").values_list("slug", flat=True))
        self.assertEqual(slugs, {"ecowas-aviana-expo-2027", "azerbaijan-mining-expo-2027"})
        self.assertFalse(TradeFair.objects.filter(kind="represented", is_published=True).exists())

    def test_partner_events_published_on_live_as_in_preview(self):
        from .models import TradeFair
        for slug in ("ecowas-aviana-expo-2027", "azerbaijan-mining-expo-2027"):
            f = TradeFair.objects.get(slug=slug)
            self.assertTrue(f.is_published and f.materials_permission)
        body = self.client.get(reverse("home")).content.decode()
        self.assertIn("Our partner trade fairs", body)
        self.assertIn("Azerbaijan Mining Expo 2027", body)

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


class SitemapDomainTests(TestCase):
    def test_sitemap_uses_public_domain_not_example_com(self):
        r = self.client.get("/sitemap.xml")
        self.assertEqual(r.status_code, 200)
        body = r.content.decode()
        self.assertNotIn("example.com", body)
        self.assertIn("<loc>http://www.tradegateconsultants.com/</loc>", body.replace("https://", "http://"))


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
        from .models import TradeFair as _TF
        _TF.objects.filter(kind="represented").update(is_published=False, materials_permission=False)
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


class LanguageTests(TestCase):
    def test_german_page_is_translated_with_seo_tags(self):
        r = self.client.get(reverse("home") + "?lang=de")
        body = r.content.decode()
        self.assertIn('<html lang="de"', body)
        self.assertIn("Ihr Markteintrittsteam", body)
        self.assertIn('?lang=de"', body)  # canonical / og:url
        for code in ("en", "de", "fr", "pt", "es", "x-default"):
            self.assertIn(f'hreflang="{code}"', body)
        self.assertEqual(r["Content-Language"], "de")
        self.assertEqual(r.cookies["tg_lang"].value, "de")

    def test_language_is_remembered_and_english_default(self):
        self.client.get(reverse("home") + "?lang=fr")
        body = self.client.get(reverse("about")).content.decode()
        self.assertIn('<html lang="fr"', body)
        fresh = self.client_class()
        self.assertIn('<html lang="en"', fresh.get(reverse("about")).content.decode())

    def test_browser_language_used_when_no_choice(self):
        body = self.client.get(reverse("faq"), HTTP_ACCEPT_LANGUAGE="es-ES,es;q=0.9").content.decode()
        self.assertIn('<html lang="es"', body)

    def test_all_languages_render_every_main_page(self):
        for code in ("de", "fr", "pt", "es"):
            for name in ("home", "about", "faq", "contact", "trade_fairs"):
                r = self.client.get(reverse(name) + f"?lang={code}")
                self.assertEqual(r.status_code, 200, (code, name))
            for slug in SERVICE_PAGES:
                self.assertEqual(self.client.get(reverse("service_landing", kwargs={"slug": slug}) + f"?lang={code}").status_code, 200)

    def test_picker_in_nav_and_structured_data_untouched(self):
        body = self.client.get(reverse("home") + "?lang=pt").content.decode()
        self.assertIn('class="lang-picker', body)
        for name in ("English", "Deutsch", "Français", "Português", "Español"):
            self.assertIn(name, body)
        self.assertIn('"ProfessionalService"', body)
        self.assertIn("csrfmiddlewaretoken", self.client.get(reverse("contact") + "?lang=de").content.decode())

    def test_contact_form_in_german_still_emails(self):
        import time
        from django.core import mail
        self.client.get(reverse("contact") + "?lang=de")
        r = self.client.post(reverse("contact"), {
            "full_name": "Max Muster", "email": "max@example.de", "company_name": "Muster GmbH",
            "service_interest": "trade_fair", "contact_method": "email", "subject": "Messe",
            "message": "Wir brauchen Unterstützung auf einer Messe im nächsten Jahr.", "consent": "on",
            "website_url": "", "form_started_at": str(int(time.time()) - 120),
        }, follow=True)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Danke", r.content.decode())

    def test_admin_and_sitemap_not_translated(self):
        self.assertNotIn("Content-Language", self.client.get("/sitemap.xml?lang=de").headers)
        body = self.client.get("/sitemap.xml").content.decode()
        self.assertIn("?lang=de", body)
        self.assertIn("?lang=es", body)

    def test_favicon_served_at_root(self):
        r = self.client.get("/favicon.ico")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r["Content-Type"], "image/x-icon")


class PartnerHubTests(TestCase):
    def setUp(self):
        from django.core.cache import cache
        cache.clear()

    def _data(self, **over):
        import time
        data = {
            "form_started_at": str(int(time.time()) - 60),
            "company_name": "Nairobi Coffee Exporters", "website": "https://ncx.example.com", "country": "Kenya",
            "company_type": "exporter", "company_size": "10_49", "sector": "agrifood", "products": "specialty coffee beans",
            "offering": "We export washed Arabica coffee beans in container loads with organic certification.",
            "seeking": "A German importer or distributor for specialty coffee beans and roasters.",
            "partner_types": ["distributor"], "target_regions": ["germany", "eu"],
            "contact_name": "Amina Otieno", "contact_role": "Export Manager", "email": "amina@ncx.example.com", "consent": "on",
        }
        data.update(over)
        return data

    def _profile(self, **kw):
        from .models import PartnerProfile
        base = dict(company_name="Hamburg Kaffee Import", country="Germany", company_type="distributor", sector="agrifood",
                    products="green coffee import", offering="We import and distribute specialty coffee beans to roasters in Germany.",
                    seeking="Exporters of specialty coffee beans from East Africa.", partner_types="supplier",
                    target_regions="africa", contact_name="Jan", email="jan@hki.example.de", status="approved")
        base.update(kw)
        return PartnerProfile.objects.create(**base)

    def test_page_renders_and_is_linked_in_menu_and_sitemap(self):
        r = self.client.get(reverse("partner_pool"))
        self.assertContains(r, "Find business partners in Germany or abroad.")
        self.assertContains(r, 'id="pool-form"')
        self.assertContains(r, '"FAQPage"')
        home = self.client.get(reverse("home"))
        self.assertContains(home, 'href="/partner-hub/"')
        self.assertContains(self.client.get("/sitemap.xml"), "/partner-hub/")
        svc = self.client.get(reverse("service_landing", kwargs={"slug": "find-business-partners-germany"}))
        self.assertContains(svc, 'href="/partner-hub/"')

    def test_registration_is_saved_pending_and_emailed_with_matches(self):
        from django.core import mail
        from .models import PartnerProfile
        self._profile()
        r = self.client.post(reverse("partner_pool"), self._data(), follow=True)
        self.assertContains(r, "Your company is registered")
        p = PartnerProfile.objects.get(email="amina@ncx.example.com")
        self.assertEqual(p.status, "pending")
        self.assertEqual(p.partner_types, "distributor")
        self.assertEqual(p.target_regions, "germany,eu")
        self.assertTrue(p.consent and p.consent_at)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("1 possible match", mail.outbox[0].subject)
        self.assertIn("Hamburg Kaffee Import", mail.outbox[0].body)
        self.assertEqual(mail.outbox[0].reply_to, ["amina@ncx.example.com"])

    def test_consent_and_details_required(self):
        from .models import PartnerProfile
        r = self.client.post(reverse("partner_pool"), self._data(consent="", offering="short", partner_types=[]))
        self.assertContains(r, "Your consent is needed")
        self.assertContains(r, "at least 30 characters")
        self.assertContains(r, "Please choose at least one partner type.")
        self.assertFalse(PartnerProfile.objects.exists())

    def test_honeypot_and_spam_are_not_saved(self):
        from django.core import mail
        from .models import PartnerProfile
        self.client.post(reverse("partner_pool"), self._data(website_url="http://spam.example"))
        self.client.post(reverse("partner_pool"), self._data(offering="We sell backlinks and guest post packages for your rank on google."))
        self.assertFalse(PartnerProfile.objects.exists())
        self.assertEqual(len(mail.outbox), 0)

    def test_matching_needs_regions_both_ways_and_substance(self):
        from .models import PartnerProfile
        from .partner_pool import suggestions_for
        importer = self._profile()
        exporter = self._profile(company_name="Kenya Beans", country="Kenya", company_type="exporter",
                                 offering="We export specialty coffee beans.", seeking="German importer distributor for coffee beans.",
                                 partner_types="distributor", target_regions="germany", email="x@kb.example")
        self.assertEqual([o for _, o, _ in suggestions_for(exporter, [importer])], [importer])
        asia_only = self._profile(company_name="Asia only", target_regions="asia", email="y@ao.example")
        self.assertEqual(suggestions_for(exporter, [asia_only]), [])
        other_sector = self._profile(company_name="Machines GmbH", sector="machinery", products="CNC machines",
                                     offering="CNC lathes", seeking="Metal workshops", email="z@m.example")
        self.assertEqual(suggestions_for(exporter, [other_sector]), [])
        self.assertEqual(suggestions_for(exporter, [exporter]), [])
        self.assertTrue(PartnerProfile.objects.count() >= 3)

    def test_admin_shows_suggested_matches(self):
        from django.contrib.auth.models import User
        importer = self._profile()
        exporter = self._profile(company_name="Kenya Beans", country="Kenya", company_type="exporter", status="pending",
                                 offering="We export specialty coffee beans.", seeking="German importer for coffee beans.",
                                 partner_types="distributor", target_regions="germany", email="x@kb.example")
        User.objects.create_superuser("boss", "boss@example.com", "pw-123456")
        self.client.login(username="boss", password="pw-123456")
        r = self.client.get(reverse("admin:website_partnerprofile_change", args=[exporter.pk]))
        self.assertContains(r, importer.company_name)
        self.assertContains(r, "same sector")
        self.assertContains(self.client.get(reverse("admin:index")), "Partner Hub: to review")

    def test_german_version(self):
        r = self.client.get(reverse("partner_pool") + "?lang=de")
        html = r.content.decode()
        self.assertIn("Geschäftspartner in Deutschland oder im Ausland finden.", html)
        self.assertIn(">Kenia<", html)
        self.assertIn('value="Kenya"', html)


class PrivacyPartnerHubMigrationTests(TestCase):
    def test_section_added_once_in_both_languages(self):
        import importlib
        from django.apps import apps
        from .models import LegalPage
        mig = importlib.import_module("website.migrations.0025_privacy_partner_hub")
        LegalPage.objects.update_or_create(key="datenschutz", defaults={"title": "Datenschutz", "content":
            "Stand: 06.02.2026\n6. Cookies\n(z. B. für Sicherheitsfunktionen wie CSRF-Schutz und ggf. Sitzungscookies).\n9. Datensicherheit\nText.\n\n\nEnglish Version\n"
            "6. Cookies\n(e.g., security-related cookies such as CSRF protection and possibly session cookies).\n9. Data security\nText."})
        mig.add_section(apps, None)
        mig.add_section(apps, None)
        c = LegalPage.objects.get(key="datenschutz").content
        self.assertEqual(c.count("10. TradeGate Partner Hub"), 2)
        self.assertLess(c.index("privates Unternehmensnetzwerk"), c.index("English Version"))
        self.assertGreater(c.index("private company network"), c.index("English Version"))
        self.assertIn("Stand: 15.11.2026", c)
        self.assertIn("tg_lang", c)


class PartnerHubConfirmationAndAdminTests(TestCase):
    def setUp(self):
        from django.core.cache import cache
        cache.clear()

    def _post(self, lang=""):
        import time
        data = {"form_started_at": str(int(time.time()) - 60), "company_name": "Lagos Agro Ltd", "country": "Nigeria",
                "company_type": "exporter", "sector": "agrifood", "products": "cashew nuts",
                "offering": "We process and export cashew nuts in bulk with full traceability.",
                "seeking": "German importers and wholesalers of nuts and dried fruit.", "partner_types": ["distributor"],
                "target_regions": ["germany"], "contact_name": "Ada Obi", "email": "ada@lagosagro.example", "consent": "on"}
        return self.client.post(reverse("partner_pool") + lang, data, follow=True)

    def test_no_confirmation_email_unless_switched_on(self):
        from django.core import mail
        self._post()
        self.assertEqual(len(mail.outbox), 1)  # only our own notification

    def test_confirmation_email_in_registration_language(self):
        from django.core import mail
        from .models import SiteSettings
        SiteSettings.objects.create(hub_confirmation_email=True)
        self.client.get(reverse("partner_pool") + "?lang=de")
        self._post()
        self.assertEqual(len(mail.outbox), 2)
        confirmation = mail.outbox[1]
        self.assertEqual(confirmation.to, ["ada@lagosagro.example"])
        self.assertIn("TradeGate Partner Hub registriert", confirmation.subject)
        self.assertIn("Lagos Agro Ltd", confirmation.body)

    def test_dashboard_and_top_menu(self):
        from django.contrib.auth.models import User
        User.objects.create_superuser("boss", "boss@example.com", "pw-123456")
        self.client.login(username="boss", password="pw-123456")
        r = self.client.get(reverse("admin:index"))
        self.assertContains(r, "Partner Hub: to review")
        self.assertContains(r, 'class="tg-topnav"')
        self.assertNotContains(r, 'id="nav-sidebar"')
        r = self.client.get(reverse("admin:website_partnerprofile_changelist"))
        self.assertContains(r, 'class="tg-topnav"')


class VisitorStatsTests(TestCase):
    UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/130.0 Safari/537.36"

    def _beacon(self, path="/partner-hub/", ref="", lang="en", **headers):
        import json
        h = {"HTTP_USER_AGENT": self.UA, "HTTP_X_REAL_IP": "203.0.113.7"}
        h.update(headers)
        return self.client.post("/v/", data=json.dumps({"p": path, "r": ref, "l": lang}), content_type="application/json", **h)

    def test_only_browser_beacons_count_and_no_ip_stored(self):
        from .models import PageVisit
        self.client.get("/", HTTP_USER_AGENT=self.UA)  # plain page load (e.g. a scanner): not counted
        self.assertEqual(PageVisit.objects.count(), 0)
        self.assertEqual(self._beacon(ref="https://www.google.com/", lang="de").status_code, 204)
        self._beacon(HTTP_USER_AGENT="Googlebot/2.1 (+http://www.google.com/bot.html)")
        self._beacon(HTTP_USER_AGENT="python-requests/2.31")
        self._beacon(HTTP_DNT="1")
        self._beacon(path="/admin/")
        self._beacon(path="https://evil.example/")
        self.assertEqual(PageVisit.objects.count(), 1)
        v = PageVisit.objects.get()
        self.assertEqual((v.path, v.source, v.language, v.device), ("/partner-hub/", "Google", "de", "Desktop"))
        self.assertNotIn("203.0.113.7", str(v.__dict__))

    def test_same_person_counts_once_per_day(self):
        from .analytics import summary
        for p in ("/", "/about/", "/partner-hub/"):
            self._beacon(path=p)
        self._beacon(path="/", HTTP_X_REAL_IP="198.51.100.9")
        s = summary(7)
        self.assertEqual((s["visitors"], s["views"]), (2, 4))

    def test_public_pages_carry_the_beacon_script(self):
        self.assertContains(self.client.get("/"), 'sendBeacon("/v/"')

    def test_staff_visits_not_counted_and_stats_page_renders(self):
        from django.contrib.auth.models import User
        from .models import PageVisit
        User.objects.create_superuser("boss", "boss@example.com", "pw-123456")
        self.client.login(username="boss", password="pw-123456")
        self._beacon()
        self.assertEqual(PageVisit.objects.count(), 0)
        self.assertNotContains(self.client.get("/"), 'sendBeacon("/v/"')
        r = self.client.get(reverse("admin:website_pagevisit_changelist") + "?days=7")
        self.assertContains(r, "Visitor statistics")
        self.assertContains(r, "DB-IP")
        self.assertContains(self.client.get(reverse("admin:index")), "Website visitors")

    def test_css_links_are_versioned(self):
        r = self.client.get("/")
        self.assertRegex(r.content.decode(), r"site\.css\?v=[0-9a-f]{10}")

    def test_source_detection(self):
        from .analytics import source_of
        self.assertEqual(source_of("", "x")[0], "Direct / unknown")
        self.assertEqual(source_of("https://www.linkedin.com/feed/", "x")[0], "LinkedIn")
        self.assertEqual(source_of("https://www.tradegateconsultants.com/about/", "www.tradegateconsultants.com")[0], "")
        self.assertEqual(source_of("https://chatgpt.com/", "x")[0], "AI assistants")

    def test_privacy_section_11_added_once(self):
        import importlib
        from django.apps import apps
        from .models import LegalPage
        mig = importlib.import_module("website.migrations.0028_privacy_visitor_stats")
        LegalPage.objects.update_or_create(key="datenschutz", defaults={"title": "D", "content": "Deutsch text here.\n\nEnglish Version\nEnglish text here."})
        mig.add_section(apps, None)
        mig.add_section(apps, None)
        c = LegalPage.objects.get(key="datenschutz").content
        self.assertEqual(c.count("11. Besucherstatistik"), 1)
        self.assertGreater(c.index("11. Visitor statistics"), c.index("English Version"))
