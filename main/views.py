from django.shortcuts import render
from django.templatetags.static import static
from .models import Banner, Feature, Post, PageContent

def index(request):
    """Homepage view with banner and features"""
    # Get banner content (only one should exist)
    banner = Banner.objects.first()
    
    # Create default banner if none exists in database
    if not banner:
        # Create a default banner object (not saved to database)
        banner = Banner(
            heading="XFED Tax Solutions",
            subheading="Former Feds Making The System Work For You!",
            description1="XFED Tax Solutions is committed to providing efficient and effective tax and tax related services to America's taxpayer population.",
            description2="Whether you are an individual or business or both, America's largest network of former IRS tax professionals can provide the services you need.",
            description3="For specific information about how we can help you, please fill out our <a href='#'>brief questionnaire</a> or call us at [Justin's Personal Cell Phone Number].",
            button_text="Learn More",
            button_link="#"
        )
    
    # Get active features
    features = Feature.objects.all()
    
    # Fallback features if none exist in database
    if not features.exists():
        features = [
            {'icon': 'fa-gem', 'title': 'Taxes', 'description': 'Expert tax preparation and planning for individuals and businesses.'},
            {'icon': 'fa-paper-plane', 'title': 'Data Science', 'description': 'Data-driven insights to optimize your financial decisions.'},
            {'icon': 'fa-rocket', 'title': 'Information Technology', 'description': 'Secure and efficient IT solutions for your tax data.'},
            {'icon': 'fa-signal', 'title': 'Veterans Affairs', 'description': 'Specialized support for veterans and their families.'},
        ]
        features_from_db = False
    else:
        features_from_db = True

    # Get active posts for the bottom section
    posts = Post.objects.all()[:6]  # Limit to 6 posts as shown in template

    context = {
        'banner': banner,
        'features': features,
        'features_from_db': features_from_db,
        'posts': posts,
    }
    return render(request, 'index.html', context)

def generic(request):
    """Generic page view - can be made dynamic with PageContent model"""
    # Get page content for generic page
    page_sections = PageContent.objects.filter(
        page='generic', 
        is_active=True
    ).order_by('section_type', 'order')
    
    context = {
        'page_sections': page_sections,
    }
    return render(request, 'generic.html', context)

def elements(request):
    """Elements page view - can be made dynamic with PageContent model"""
    # Get page content for elements page
    page_sections = PageContent.objects.filter(
        page='elements', 
        is_active=True
    ).order_by('section_type', 'order')
    
    context = {
        'page_sections': page_sections,
    }
    return render(request, 'elements.html', context)