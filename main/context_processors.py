from .models import ContactInfo, Footer, SocialMediaLink, NavigationItem, MiniPost, DynamicPage

def global_context(request):
    """
    Add global context data that should be available in all templates
    """
    context = {}

    # Get contact information
    contact_info = ContactInfo.objects.first()
    if contact_info:
        context['contact_info'] = contact_info

    # Get footer information
    footer = Footer.objects.first()
    if footer:
        context['footer'] = footer

    # Get active social media links
    context['social_links'] = SocialMediaLink.objects.filter(is_active=True).order_by('order')

    # Get active navigation items
    # Top-level items (no parent)
    context['nav_items'] = NavigationItem.objects.filter(
        is_active=True,
        parent=None
    ).order_by('order').prefetch_related('children')

    # Get active mini posts for sidebar
    context['mini_posts'] = MiniPost.objects.all()[:3]  # Limit to 3 posts

    # Get published dynamic pages that should show in navigation
    context['dynamic_nav_pages'] = DynamicPage.objects.filter(
        is_published=True,
        show_in_navigation=True
    ).order_by('navigation_order', 'title')

    return context
