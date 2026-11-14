"""Owner request 2026-11-14: show the two partner events on the live site as approved in the preview."""
from django.db import migrations

SLUGS = ["ecowas-aviana-expo-2027", "azerbaijan-mining-expo-2027"]


def publish(apps, schema_editor):
    TradeFair = apps.get_model("website", "TradeFair")
    TradeFair.objects.filter(slug__in=SLUGS, kind="represented").update(
        materials_permission=True, is_published=True, show_in_carousel=True, official_url=""
    )


class Migration(migrations.Migration):
    dependencies = [("website", "0021_tradefair_help_texts")]
    operations = [migrations.RunPython(publish, migrations.RunPython.noop)]
