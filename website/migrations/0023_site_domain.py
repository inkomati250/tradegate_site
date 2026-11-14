from django.conf import settings
from django.db import migrations


def set_domain(apps, schema_editor):
    Site = apps.get_model("sites", "Site")
    site_id = getattr(settings, "SITE_ID", 1)
    site, _ = Site.objects.get_or_create(pk=site_id, defaults={"domain": "www.tradegateconsultants.com", "name": "TradeGate Consultants"})
    if site.domain in ("", "example.com"):
        site.domain = "www.tradegateconsultants.com"
        site.name = "TradeGate Consultants"
        site.save()


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0022_publish_partner_events"),
        ("sites", "0002_alter_domain_unique"),
    ]
    operations = [migrations.RunPython(set_domain, migrations.RunPython.noop)]
