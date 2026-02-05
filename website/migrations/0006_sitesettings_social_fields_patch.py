from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ("website", "0005_sitesettings_address_fields_patch"),
    ]

    operations = [
        migrations.AddField(
            model_name="sitesettings",
            name="facebook_url",
            field=models.URLField(blank=True, default=""),
        ),
    ]
