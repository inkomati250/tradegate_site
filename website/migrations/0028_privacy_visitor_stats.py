"""Append section 11 (cookieless visitor statistics) to the privacy policy, in German and English.

Append-only; runs once (marker check); does nothing if the privacy page does not exist.
"""
from django.db import migrations

MARKER = "11. Besucherstatistik"

DE = """11. Besucherstatistik (ohne Cookies)

Um zu verstehen, wie unsere Website genutzt wird und aus welchen Ländern unsere Besucher kommen, erstellen wir eine eigene, einfache Statistik. Dafür setzen wir keine Cookies und keine Dienste Dritter ein. Pro Seitenaufruf speichern wir: Datum, aufgerufene Seite, Land (aus der IP-Adresse über eine lokal auf unserem Server gespeicherte Länderdatenbank von DB-IP ermittelt), Herkunft (z. B. Suchmaschine oder direkter Aufruf), Gerätetyp und Sprache der Website sowie einen anonymen Besuchercode. Dieser Code wird aus IP-Adresse und Browserkennung mit einem täglich wechselnden Schlüssel berechnet; die IP-Adresse selbst wird nicht gespeichert, und Besuche an verschiedenen Tagen lassen sich nicht miteinander verknüpfen. Wenn Ihr Browser "Do Not Track" oder "Global Privacy Control" sendet, zählen wir Ihren Besuch nicht.

Zweck: Verbesserung unseres Angebots und Verständnis der Nachfrage aus verschiedenen Märkten.
Rechtsgrundlage: Art. 6 Abs. 1 lit. f DSGVO (berechtigtes Interesse an einer bedarfsgerechten Gestaltung unserer Website).
Speicherdauer: höchstens 13 Monate; danach werden die Einträge automatisch gelöscht."""

EN = """11. Visitor statistics (without cookies)

To understand how our website is used and which countries our visitors come from, we keep our own simple statistics. We use no cookies and no third-party services for this. For each page view we store: date, page visited, country (derived from the IP address using a DB-IP country database kept on our own server), source (e.g. search engine or direct visit), device type and website language, plus an anonymous visitor code. This code is calculated from the IP address and browser identifier with a key that changes every day; the IP address itself is not stored, and visits on different days cannot be linked. If your browser sends "Do Not Track" or "Global Privacy Control", we do not count your visit.

Purpose: improving our services and understanding demand from different markets.
Legal basis: Art. 6(1)(f) GDPR (legitimate interest in designing our website according to demand).
Retention: at most 13 months; entries are then deleted automatically."""


def add_section(apps, schema_editor):
    LegalPage = apps.get_model("website", "LegalPage")
    page = LegalPage.objects.filter(key="datenschutz").first()
    if not page or MARKER in page.content:
        return
    text = page.content.replace("\r\n", "\n")
    split = text.find("English Version")
    if split != -1:
        german, english = text[:split].rstrip(), text[split:].rstrip()
        text = german + "\n\n" + DE + "\n\n\n\n" + english + "\n\n" + EN + "\n"
    else:
        text = text.rstrip() + "\n\n" + DE + "\n\n" + EN + "\n"
    page.content = text
    page.save()


class Migration(migrations.Migration):
    dependencies = [("website", "0027_page_visits")]
    operations = [migrations.RunPython(add_section, migrations.RunPython.noop)]
