"""Add the Partner Hub section (and the language cookie) to the existing privacy policy.

Only appends; never rewrites the owner's text. Runs once (marker check) and does
nothing when the privacy page does not exist.
"""
from django.db import migrations

MARKER = "TradeGate Partner Hub"

DE_COOKIE = ("Zusätzlich speichern wir die von Ihnen gewählte Sprache in einem Cookie (tg_lang, Laufzeit ein Jahr), "
             "damit die Website weiterhin in dieser Sprache angezeigt wird.")
EN_COOKIE = ("We also store the language you choose in a cookie (tg_lang, valid for one year) so the website "
             "keeps showing that language.")

DE = """10. TradeGate Partner Hub (privates Unternehmensnetzwerk)

Wenn Sie Ihr Unternehmen im TradeGate Partner Hub registrieren, verarbeiten wir die Angaben aus dem Formular: Unternehmensdaten (Name, Website, Land, Stadt, Unternehmensart und -größe, Branche, Produkte, Angebot und Suche, gewünschte Partnerarten und Regionen) sowie Daten der Kontaktperson (Name, Funktion, E-Mail-Adresse und ggf. Telefonnummer). Zusätzlich speichern wir den Zeitpunkt Ihrer Einwilligung, die genutzte Sprache sowie IP-Adresse und Browser-Informationen zur Missbrauchsprävention.

Zweck: Aufnahme in unser privates Partnernetzwerk, Prüfung Ihres Profils, Abgleich mit anderen Profilen und Anbahnung von Geschäftskontakten. Der Abgleich erfolgt teilweise automatisiert anhand von Kriterien wie Branche, Region und Partnerart. Jeden Vorschlag prüfen wir selbst; es findet keine automatisierte Entscheidung mit rechtlicher Wirkung statt.

Sichtbarkeit und Weitergabe: Profile werden nicht veröffentlicht. Den Namen Ihres Unternehmens und Ihre Kontaktdaten geben wir an einen möglichen Partner erst weiter, wenn Sie dem im Einzelfall zugestimmt haben. Befindet sich dieser Partner außerhalb der EU bzw. des EWR, besteht dort möglicherweise kein der DSGVO vergleichbares Datenschutzniveau; die Übermittlung erfolgt dann auf Grundlage Ihrer ausdrücklichen Einwilligung (Art. 49 Abs. 1 lit. a DSGVO).

Rechtsgrundlage: Art. 6 Abs. 1 lit. a DSGVO (Einwilligung) und Art. 6 Abs. 1 lit. b DSGVO (vorvertragliche Maßnahmen).

Speicherdauer: so lange Sie Teil des Netzwerks sein möchten. Profile, die 24 Monate weder aktualisiert noch bestätigt wurden, prüfen und löschen wir. Sie können Ihre Einwilligung jederzeit mit Wirkung für die Zukunft widerrufen; eine Nachricht an ivan.nkomati@tradegateconsultants.com genügt. Wir löschen Ihr Profil dann, soweit keine gesetzlichen Aufbewahrungspflichten bestehen."""

EN = """10. TradeGate Partner Hub (private company network)

If you register your company in the TradeGate Partner Hub, we process the information from the form: company data (name, website, country, city, type and size of company, sector, products, what you offer and seek, partner types and regions sought) and contact person data (name, role, email address and, if provided, phone number). We also store the time of your consent, the language used, and IP address and browser information to prevent misuse.

Purpose: admission to our private partner network, review of your profile, comparison with other profiles and initiating business contacts. The comparison is partly automated, based on criteria such as sector, region and partner type. We check every suggestion ourselves; there is no automated decision with legal effect.

Visibility and disclosure: profiles are not published. We pass your company name and contact details to a possible partner only after you have agreed in each individual case. If that partner is located outside the EU/EEA, the level of data protection there may not be comparable to the GDPR; the transfer is then based on your explicit consent (Art. 49(1)(a) GDPR).

Legal basis: Art. 6(1)(a) GDPR (consent) and Art. 6(1)(b) GDPR (pre-contractual steps).

Retention: for as long as you wish to be part of the network. We review and delete profiles that have not been updated or confirmed for 24 months. You can withdraw your consent at any time with effect for the future; a message to ivan.nkomati@tradegateconsultants.com is enough. We then delete your profile unless statutory retention obligations apply."""


def add_section(apps, schema_editor):
    LegalPage = apps.get_model("website", "LegalPage")
    page = LegalPage.objects.filter(key="datenschutz").first()
    if not page or MARKER in page.content:
        return
    text = page.content.replace("\r\n", "\n")

    de_cookie_anchor = "ggf. Sitzungscookies)."
    if de_cookie_anchor in text and DE_COOKIE not in text:
        text = text.replace(de_cookie_anchor, de_cookie_anchor + "\n" + DE_COOKIE, 1)
    en_cookie_anchor = "possibly session cookies)."
    if en_cookie_anchor in text and EN_COOKIE not in text:
        text = text.replace(en_cookie_anchor, en_cookie_anchor + "\n" + EN_COOKIE, 1)

    split = text.find("English Version")
    if split != -1:
        german, english = text[:split].rstrip(), text[split:].rstrip()
        text = german + "\n\n" + DE + "\n\n\n\n" + english + "\n\n" + EN + "\n"
    else:
        text = text.rstrip() + "\n\n" + DE + "\n\n" + EN + "\n"

    text = text.replace("Stand: 06.02.2026", "Stand: 15.11.2026")
    page.content = text
    page.save()


class Migration(migrations.Migration):
    dependencies = [("website", "0024_partner_hub")]
    operations = [migrations.RunPython(add_section, migrations.RunPython.noop)]
