# Follow-up to 0016: the original 8(a) pivot banner copy was too long and
# produced a large empty margin around the logo (a fixed-aspect graphic
# forced to stretch to match a tall text column). This migration re-applies
# the now-shortened banner copy from main.seed_content. A plain code change
# to seed_content.py is not enough on its own — migration 0016 already ran
# in production and will not re-run just because the module it imported from
# changed, so the shorter copy needs its own migration to reach the database.
from django.db import migrations

from main import seed_content


def apply_shorter_banner(apps, schema_editor):
    Banner = apps.get_model('main', 'Banner')
    banner = Banner.objects.order_by('pk').first()
    if banner:
        for field, value in seed_content.PIVOT_BANNER.items():
            setattr(banner, field, value)
        banner.save()
    else:
        Banner.objects.create(**seed_content.PIVOT_BANNER)


def revert_shorter_banner(apps, schema_editor):
    # Content-only migration; reverting code does not need to restore old copy.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_8a_set_aside_pivot'),
    ]

    operations = [
        migrations.RunPython(apply_shorter_banner, revert_shorter_banner),
    ]
