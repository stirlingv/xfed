from django.shortcuts import render
from django.templatetags.static import static
from .models import Banner, Feature

def index(request):
    banner = Banner.objects.first()
    features = Feature.objects.all()
    if not features.exists():
        # Provide default features if DB is empty
        features = [
            {'icon': 'fa-gem', 'title': 'Taxes', 'description': 'Expert tax preparation and planning for individuals and businesses.'},
            {'icon': 'fa-paper-plane', 'title': 'Data Science', 'description': 'Data-driven insights to optimize your financial decisions.'},
            {'icon': 'fa-rocket', 'title': 'Information Technology', 'description': 'Secure and efficient IT solutions for your tax data.'},
            {'icon': 'fa-signal', 'title': 'Veterans Affairs', 'description': 'Specialized support for veterans and their families.'},
        ]
        features_from_db = False
    else:
        features_from_db = True

    context = {
        'banner': {
            'heading': banner.heading if banner else "XFED Tax Solutions",
            'subheading': banner.subheading if banner else "Former Feds Making The System Work For You!",
            'description1': banner.description1 if banner else "XFED Tax Solutions is committed to providing efficient and effective tax and tax related services to America's taxpayer population.",
            'description2': banner.description2 if banner else "Whether you are an individual or business or both, America's largest network of former IRS tax professionals can provide the services you need.",
            'description3': banner.description3 if banner else "For specific information about how we can help you, please fill out our <a href='#'>brief questionnaire</a> or call us at [Justin's Personal Cell Phone Number].",
            'button_text': banner.button_text if banner else "Learn More",
            'button_link': banner.button_link if banner else "#",
            'image': banner.image.url if (banner and banner.image) else static('images/xfed_logo.png'),
        },
        'features': features if not features_from_db else features,
        'features_from_db': features_from_db,
    }
    return render(request, 'index.html', context)

def generic(request):
    return render(request, 'generic.html')
def elements(request):
    return render(request, 'elements.html')