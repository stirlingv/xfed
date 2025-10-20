from django.contrib import admin
from .models import (Banner, Feature, Post, MiniPost, ContactInfo, Footer, 
                    GenericPageSection, PageContent, NavigationItem, SocialMediaLink)

# Configure admin site headers
admin.site.site_header = "XFED Website Admin"
admin.site.site_title = "XFED Admin"
admin.site.index_title = "Website Content Management"

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('heading', 'subheading')
    fieldsets = (
        ('Main Banner Content', {
            'fields': ('heading', 'subheading'),
            'description': 'This content appears at the top of your homepage'
        }),
        ('Banner Descriptions', {
            'fields': ('description1', 'description2', 'description3'),
            'description': 'Three paragraphs that appear below the main headline'
        }),
        ('Call-to-Action Button', {
            'fields': ('button_text', 'button_link'),
            'description': 'The button that appears in the banner section'
        }),
        ('Banner Image', {
            'fields': ('image',),
            'description': 'Optional image that appears on the right side of the banner'
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one banner instance
        return not Banner.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion of banner
        return False

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'get_description_preview')
    list_filter = ('icon',)
    fields = ('icon', 'title', 'description')
    ordering = ('title',)
    
    def get_description_preview(self, obj):
        return obj.description[:50] + "..." if len(obj.description) > 50 else obj.description
    get_description_preview.short_description = "Description Preview"
    
    class Meta:
        verbose_name = "Service Feature"
        verbose_name_plural = "Service Features (More About Us Section)"

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_description_preview', 'button_text', 'has_image')
    list_filter = ('button_text',)
    fields = ('title', 'description', 'image', 'button_text', 'button_link')
    search_fields = ('title', 'description')
    
    def get_description_preview(self, obj):
        return obj.description[:50] + "..." if len(obj.description) > 50 else obj.description
    get_description_preview.short_description = "Description Preview"
    
    def has_image(self, obj):
        return bool(obj.image)
    has_image.boolean = True
    has_image.short_description = "Has Image"
    
    class Meta:
        verbose_name = "Blog Article"
        verbose_name_plural = "Blog Articles (Main Content Section)"

@admin.register(MiniPost)
class MiniPostAdmin(admin.ModelAdmin):
    list_display = ('get_description_preview', 'has_image')
    fields = ('description', 'image')
    
    def get_description_preview(self, obj):
        return obj.description[:50] + "..." if len(obj.description) > 50 else obj.description
    get_description_preview.short_description = "Description Preview"
    
    def has_image(self, obj):
        return bool(obj.image)
    has_image.boolean = True
    has_image.short_description = "Has Image"
    
    class Meta:
        verbose_name = "Sidebar Mini Post"
        verbose_name_plural = "Sidebar Mini Posts"

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'get_address_preview')
    fields = ('email', 'phone', 'address')
    
    def get_address_preview(self, obj):
        return obj.address[:30] + "..." if len(obj.address) > 30 else obj.address
    get_address_preview.short_description = "Address Preview"
    
    def has_add_permission(self, request):
        # Only allow one contact info instance
        return not ContactInfo.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion of contact info
        return False
    
    class Meta:
        verbose_name = "Contact Information"
        verbose_name_plural = "Contact Information"

@admin.register(Footer)
class FooterAdmin(admin.ModelAdmin):
    list_display = ('get_copyright_preview', 'has_demo_link', 'has_design_link')
    fields = ('copyright', 'demo_images_link', 'design_link')
    
    def get_copyright_preview(self, obj):
        return obj.copyright[:50] + "..." if len(obj.copyright) > 50 else obj.copyright
    get_copyright_preview.short_description = "Copyright Text"
    
    def has_demo_link(self, obj):
        return bool(obj.demo_images_link)
    has_demo_link.boolean = True
    has_demo_link.short_description = "Has Demo Link"
    
    def has_design_link(self, obj):
        return bool(obj.design_link)
    has_design_link.boolean = True
    has_design_link.short_description = "Has Design Link"
    
    def has_add_permission(self, request):
        # Only allow one footer instance
        return not Footer.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion of footer
        return False

@admin.register(GenericPageSection)
class GenericPageSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_content_preview', 'has_image')
    fields = ('title', 'content', 'image')
    search_fields = ('title', 'content')
    
    def get_content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    get_content_preview.short_description = "Content Preview"
    
    def has_image(self, obj):
        return bool(obj.image)
    has_image.boolean = True
    has_image.short_description = "Has Image"
    
    class Meta:
        verbose_name = "Generic Page Section"
        verbose_name_plural = "Generic Page Sections"

@admin.register(PageContent)
class PageContentAdmin(admin.ModelAdmin):
    list_display = ('page', 'section_type', 'title', 'order', 'is_active')
    list_filter = ('page', 'section_type', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'content')
    ordering = ('page', 'section_type', 'order')
    
    fieldsets = (
        ('Page Information', {
            'fields': ('page', 'section_type'),
            'description': 'Select which page and section type this content belongs to'
        }),
        ('Content', {
            'fields': ('title', 'content'),
            'description': 'The main content for this section'
        }),
        ('Media', {
            'fields': ('image',),
            'description': 'Optional image for this section'
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active'),
            'description': 'Control how and where this content appears'
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()

@admin.register(NavigationItem)
class NavigationItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent', 'url', 'order', 'is_active')
    list_filter = ('parent', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'url')
    ordering = ('order',)
    
    fieldsets = (
        ('Menu Item Details', {
            'fields': ('title', 'url'),
            'description': 'The text and link for this menu item'
        }),
        ('Menu Structure', {
            'fields': ('parent',),
            'description': 'Leave blank for top-level menu items, or select a parent for sub-menu items'
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active'),
            'description': 'Control the order and visibility of this menu item'
        }),
    )

@admin.register(SocialMediaLink)
class SocialMediaLinkAdmin(admin.ModelAdmin):
    list_display = ('platform', 'url', 'order', 'is_active')
    list_filter = ('platform', 'is_active')
    list_editable = ('order', 'is_active')
    ordering = ('order',)
    
    fieldsets = (
        ('Social Media Details', {
            'fields': ('platform', 'url'),
            'description': 'Select the platform and enter your profile URL'
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active'),
            'description': 'Control the order and visibility of this social media link'
        }),
    )