# Generated manually to avoid touching deployment/settings files.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0009_alter_sitesettings_country_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="TradeFairOpportunity",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("title", models.CharField(max_length=140)),
                ("slug", models.SlugField(max_length=160, unique=True)),
                ("city_country", models.CharField(blank=True, default="", max_length=120)),
                ("date_label", models.CharField(blank=True, default="", max_length=120)),
                ("industry", models.CharField(blank=True, default="", max_length=140)),
                ("summary", models.CharField(max_length=260)),
                ("image", models.FileField(blank=True, default="", upload_to="event-opportunities/")),
                ("image_url", models.URLField(blank=True, default="")),
                ("visual_label", models.CharField(blank=True, default="", max_length=20)),
                ("cta_label", models.CharField(default="Request representation", max_length=60)),
                ("cta_url", models.CharField(default="/contact/?service=trade_fair#contact-form", max_length=220)),
                ("is_active", models.BooleanField(default=True)),
                ("order", models.PositiveIntegerField(default=0)),
            ],
            options={
                "verbose_name": "Trade Fair / Market Opportunity",
                "verbose_name_plural": "Trade Fair & Market Opportunities",
                "ordering": ["order", "title"],
            },
        ),
    ]
