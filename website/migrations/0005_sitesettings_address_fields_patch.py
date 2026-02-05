from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ("website", "0004_merge_20260204_1636"),
    ]

    operations = [
        migrations.AddField(
            model_name="sitesettings",
            name="address_line1",
            field=models.CharField(max_length=160, blank=True, default=""),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="address_line2",
            field=models.CharField(max_length=160, blank=True, default=""),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="postal_code",
            field=models.CharField(max_length=20, blank=True, default=""),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="city",
            field=models.CharField(max_length=80, blank=True, default=""),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="country",
            field=models.CharField(max_length=80, blank=True, default=""),
        ),
    ]
