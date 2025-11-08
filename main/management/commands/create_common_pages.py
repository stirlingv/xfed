from django.core.management.base import BaseCommand
from main.models import DynamicPage, PageContent


class Command(BaseCommand):
    help = 'Create common pages that are often used in navigation'

    def add_arguments(self, parser):
        parser.add_argument(
            '--pages',
            nargs='+',
            default=['contact', 'about', 'services', 'privacy', 'terms'],
            help='Space-separated list of page slugs to create'
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating common pages for navigation...'))

        page_templates = {
            'contact': {
                'title': 'Contact Us',
                'content': 'Get in touch with our team. We\'re here to help with all your tax and financial needs.',
                'template_type': 'generic',
                'meta_description': 'Contact XFED Tax Solutions for professional tax and financial services.'
            },
            'about': {
                'title': 'About Us',
                'content': 'Learn more about XFED Tax Solutions and our team of former federal employees.',
                'template_type': 'generic',
                'meta_description': 'Learn about XFED Tax Solutions and our experienced team of former federal employees.'
            },
            'services': {
                'title': 'Our Services',
                'content': 'Comprehensive tax and financial services from experienced professionals.',
                'template_type': 'generic',
                'meta_description': 'Professional tax preparation, financial planning, and business consulting services.'
            },
            'privacy': {
                'title': 'Privacy Policy',
                'content': 'Our commitment to protecting your personal information and data.',
                'template_type': 'generic',
                'meta_description': 'XFED Tax Solutions privacy policy and data protection commitment.'
            },
            'terms': {
                'title': 'Terms of Service',
                'content': 'Terms and conditions for using our services and website.',
                'template_type': 'generic',
                'meta_description': 'Terms of service and conditions for XFED Tax Solutions clients.'
            }
        }

        created_count = 0
        updated_count = 0

        for page_slug in options['pages']:
            if page_slug in page_templates:
                template = page_templates[page_slug]

                page, created = DynamicPage.objects.get_or_create(
                    slug=page_slug,
                    defaults={
                        'title': template['title'],
                        'template_type': template['template_type'],
                        'meta_description': template['meta_description'],
                        'is_published': True,
                        'show_in_navigation': True,
                        'navigation_order': len(DynamicPage.objects.all()) * 10,
                    }
                )

                if created:
                    # Create initial page content section
                    PageContent.objects.create(
                        page=page.slug,
                        section_type='main_content',
                        title=f'{page.title} Content',
                        content=template['content'],
                        order=1,
                        is_active=True
                    )

                    self.stdout.write(
                        self.style.SUCCESS(f'✓ Created page: {page.title} (/{page.slug}/)')
                    )
                    created_count += 1
                else:
                    self.stdout.write(
                        self.style.WARNING(f'• Page already exists: {page.title} (/{page.slug}/)')
                    )
                    updated_count += 1
            else:
                self.stdout.write(
                    self.style.ERROR(f'✗ Unknown page template: {page_slug}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\nSummary: {created_count} pages created, {updated_count} already existed'
            )
        )

        if created_count > 0:
            self.stdout.write(
                self.style.SUCCESS(
                    '\n💡 These pages are now available in the Navigation Item dropdown!'
                )
            )
