from django.shortcuts import render
from .models import Banner, Feature, Post, MiniPost, ContactInfo, Footer, GenericPageSection

def generic(request):
    sections = GenericPageSection.objects.all()
    return render(request, 'generic.html', {'sections': sections})

def index(request):
    context = {
        'banner': Banner.objects.first(),
        'features': Feature.objects.all(),
        'posts': Post.objects.all(),
        'miniposts': MiniPost.objects.all(),
        'contact': ContactInfo.objects.first(),
        'footer': Footer.objects.first(),
    }
    return render(request, 'index.html', context)

def elements(request):
    return render(request, 'elements.html')

def generic(request):
    return render(request, 'generic.html')