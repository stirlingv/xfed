"""
URL configuration for xfed project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from main import views
from main.sitemaps import StaticViewSitemap, DynamicPageSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'pages': DynamicPageSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'), name='robots'),
    path('', views.index, name='index'),
    path('generic/', views.generic, name='generic'),
    path('elements/', views.elements, name='elements'),
    # Admin helper views
    path('admin-helper/add-page/', views.add_page_popup, name='add_page_popup'),
    # Intake forms
    path('intake/<slug:slug>/', views.intake_form_view, name='intake_form'),
    # Dynamic pages - these should be last to catch custom page URLs
    path('<slug:slug>/', views.dynamic_page_view, name='dynamic_page'),
    # Nested dynamic pages (e.g., tax-solutions/services)
    path('<path:slug>/', views.dynamic_page_view, name='dynamic_page_nested'),
]

# Serve static and media files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
