from django.conf import settings
from django.db import migrations


def update_site(apps, schema_editor):
    Site = apps.get_model("sites", "Site")
    site = Site.objects.get_or_create(id=getattr(settings, "SITE_ID", 1))[0]
    site.domain = settings.SITE_DOMAIN
    site.name = settings.SITE_NAME
    site.save()


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
        ("sites", "0002_alter_domain_unique"),
    ]

    operations = [
        migrations.RunPython(update_site),
    ]