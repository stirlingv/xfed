import mimetypes
from pathlib import Path
from urllib.parse import quote

from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.urls import path, reverse
from django.utils.html import format_html
from .models import (Banner, Feature, Post, MiniPost, ContactInfo, Footer,
                    GenericPageSection, PageContent, DynamicPage,
                    IntakeForm, IntakeField, IntakeSubmission, IntakeFile,
                    NavigationItem, SocialMediaLink)

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



# Inline admin for PageContent to manage page sections
class PageContentInline(admin.TabularInline):
    model = PageContent
    extra = 1
    fields = ('section_type', 'title', 'content', 'order', 'is_active')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if hasattr(self, 'instance') and self.instance.pk:
            return qs.filter(page=self.instance.slug)
        return qs.none()

@admin.register(DynamicPage)
class DynamicPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'template_type', 'is_published', 'show_in_navigation', 'updated_at')
    list_filter = ('template_type', 'is_published', 'show_in_navigation', 'created_at')
    list_editable = ('is_published', 'show_in_navigation')
    search_fields = ('title', 'slug', 'meta_description')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('navigation_order', 'title')

    # Use fieldsets for better organization
    fieldsets = (
        ('Page Information', {
            'fields': ('title', 'slug', 'template_type'),
            'description': 'Basic page settings - the title appears in browser tabs and headers'
        }),
        ('SEO & Meta Data', {
            'fields': ('meta_description',),
            'description': 'Search engine optimization settings'
        }),
        ('Publication Settings', {
            'fields': ('is_published', 'show_in_navigation', 'navigation_order'),
            'description': 'Control page visibility and navigation placement'
        }),
    )

    inlines = []  # We'll add content management through a separate interface

    # Temporarily disable readonly fields to avoid form errors
    # def get_readonly_fields(self, request, obj=None):
    #     if obj:  # editing an existing object
    #         return ['slug']
    #     return []

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:  # New page
            # Create default content sections based on template type
            if obj.template_type == 'generic':
                PageContent.objects.create(
                    page=obj.slug,
                    section_type='header',
                    title=f'Welcome to {obj.title}',
                    content='Edit this header content in the Page Content section.',
                    order=0
                )
                PageContent.objects.create(
                    page=obj.slug,
                    section_type='main_content',
                    title='Main Content',
                    content='<p>Add your main page content here. You can use HTML formatting.</p>',
                    order=1
                )
            elif obj.template_type == 'elements':
                PageContent.objects.create(
                    page=obj.slug,
                    section_type='header',
                    title=f'{obj.title} - Elements & Features',
                    content='This page showcases various design elements and interactive features.',
                    order=0
                )

    def response_add(self, request, obj, post_url_continue=None):
        response = super().response_add(request, obj, post_url_continue)
        if '_continue' not in request.POST:
            # Redirect to PageContent admin filtered for this page
            from django.shortcuts import redirect
            return redirect(f'/admin/main/pagecontent/?page__exact={obj.slug}')
        return response

    class Media:
        css = {
            'all': ('admin/css/dynamic_page_admin.css',)
        }
        js = ('admin/js/dynamic_page_admin.js',)

# Intake Form Admin Configuration

class IntakeFieldInline(admin.TabularInline):
    model = IntakeField
    extra = 1
    fields = ('label', 'field_name', 'field_type', 'placeholder', 'is_required', 'order')
    ordering = ['order']

@admin.register(IntakeForm)
class IntakeFormAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_active', 'allow_file_uploads', 'updated_at')
    list_filter = ('is_active', 'allow_file_uploads', 'created_at')
    list_editable = ('is_active',)
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}

    fieldsets = (
        ('Form Information', {
            'fields': ('title', 'slug', 'description'),
            'description': 'Basic form settings and description'
        }),
        ('Email & Messages', {
            'fields': ('email_recipients', 'success_message'),
            'description': 'Configure email notifications and success messages'
        }),
        ('Form Options', {
            'fields': ('is_active', 'allow_file_uploads'),
            'description': 'Control form availability and features'
        }),
    )

    inlines = [IntakeFieldInline]

    # Temporarily disable readonly fields to avoid form errors until migrations are run
    # def get_readonly_fields(self, request, obj=None):
    #     if obj:  # editing an existing object
    #         return ['slug']
    #     return []

@admin.register(IntakeField)
class IntakeFieldAdmin(admin.ModelAdmin):
    list_display = ('form', 'label', 'field_type', 'is_required', 'order')
    list_filter = ('form', 'field_type', 'is_required')
    list_editable = ('order',)
    search_fields = ('label', 'field_name')
    ordering = ('form', 'order')

    fieldsets = (
        ('Field Configuration', {
            'fields': ('form', 'label', 'field_name', 'field_type'),
            'description': 'Basic field settings'
        }),
        ('Field Options', {
            'fields': ('placeholder', 'choices', 'help_text'),
            'description': 'Additional field configuration'
        }),
        ('Display Settings', {
            'fields': ('is_required', 'order'),
            'description': 'Field behavior and positioning'
        }),
    )

class IntakeFileInline(admin.TabularInline):
    model = IntakeFile
    extra = 0
    readonly_fields = ('preview_link', 'original_filename', 'uploaded_at')
    fields = ('preview_link', 'file', 'original_filename', 'uploaded_at')

    def preview_link(self, obj):
        if not obj.pk or not obj.file:
            return "-"
        preview_url = reverse(
            'admin:main_intakesubmission_file_preview',
            args=[obj.submission_id, obj.pk],
        )
        return format_html(
            '<a href="{}" target="_blank" rel="noopener">Preview</a>',
            preview_url
        )
    preview_link.short_description = "Preview"

@admin.register(IntakeSubmission)
class IntakeSubmissionAdmin(admin.ModelAdmin):
    list_display = (
        'get_client_name', 'form', 'status', 'priority', 'assigned_to',
        'submitted_at', 'days_since_submission', 'needs_followup_flag', 'has_files'
    )
    list_filter = (
        'status', 'priority', 'form', 'assigned_to',
        'submitted_at', 'first_contacted_at'
    )
    list_editable = ('status', 'priority', 'assigned_to')
    search_fields = ('data', 'admin_notes')
    ordering = ['-submitted_at']
    readonly_fields = (
        'form', 'submitted_at', 'ip_address', 'data', 'status_updated_at',
        'days_since_submission', 'get_formatted_data'
    )

    fieldsets = (
        ('Client Information', {
            'fields': ('get_formatted_data',),
            'description': 'Information submitted by the client'
        }),
        ('Submission Details', {
            'fields': ('form', 'submitted_at', 'ip_address', 'status_updated_at'),
            'description': 'Technical submission information'
        }),
        ('Status & Assignment', {
            'fields': ('status', 'priority', 'assigned_to'),
            'description': 'Current status and assignment'
        }),
        ('Contact Tracking', {
            'fields': ('first_contacted_at', 'last_contact_at', 'next_followup_date'),
            'description': 'Track contact attempts and follow-up dates'
        }),
        ('Internal Notes', {
            'fields': ('admin_notes',),
            'description': 'Internal notes and comments (not visible to client)',
            'classes': ['wide']
        }),
        ('Raw Data (Technical)', {
            'fields': ('data',),
            'description': 'Raw JSON data submitted by the user',
            'classes': ['collapse']
        }),
    )

    inlines = [IntakeFileInline]

    # Custom admin actions
    actions = ['mark_as_contacted', 'mark_as_scheduled', 'mark_as_completed', 'assign_to_me']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:submission_id>/file/<int:file_id>/preview/',
                self.admin_site.admin_view(self.preview_uploaded_file),
                name='main_intakesubmission_file_preview',
            ),
        ]
        return custom_urls + urls

    def preview_uploaded_file(self, request, submission_id, file_id):
        submission = get_object_or_404(IntakeSubmission, pk=submission_id)
        if not self.has_view_or_change_permission(request, submission):
            raise PermissionDenied

        intake_file = get_object_or_404(IntakeFile, pk=file_id, submission=submission)
        storage_file = intake_file.file.open('rb')
        filename = Path(intake_file.original_filename or intake_file.file.name).name
        content_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"

        response = FileResponse(storage_file, content_type=content_type)
        response["Content-Disposition"] = f"inline; filename*=UTF-8''{quote(filename)}"
        return response

    def get_client_name(self, obj):
        """Display client name"""
        return obj.get_client_name()
    get_client_name.short_description = "Client Name"
    get_client_name.admin_order_field = 'submitted_at'  # Allow sorting

    def get_formatted_data(self, obj):
        """Display submitted data in a readable format"""
        if not obj.data:
            return "No data submitted"

        from django.utils.html import format_html
        html_parts = []

        # Contact information first
        contact_info = obj.get_contact_info()
        if contact_info['email']:
            html_parts.append(f"<strong>Email:</strong> <a href='mailto:{contact_info['email']}'>{contact_info['email']}</a>")
        if contact_info['phone']:
            html_parts.append(f"<strong>Phone:</strong> <a href='tel:{contact_info['phone']}'>{contact_info['phone']}</a>")

        html_parts.append("<hr>")

        # All form data
        for key, value in obj.data.items():
            if value:  # Only show non-empty values
                html_parts.append(f"<strong>{key}:</strong> {value}")

        return format_html("<br>".join(html_parts))
    get_formatted_data.short_description = "Submitted Information"

    def days_since_submission(self, obj):
        """Show days since submission"""
        days = obj.days_since_submission()
        if days == 0:
            return "Today"
        elif days == 1:
            return "1 day ago"
        else:
            return f"{days} days ago"
    days_since_submission.short_description = "Age"

    def needs_followup_flag(self, obj):
        """Visual indicator for submissions needing follow-up"""
        return obj.needs_followup()
    needs_followup_flag.boolean = True
    needs_followup_flag.short_description = "Needs Follow-up"

    def has_files(self, obj):
        """Check if submission has uploaded files"""
        return obj.files.exists()
    has_files.boolean = True
    has_files.short_description = "Has Files"

    # Custom actions
    def mark_as_contacted(self, request, queryset):
        """Mark submissions as contacted"""
        from django.utils import timezone
        updated = 0
        for submission in queryset:
            if submission.status == 'new':
                submission.status = 'contacted'
                if not submission.first_contacted_at:
                    submission.first_contacted_at = timezone.now()
                submission.last_contact_at = timezone.now()
                submission.save()
                updated += 1

        self.message_user(request, f"Marked {updated} submission(s) as contacted.")
    mark_as_contacted.short_description = "Mark selected as contacted"

    def mark_as_scheduled(self, request, queryset):
        """Mark submissions as scheduled"""
        updated = queryset.update(status='scheduled')
        self.message_user(request, f"Marked {updated} submission(s) as scheduled.")
    mark_as_scheduled.short_description = "Mark selected as scheduled"

    def mark_as_completed(self, request, queryset):
        """Mark submissions as completed"""
        updated = queryset.update(status='completed')
        self.message_user(request, f"Marked {updated} submission(s) as completed.")
    mark_as_completed.short_description = "Mark selected as completed"

    def assign_to_me(self, request, queryset):
        """Assign submissions to current user"""
        updated = queryset.update(assigned_to=request.user)
        self.message_user(request, f"Assigned {updated} submission(s) to you.")
    assign_to_me.short_description = "Assign selected to me"

    def has_add_permission(self, request):
        # Don't allow manual creation of submissions
        return False

    def changelist_view(self, request, extra_context=None):
        """Add dashboard stats to the changelist view"""
        extra_context = extra_context or {}

        # Get submission statistics
        from django.db.models import Count
        total_submissions = IntakeSubmission.objects.count()
        new_submissions = IntakeSubmission.objects.filter(status='new').count()
        need_followup = len([s for s in IntakeSubmission.objects.all() if s.needs_followup()])

        extra_context['submission_stats'] = {
            'total': total_submissions,
            'new': new_submissions,
            'need_followup': need_followup,
        }

        return super().changelist_view(request, extra_context)

    class Media:
        css = {
            'all': ('admin/css/intake_submission_admin.css',)
        }


@admin.register(NavigationItem)
class NavigationItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'url_display', 'parent', 'order', 'is_active', 'has_children_indicator')
    list_filter = ('is_active', 'parent')
    search_fields = ('title', 'url')
    list_editable = ('order', 'is_active')
    ordering = ('order', 'title')

    def get_fieldsets(self, request, obj=None):
        """Dynamic fieldsets based on whether we're adding or editing"""
        if obj is None:  # Adding new item
            return (
                ('Basic Information', {
                    'fields': ('title', 'url_choice', 'parent'),
                    'description': 'Configure the menu item title and destination. All links are validated to ensure they work correctly.',
                    'classes': ('wide',),
                }),
                ('Display Options', {
                    'fields': ('order', 'is_active', 'icon_class', 'opens_new_window'),
                    'description': 'Control how this menu item appears and behaves'
                }),
            )
        else:  # Editing existing item
            return (
                ('Basic Information', {
                    'fields': ('title', 'url', 'parent'),
                    'description': 'Configure the menu item title and where it links.',
                    'classes': ('wide',),
                }),
                ('Display Options', {
                    'fields': ('order', 'is_active', 'icon_class', 'opens_new_window'),
                    'description': 'Control how this menu item appears and behaves'
                }),
            )

    def get_form(self, request, obj=None, **kwargs):
        """Customize the form to add page choices and JavaScript"""
        # Only use custom form for new items
        if obj is None:  # Adding new item
            form = super().get_form(request, obj, **kwargs)

            # Get available pages for dropdown
            page_choices = self.get_page_choices()

            # Create a choice field for existing pages
            from django import forms
            from django.utils.safestring import mark_safe

            class NavigationItemForm(form):
                url_choice = forms.ChoiceField(
                    choices=page_choices,
                    required=True,
                    label="Link Destination",
                    help_text="Choose where this menu item should link to"
                )

                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    # Add "Add New Page" button info to the form
                    self.fields['url_choice'].help_text = (
                        'Choose where this menu item should link to. '
                        'Don\'t see the page you need? '
                        '<a href="#" onclick="openAddPagePopup(); return false;" '
                        'style="color: #0073aa; font-weight: bold;">+ Create New Page</a>'
                    )

                def clean(self):
                    cleaned_data = super().clean()
                    url_choice = cleaned_data.get('url_choice')

                    # Validate that a valid URL was selected
                    if not url_choice or url_choice == '' or url_choice.startswith('---'):
                        raise forms.ValidationError("Please select a valid page or link destination.")

                    # Set the actual url field
                    cleaned_data['url'] = url_choice
                    return cleaned_data

            return NavigationItemForm
        else:  # Editing existing item - use standard form
            return super().get_form(request, obj, **kwargs)

    def get_page_choices(self):
        """Get available pages for the dropdown - organized by type"""
        choices = [('', '-- Select where this menu item should link --')]

        # Main website pages
        main_pages = [
            ('/', '🏠 Homepage'),
            ('/generic/', '📄 Generic Demo Page'),
            ('/elements/', '🧩 Elements Demo Page'),
        ]

        # Add dynamic pages if they exist
        dynamic_pages = []
        try:
            for page in DynamicPage.objects.filter(is_published=True).order_by('title'):
                icon = '📝' if page.template_type == 'generic' else '🏠' if page.template_type == 'index' else '📋'
                dynamic_pages.append((f'/{page.slug}/', f'{icon} {page.title}'))
        except:
            pass

        # Add intake forms if they exist
        intake_forms = []
        try:
            for form in IntakeForm.objects.filter(is_active=True).order_by('title'):
                intake_forms.append((f'/intake/{form.slug}/', f'📋 {form.title}'))
        except:
            pass

        # Special menu options
        special_options = [
            ('#', '📂 Dropdown Menu (No Direct Link)'),
        ]

        # Contact options
        contact_options = [
            ('mailto:contact@xfedtax.com', '📧 Email Contact'),
            ('tel:+15551234567', '📞 Phone Contact'),
        ]

        # External links (examples)
        external_options = [
            ('https://www.irs.gov', '🌐 IRS Website'),
            ('https://calendar.google.com', '📅 Schedule Appointment'),
        ]

        # Build organized choices with separators
        if main_pages:
            choices.extend([('', '--- MAIN PAGES ---')] + main_pages)

        if dynamic_pages:
            choices.extend([('', '--- CUSTOM PAGES ---')] + dynamic_pages)

        if intake_forms:
            choices.extend([('', '--- INTAKE FORMS ---')] + intake_forms)

        if special_options:
            choices.extend([('', '--- MENU OPTIONS ---')] + special_options)

        if contact_options:
            choices.extend([('', '--- CONTACT LINKS ---')] + contact_options)

        if external_options:
            choices.extend([('', '--- EXTERNAL LINKS ---')] + external_options)

        return choices

    def url_display(self, obj):
        """Display URL with helpful formatting"""
        if obj.url == '#':
            return format_html('<em style="color: #666;">Dropdown Menu</em>')
        elif obj.url.startswith('mailto:'):
            return format_html('<span style="color: #0066cc;">📧 {}</span>', obj.url)
        elif obj.url.startswith('tel:'):
            return format_html('<span style="color: #0066cc;">📞 {}</span>', obj.url)
        elif obj.url.startswith('http'):
            return format_html('<span style="color: #cc6600;">🌐 {}</span>', obj.url)
        else:
            return format_html('<span style="color: #006600;">🔗 {}</span>', obj.url)
    url_display.short_description = 'Link URL'

    def has_children_indicator(self, obj):
        """Show if this menu item has dropdown children"""
        if obj.has_children:
            return format_html('<span style="color: green; font-weight: bold;">✓ Has Submenu</span>')
        return format_html('<span style="color: gray;">No Submenu</span>')
    has_children_indicator.short_description = 'Submenu Status'

    def get_queryset(self, request):
        """Optimize query to reduce database hits"""
        return super().get_queryset(request).select_related('parent').prefetch_related('children')

    def get_readonly_fields(self, request, obj=None):
        """Make URL readonly when editing existing items to encourage using add form for complex changes"""
        if obj is not None:  # Editing existing item
            return []  # Allow editing URL directly
        return []

    class Media:
        js = ('admin/js/navigation_admin.js',)
        css = {
            'all': ('admin/css/navigation_admin.css',)
        }


class NavigationItemInline(admin.TabularInline):
    """Inline admin for managing child navigation items"""
    model = NavigationItem
    fk_name = 'parent'
    extra = 0
    fields = ('title', 'url', 'order', 'is_active', 'icon_class')
    ordering = ('order',)

    def get_readonly_fields(self, request, obj=None):
        # Make URL readonly in inline to encourage using the main form
        return ('url',) if obj else ()

    class Media:
        css = {
            'all': ('admin/css/navigation_inline.css',)
        }


@admin.register(SocialMediaLink)
class SocialMediaLinkAdmin(admin.ModelAdmin):
    list_display = ('platform', 'url', 'is_active', 'order')
    list_filter = ('platform', 'is_active')
    list_editable = ('order', 'is_active')
    ordering = ('order', 'platform')

    fieldsets = (
        ('Social Media Information', {
            'fields': ('platform', 'url'),
            'description': 'Configure your social media presence'
        }),
        ('Display Options', {
            'fields': ('order', 'is_active'),
            'description': 'Control how this social link appears'
        }),
    )
