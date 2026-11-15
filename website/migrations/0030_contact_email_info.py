"""Owner request (15 Nov 2026): use info@tradegateconsultants.com instead of the personal
address ivan.nkomati@tradegateconsultants.com everywhere on the website (privacy policy,
Impressum and any other stored text). Replaces the address in every text field of the
website's own tables; prints what changed in the deploy log."""
from django.db import migrations, models

OLD = "ivan.nkomati@tradegateconsultants.com"
NEW = "info@tradegateconsultants.com"


def replace(apps, schema_editor):
    for model in apps.get_app_config("website").get_models():
        fields = [f.name for f in model._meta.get_fields()
                  if isinstance(f, (models.CharField, models.TextField, models.EmailField)) and not f.choices]
        if not fields:
            continue
        changed = 0
        for obj in model.objects.all():
            dirty = []
            for name in fields:
                value = getattr(obj, name, None)
                if isinstance(value, str) and OLD in value.lower():
                    import re
                    setattr(obj, name, re.sub(re.escape(OLD), NEW, value, flags=re.I))
                    dirty.append(name)
            if dirty:
                obj.save(update_fields=dirty)
                changed += 1
        if changed:
            print(f"\n  {model.__name__}: replaced the email address in {changed} record(s)")


class Migration(migrations.Migration):
    dependencies = [("website", "0029_reset_bot_visits")]
    operations = [migrations.RunPython(replace, migrations.RunPython.noop)]
