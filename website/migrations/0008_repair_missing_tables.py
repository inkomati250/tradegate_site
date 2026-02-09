from django.db import migrations


def repair_missing_tables(apps, schema_editor):
    # List missing tables that must exist for the app to work.
    # We'll create them if absent, without touching existing ones.
    models_to_ensure = [
        ("website", "NavigationItem"),
    ]

    existing = set(schema_editor.connection.introspection.table_names())

    for app_label, model_name in models_to_ensure:
        Model = apps.get_model(app_label, model_name)
        table = Model._meta.db_table

        if table not in existing:
            schema_editor.create_model(Model)
            existing.add(table)


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0007_sitesettings_social_links_patch"),
    ]

    operations = [
        migrations.RunPython(repair_missing_tables, migrations.RunPython.noop),
    ]
