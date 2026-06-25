from django.conf import settings
from django.db import migrations


def create_google_app(apps, schema_editor):
    SocialApp = apps.get_model("socialaccount", "SocialApp")
    Site = apps.get_model("sites", "Site")

    client_id = getattr(settings, "GOOGLE_CLIENT_ID", None)
    client_secret = getattr(settings, "GOOGLE_CLIENT_SECRET", None)

    if not client_id or not client_secret:
        return

    app, _ = SocialApp.objects.get_or_create(
        provider="google",
        defaults={
            "name": "Google",
            "client_id": client_id,
            "secret": client_secret,
        },
    )
    site = Site.objects.get_current()
    app.sites.add(site)


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_update_site_data"),
        ("socialaccount", "0006_alter_socialaccount_extra_data"),
    ]

    operations = [
        migrations.RunPython(create_google_app),
    ]