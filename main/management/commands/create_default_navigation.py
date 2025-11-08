from django.core.management.base import BaseCommand
from main.models import NavigationItem, SocialMediaLink


class Command(BaseCommand):
    help = 'Create default navigation items and social media links'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Setting up default navigation...'))

        # Clear existing navigation items to avoid duplicates
        NavigationItem.objects.all().delete()
        SocialMediaLink.objects.all().delete()

        # Create main navigation items
        home = NavigationItem.objects.create(
            title="Homepage",
            url="/",
            order=10,
            icon_class="fa-home"
        )

        # Services menu with dropdown
        services = NavigationItem.objects.create(
            title="Services",
            url="#",
            order=20,
            icon_class="fa-briefcase"
        )

        # Services submenu items
        NavigationItem.objects.create(
            title="Tax Preparation",
            url="/services/tax-preparation/",
            parent=services,
            order=10
        )

        NavigationItem.objects.create(
            title="Financial Planning",
            url="/services/financial-planning/",
            parent=services,
            order=20
        )

        NavigationItem.objects.create(
            title="Business Consulting",
            url="/services/business-consulting/",
            parent=services,
            order=30
        )

        NavigationItem.objects.create(
            title="Veterans Services",
            url="/services/veterans/",
            parent=services,
            order=40
        )

        # About page
        NavigationItem.objects.create(
            title="About Us",
            url="/about/",
            order=30,
            icon_class="fa-users"
        )

        # Resources menu with dropdown
        resources = NavigationItem.objects.create(
            title="Resources",
            url="#",
            order=40,
            icon_class="fa-folder-open"
        )

        # Resources submenu items
        NavigationItem.objects.create(
            title="Tax Documents",
            url="/resources/documents/",
            parent=resources,
            order=10
        )

        NavigationItem.objects.create(
            title="Forms & Checklists",
            url="/resources/forms/",
            parent=resources,
            order=20
        )

        NavigationItem.objects.create(
            title="Planning Tools",
            url="/resources/tools/",
            parent=resources,
            order=30
        )

        NavigationItem.objects.create(
            title="Client Portal",
            url="/portal/",
            parent=resources,
            order=40,
            opens_new_window=True
        )

        # Contact page
        NavigationItem.objects.create(
            title="Contact",
            url="/contact/",
            order=50,
            icon_class="fa-envelope"
        )

        # News & Updates
        NavigationItem.objects.create(
            title="News & Updates",
            url="/news/",
            order=60,
            icon_class="fa-newspaper"
        )

        # Client Testimonials
        NavigationItem.objects.create(
            title="Client Testimonials",
            url="/testimonials/",
            order=70,
            icon_class="fa-star"
        )

        # Schedule Appointment
        NavigationItem.objects.create(
            title="Schedule Appointment",
            url="/schedule/",
            order=80,
            icon_class="fa-calendar"
        )

        # Create default social media links (placeholder URLs)
        SocialMediaLink.objects.create(
            platform="facebook-f",
            url="https://facebook.com/xfedtax",
            order=10
        )

        SocialMediaLink.objects.create(
            platform="twitter",
            url="https://twitter.com/xfedtax",
            order=20
        )

        SocialMediaLink.objects.create(
            platform="linkedin-in",
            url="https://linkedin.com/company/xfed",
            order=30
        )

        SocialMediaLink.objects.create(
            platform="envelope",
            url="mailto:contact@xfedtax.com",
            order=40
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {NavigationItem.objects.count()} navigation items '
                f'and {SocialMediaLink.objects.count()} social media links'
            )
        )
