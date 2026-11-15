"""The first hours of statistics (15 Nov 2026) were counted on the server and included automated
scanners posing as browsers. Counting now happens only when a real browser reports the view,
so start the statistics fresh."""
from django.db import migrations


def reset(apps, schema_editor):
    apps.get_model("website", "PageVisit").objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [("website", "0028_privacy_visitor_stats")]
    operations = [migrations.RunPython(reset, migrations.RunPython.noop)]
