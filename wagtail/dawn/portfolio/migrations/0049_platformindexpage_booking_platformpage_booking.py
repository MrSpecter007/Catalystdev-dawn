from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio", "0048_platformindexpage_platformpage"),
    ]

    operations = [
        migrations.AddField(
            model_name="platformindexpage",
            name="booking_url",
            field=models.URLField(
                blank=True,
                help_text="Primary booking link (Calendly, etc.) used as fallback for all platform cards.",
            ),
        ),
        migrations.AddField(
            model_name="platformindexpage",
            name="booking_cta_text",
            field=models.CharField(blank=True, default="Book a Walkthrough", max_length=100),
        ),
        migrations.AddField(
            model_name="platformpage",
            name="outcome",
            field=models.TextField(
                blank=True,
                help_text="2–3 outcome-focused bullet points, one per line.",
            ),
        ),
        migrations.AddField(
            model_name="platformpage",
            name="booking_url",
            field=models.URLField(
                blank=True,
                help_text="Per-platform booking link. Falls back to the index page booking URL.",
            ),
        ),
        migrations.AddField(
            model_name="platformpage",
            name="booking_label",
            field=models.CharField(blank=True, default="Book to View", max_length=100),
        ),
        migrations.AlterField(
            model_name="platformpage",
            name="status",
            field=models.CharField(
                choices=[
                    ("live", "Live"),
                    ("in_demo", "In Demo"),
                    ("coming_soon", "Coming Soon"),
                ],
                default="live",
                max_length=20,
            ),
        ),
    ]
