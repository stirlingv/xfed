"""
Sitemap configuration for HireXFed.
Helps Google discover and index all pages on the site.
"""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import DynamicPage


class StaticViewSitemap(Sitemap):
    """Sitemap for static pages."""
    priority = 0.8
    changefreq = 'weekly'
    protocol = 'https'

    def items(self):
        return ['index']

    def location(self, item):
        return reverse(item)


class DynamicPageSitemap(Sitemap):
    """Sitemap for dynamic pages created through the admin."""
    changefreq = 'weekly'
    protocol = 'https'

    def items(self):
        return DynamicPage.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return f'/{obj.slug}/'

    def priority(self, obj):
        # Higher priority for main pages
        if obj.slug in ['tax-solutions', 'members', 'services', 'contact']:
            return 0.9
        elif 'services' in obj.slug:
            return 0.8
        return 0.6
