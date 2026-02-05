from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ("website", "0006_sitesettings_social_fields_patch"),
    ]

    operations = [
        migrations.AddField(
            model_name="sitesettings",
            name="instagram_url",
            field=models.URLField(blank=True, default=""),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="whatsapp_url",
            field=models.URLField(blank=True, default=""),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="x_url",
            field=models.URLField(blank=True, default=""),
        ),
    ]
