# Content migration: pivot the site's seeded content to the 8(a) / small
# business set-aside focus. build.sh runs `migrate` on every deploy, so this
# applies the pivot to production without a manual content-setup step.
#
# Content lives in main.seed_content (pure data, no models) and is shared with
# the setup_hirexfed_content command. Editing seed_content later changes what
# this migration would seed on a fresh database — acceptable for marketing
# content, where "latest copy" is always the right answer.
from django.db import migrations

from main import seed_content


def apply_pivot(apps, schema_editor):
    Banner = apps.get_model('main', 'Banner')
    Feature = apps.get_model('main', 'Feature')
    Post = apps.get_model('main', 'Post')
    MiniPost = apps.get_model('main', 'MiniPost')
    DynamicPage = apps.get_model('main', 'DynamicPage')
    PageContent = apps.get_model('main', 'PageContent')
    NavigationItem = apps.get_model('main', 'NavigationItem')
    IntakeForm = apps.get_model('main', 'IntakeForm')
    IntakeField = apps.get_model('main', 'IntakeField')

    # Banner
    banner = Banner.objects.order_by('pk').first()
    if banner:
        for field, value in seed_content.PIVOT_BANNER.items():
            setattr(banner, field, value)
        banner.save()
    else:
        Banner.objects.create(**seed_content.PIVOT_BANNER)

    # Homepage service tiles
    Feature.objects.filter(title__in=seed_content.RETIRED_FEATURE_TITLES).delete()
    for feature in seed_content.PIVOT_FEATURES:
        Feature.objects.update_or_create(
            title=feature['title'],
            defaults={'icon': feature['icon'], 'description': feature['description']},
        )

    # Resource posts
    Post.objects.filter(title__in=seed_content.RETIRED_POST_TITLES).delete()
    for post in seed_content.PIVOT_POSTS:
        Post.objects.update_or_create(
            title=post['title'],
            defaults={
                'description': post['description'],
                'button_text': post['button_text'],
                'button_link': post['button_link'],
            },
        )

    # Sidebar mini posts
    for snippet in seed_content.RETIRED_MINI_POST_SNIPPETS:
        MiniPost.objects.filter(description__icontains=snippet).delete()
    for mini in seed_content.PIVOT_MINI_POSTS:
        MiniPost.objects.get_or_create(description=mini['description'])

    # Landing + checklist pages
    for page_data in (seed_content.PAGE_8A_TAX_HELP, seed_content.PAGE_8A_CHECKLIST):
        DynamicPage.objects.update_or_create(
            slug=page_data['slug'],
            defaults={
                'title': page_data['title'],
                'template_type': 'generic',
                'meta_description': page_data['meta_description'],
                'is_published': True,
                'show_in_navigation': False,
            },
        )
        PageContent.objects.update_or_create(
            page=page_data['slug'],
            section_type='main_content',
            order=1,
            defaults={
                'title': page_data['content_title'],
                'content': page_data['content'],
                'is_active': True,
            },
        )

    # Navigation entry (only when a nav already exists; a fresh install gets
    # its navigation from setup_hirexfed_content instead)
    if NavigationItem.objects.exists():
        NavigationItem.objects.get_or_create(
            title=seed_content.NAV_8A_ITEM['title'],
            parent=None,
            defaults={
                'url': seed_content.NAV_8A_ITEM['url'],
                'order': seed_content.NAV_8A_ITEM['order'],
                'is_active': True,
            },
        )

    # Consultation intake form (update in place if it exists)
    form = IntakeForm.objects.filter(slug='client-consultation').first()
    if form:
        form.description = seed_content.CONSULTATION_PIVOT['description']
        form.save()
        IntakeField.objects.filter(form=form, field_name='issue_type').update(
            choices=seed_content.CONSULTATION_PIVOT['issue_type_choices'],
        )


def revert_pivot(apps, schema_editor):
    # Content-only migration; reverting code does not need to restore old copy.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_slack_only_notifications'),
    ]

    operations = [
        migrations.RunPython(apply_pivot, revert_pivot),
    ]
