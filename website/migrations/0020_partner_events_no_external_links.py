from django.db import migrations


def clear(apps, schema_editor):
    TradeFair = apps.get_model("website", "TradeFair")
    TradeFair.objects.filter(kind="represented").update(official_url="")


class Migration(migrations.Migration):
    dependencies = [("website", "0019_official_url_help")]
    operations = [migrations.RunPython(clear, migrations.RunPython.noop)]
