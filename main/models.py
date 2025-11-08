from django.db import models

class Banner(models.Model):
    heading = models.CharField(
        max_length=200,
        default="XFED Tax Solutions",
        verbose_name="Main Headline",
        help_text="The large heading text that appears at the top of the homepage banner"
    )
    subheading = models.CharField(
        max_length=200,
        default="Former Feds Making The System Work For You!",
        verbose_name="Tagline",
        help_text="The smaller text that appears directly under the main headline"
    )
    description1 = models.TextField(
        default="XFED Tax Solutions is committed to providing efficient and effective tax and tax related services to America's taxpayer population.",
        verbose_name="First Description Paragraph",
        help_text="The first paragraph of text in the banner section"
    )
    description2 = models.TextField(
        default="Whether you are an individual or business or both, America's largest network of former IRS tax professionals can provide the services you need.",
        verbose_name="Second Description Paragraph",
        help_text="The second paragraph of text in the banner section"
    )
    description3 = models.TextField(
        default="For specific information about how we can help you, please fill out our <a href='#'>brief questionnaire</a> or call us at [Justin's Personal Cell Phone Number].",
        verbose_name="Third Description Paragraph",
        help_text="The third paragraph of text in the banner section. You can include HTML links like <a href='#'>link text</a>"
    )
    button_text = models.CharField(
        max_length=100,
        default="Learn More",
        verbose_name="Button Text",
        help_text="The text that appears on the button in the banner"
    )
    button_link = models.CharField(
        max_length=200,
        blank=True,
        default="/",
        verbose_name="Button Link URL",
        help_text="Where the button should link to (e.g., '/contact/' or 'https://example.com')"
    )
    image = models.ImageField(
        upload_to='banner/',
        blank=True,
        null=True,
        verbose_name="Banner Image",
        help_text="The image that appears on the right side of the banner (optional)"
    )

    def __str__(self):
        return self.heading

class Feature(models.Model):
    ICON_CHOICES = [
        ('fa-gem', 'Gem'),
        ('fa-paper-plane', 'Paper Plane'),
        ('fa-rocket', 'Rocket'),
        ('fa-signal', 'Signal'),
    ]
    icon = models.CharField(
        max_length=50,
        choices=ICON_CHOICES,
        default='fa-gem',
        verbose_name="Feature Icon",
        help_text="Choose an icon that represents this feature"
    )
    title = models.CharField(
        max_length=100,
        default="Enter text here",
        verbose_name="Feature Title",
        help_text="Short title for this feature (appears in the 'More About Us' section)"
    )
    description = models.TextField(
        default="Enter text here",
        verbose_name="Feature Description",
        help_text="Brief description explaining this feature or service"
    )

    def __str__(self):
        return self.title

class Post(models.Model):
    image = models.ImageField(
        upload_to='posts/',
        blank=True,
        null=True,
        verbose_name="Article Image",
        help_text="Image that appears with this article (appears in the 'Ipsum sed dolor' section)"
    )
    title = models.CharField(
        max_length=100,
        verbose_name="Article Title",
        help_text="Title of the article or blog post"
    )
    description = models.TextField(
        verbose_name="Article Description",
        help_text="Brief description or excerpt of the article"
    )
    button_text = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Read More Button Text",
        help_text="Text for the button (e.g., 'Read More', 'Learn More')"
    )
    button_link = models.URLField(
        blank=True,
        verbose_name="Article Link",
        help_text="URL where this article can be read in full"
    )

    def __str__(self):
        return self.title

class MiniPost(models.Model):
    image = models.ImageField(
        upload_to='miniposts/',
        blank=True,
        null=True,
        verbose_name="Sidebar Post Image",
        help_text="Small image that appears in the sidebar mini-posts section"
    )
    description = models.TextField(
        verbose_name="Sidebar Post Text",
        help_text="Brief text content for this sidebar post"
    )

    class Meta:
        verbose_name = "Sidebar Mini Post"
        verbose_name_plural = "Sidebar Mini Posts"

    def __str__(self):
        return self.description[:30]

class ContactInfo(models.Model):
    email = models.EmailField(
        verbose_name="Contact Email Address",
        help_text="Email address displayed in the 'Get in touch' section"
    )
    phone = models.CharField(
        max_length=50,
        verbose_name="Contact Phone Number",
        help_text="Phone number displayed in the contact section (e.g., '(555) 123-4567')"
    )
    address = models.TextField(
        verbose_name="Business Address",
        help_text="Full business address displayed in the contact section"
    )

    class Meta:
        verbose_name = "Contact Information"
        verbose_name_plural = "Contact Information"

    def __str__(self):
        return self.email

class Footer(models.Model):
    copyright = models.CharField(
        max_length=200,
        verbose_name="Copyright Text",
        help_text="Copyright notice that appears at the bottom of every page"
    )
    demo_images_link = models.URLField(
        blank=True,
        verbose_name="Demo Images Credit Link",
        help_text="Optional link to credit demo images (leave blank if not needed)"
    )
    design_link = models.URLField(
        blank=True,
        verbose_name="Design Credit Link",
        help_text="Optional link to credit website design (leave blank if not needed)"
    )

    class Meta:
        verbose_name = "Footer Information"
        verbose_name_plural = "Footer Information"

    def __str__(self):
        return self.copyright

# Extensible Page Content Management
class PageContent(models.Model):
    """Base model for managing different page sections"""
    SECTION_TYPE_CHOICES = [
        ('header', 'Page Header'),
        ('main_content', 'Main Content Section'),
        ('sidebar', 'Sidebar Content'),
        ('footer', 'Footer Content'),
        ('banner', 'Banner Section'),
        ('features', 'Features Section'),
        ('posts', 'Posts Section'),
    ]

    page = models.CharField(
        max_length=100,
        verbose_name="Page",
        help_text="Which page this content appears on (use page slug for dynamic pages, or 'homepage'/'generic'/'elements' for default pages)"
    )
    section_type = models.CharField(
        max_length=50,
        choices=SECTION_TYPE_CHOICES,
        verbose_name="Section Type",
        help_text="What type of section this content represents"
    )
    title = models.CharField(
        max_length=200,
        verbose_name="Section Title",
        help_text="The main heading for this section"
    )
    content = models.TextField(
        verbose_name="Section Content",
        help_text="The main text content for this section (HTML allowed)"
    )
    image = models.ImageField(
        upload_to='page_content/',
        blank=True,
        null=True,
        verbose_name="Section Image",
        help_text="Optional image for this section"
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Display Order",
        help_text="Order in which this section appears (0 = first, 1 = second, etc.)"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Show on Website",
        help_text="Uncheck to hide this section from the website"
    )

    class Meta:
        ordering = ['page', 'section_type', 'order']
        verbose_name = "Page Section"
        verbose_name_plural = "Page Sections"

    def __str__(self):
        return f"{self.get_page_name()} - {self.title}"

    def get_page_name(self):
        """Get a friendly name for the page"""
        # Return the page slug with title case
        return self.page.replace('_', ' ').replace('-', ' ').title()

# Intake Form Management System
class IntakeForm(models.Model):
    """Model for creating custom intake forms"""
    title = models.CharField(
        max_length=200,
        verbose_name="Form Title",
        help_text="The title that appears at the top of the form"
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name="Form URL",
        help_text="The URL path for this form (e.g., 'client-intake' creates /intake/client-intake/)"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Form Description",
        help_text="Optional description that appears below the title"
    )
    success_message = models.TextField(
        default="Thank you for your submission! We will contact you soon.",
        verbose_name="Success Message",
        help_text="Message shown after successful form submission"
    )
    email_recipients = models.TextField(
        verbose_name="Email Recipients",
        help_text="Email addresses to send form submissions to (one per line)"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Form Active",
        help_text="Uncheck to disable this form"
    )
    allow_file_uploads = models.BooleanField(
        default=True,
        verbose_name="Allow File Uploads",
        help_text="Allow users to upload documents with their submission"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']
        verbose_name = "Intake Form"
        verbose_name_plural = "Intake Forms"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/intake/{self.slug}/"

class IntakeField(models.Model):
    """Model for configurable form fields"""
    FIELD_TYPE_CHOICES = [
        ('text', 'Text Input'),
        ('email', 'Email Input'),
        ('phone', 'Phone Number'),
        ('textarea', 'Text Area (Multi-line)'),
        ('select', 'Dropdown Select'),
        ('checkbox', 'Checkbox'),
        ('radio', 'Radio Button Group'),
        ('file', 'File Upload'),
    ]

    form = models.ForeignKey(
        IntakeForm,
        on_delete=models.CASCADE,
        related_name='fields',
        verbose_name="Intake Form"
    )
    label = models.CharField(
        max_length=100,
        verbose_name="Field Label",
        help_text="The label that appears above the field"
    )
    field_name = models.CharField(
        max_length=50,
        verbose_name="Field Name",
        help_text="Internal name for the field (letters, numbers, underscores only)"
    )
    field_type = models.CharField(
        max_length=20,
        choices=FIELD_TYPE_CHOICES,
        verbose_name="Field Type",
        help_text="What type of input field this is"
    )
    placeholder = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Placeholder Text",
        help_text="Optional placeholder text inside the field"
    )
    choices = models.TextField(
        blank=True,
        verbose_name="Choices (for select/radio)",
        help_text="For dropdown or radio fields, enter choices (one per line)"
    )
    is_required = models.BooleanField(
        default=False,
        verbose_name="Required Field",
        help_text="Check if this field must be filled out"
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Display Order",
        help_text="Order in which this field appears (0 = first, 1 = second, etc.)"
    )
    help_text = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Help Text",
        help_text="Optional help text that appears below the field"
    )

    class Meta:
        ordering = ['form', 'order']
        verbose_name = "Form Field"
        verbose_name_plural = "Form Fields"
        unique_together = ['form', 'field_name']

    def __str__(self):
        return f"{self.form.title} - {self.label}"

    def get_choices_list(self):
        """Convert choices text into a list"""
        if self.choices:
            return [choice.strip() for choice in self.choices.split('\n') if choice.strip()]
        return []

class IntakeSubmission(models.Model):
    """Model to store form submissions"""
    STATUS_CHOICES = [
        ('new', 'New - Needs Review'),
        ('reviewed', 'Reviewed - Needs Response'),
        ('contacted', 'Client Contacted'),
        ('scheduled', 'Meeting Scheduled'),
        ('completed', 'Process Completed'),
        ('declined', 'Declined/Not Proceeding'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low Priority'),
        ('normal', 'Normal Priority'),
        ('high', 'High Priority'),
        ('urgent', 'Urgent'),
    ]

    form = models.ForeignKey(
        IntakeForm,
        on_delete=models.CASCADE,
        related_name='submissions',
        verbose_name="Intake Form"
    )
    submitted_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(
        blank=True,
        null=True,
        verbose_name="IP Address"
    )
    data = models.JSONField(
        verbose_name="Submission Data",
        help_text="Form field data submitted by the user"
    )

    # Status and tracking fields
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name="Status",
        help_text="Current status of this submission"
    )
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='normal',
        verbose_name="Priority Level",
        help_text="Priority level for follow-up"
    )
    assigned_to = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Assigned To",
        help_text="Staff member responsible for this submission"
    )

    # Response tracking
    first_contacted_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="First Contact Date",
        help_text="When we first contacted the client"
    )
    last_contact_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Last Contact Date",
        help_text="Most recent contact with client"
    )
    next_followup_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Next Follow-up Date",
        help_text="When to follow up with this client"
    )

    # Admin notes
    admin_notes = models.TextField(
        blank=True,
        verbose_name="Internal Notes",
        help_text="Internal notes about this submission (not visible to client)"
    )

    # Timestamps for tracking
    status_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = "Form Submission"
        verbose_name_plural = "Form Submissions"

    def __str__(self):
        client_name = self.get_client_name()
        return f"{client_name} - {self.form.title} ({self.get_status_display()})"

    def get_client_name(self):
        """Extract client name from submission data"""
        data = self.data
        first_name = data.get('First Name', data.get('first_name', ''))
        last_name = data.get('Last Name', data.get('last_name', ''))
        email = data.get('Email Address', data.get('email', ''))

        if first_name and last_name:
            return f"{first_name} {last_name}"
        elif email:
            return email
        else:
            return f"Submission #{self.id}"

    def get_contact_info(self):
        """Extract contact information from submission data"""
        data = self.data
        return {
            'email': data.get('Email Address', data.get('email', '')),
            'phone': data.get('Phone Number', data.get('phone', '')),
        }

    def days_since_submission(self):
        """Calculate days since submission"""
        from django.utils import timezone
        return (timezone.now() - self.submitted_at).days

    def needs_followup(self):
        """Check if submission needs follow-up"""
        from django.utils import timezone
        if self.next_followup_date and self.next_followup_date <= timezone.now().date():
            return True
        if self.status == 'new' and self.days_since_submission() >= 1:
            return True
        return False

class IntakeFile(models.Model):
    """Model to store uploaded files from intake forms"""
    submission = models.ForeignKey(
        IntakeSubmission,
        on_delete=models.CASCADE,
        related_name='files',
        verbose_name="Form Submission"
    )
    file = models.FileField(
        upload_to='intake_uploads/%Y/%m/',
        verbose_name="Uploaded File"
    )
    original_filename = models.CharField(
        max_length=255,
        verbose_name="Original Filename"
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = "Uploaded File"
        verbose_name_plural = "Uploaded Files"

    def __str__(self):
        return f"{self.original_filename} - {self.submission}"

# Keep existing GenericPageSection for backward compatibility
class GenericPageSection(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="Section Title",
        help_text="The main heading for this page section"
    )
    content = models.TextField(
        verbose_name="Section Content",
        help_text="The main text content for this section (HTML formatting allowed)"
    )
    image = models.ImageField(
        upload_to='generic/',
        blank=True,
        null=True,
        verbose_name="Section Image",
        help_text="Optional image for this section"
    )

    class Meta:
        verbose_name = "Generic Page Section"
        verbose_name_plural = "Generic Page Sections"

    def __str__(self):
        return self.title

# Dynamic Page Management System
class DynamicPage(models.Model):
    """Model for creating custom pages with different templates"""
    TEMPLATE_CHOICES = [
        ('generic', 'Generic Template (Simple content layout)'),
        ('elements', 'Elements Template (Feature-rich with forms, tables, etc.)'),
        ('index', 'Homepage Template (Banner + features + posts layout)'),
        ('intake', 'Intake Form Template (Custom intake forms)'),
    ]

    title = models.CharField(
        max_length=200,
        verbose_name="Page Title",
        help_text="The title that appears in the browser tab and page header"
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name="Page URL",
        help_text="The URL path for this page (e.g., 'about-us' creates /about-us/). Only letters, numbers, and hyphens allowed."
    )
    template_type = models.CharField(
        max_length=50,
        choices=TEMPLATE_CHOICES,
        default='generic',
        verbose_name="Page Template",
        help_text="Choose the layout style for this page"
    )
    meta_description = models.TextField(
        max_length=160,
        blank=True,
        verbose_name="SEO Description",
        help_text="Brief description for search engines (160 characters max)"
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name="Publish Page",
        help_text="Uncheck to hide this page from the website"
    )
    show_in_navigation = models.BooleanField(
        default=False,
        verbose_name="Show in Main Navigation",
        help_text="Check to automatically add this page to the main navigation menu"
    )
    navigation_order = models.PositiveIntegerField(
        default=0,
        verbose_name="Navigation Order",
        help_text="Order in navigation menu (lower numbers appear first)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['navigation_order', 'title']
        verbose_name = "Custom Page"
        verbose_name_plural = "Custom Pages"

    def __str__(self):
        return f"{self.title} ({self.get_template_type_display()})"

    def get_absolute_url(self):
        return f"/{self.slug}/"

    def get_page_content(self):
        """Get all content sections for this page"""
        return PageContent.objects.filter(
            page=self.slug,
            is_active=True
        ).order_by('section_type', 'order')


class NavigationItem(models.Model):
    """Navigation menu items that appear in the sidebar"""
    title = models.CharField(
        max_length=100,
        verbose_name="Menu Title",
        help_text="The text that will appear in the navigation menu"
    )
    url = models.CharField(
        max_length=200,
        verbose_name="Link URL",
        help_text="Where this menu item links to (e.g., '/contact/', 'https://example.com', or '#' for dropdowns)"
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='children',
        verbose_name="Parent Menu Item",
        help_text="Leave blank for top-level menu items. Select a parent to create dropdown submenu items."
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Display Order",
        help_text="Lower numbers appear first. Use 10, 20, 30... to leave room for reordering."
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Active",
        help_text="Uncheck to temporarily hide this menu item"
    )
    icon_class = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Icon Class (Optional)",
        help_text="Font Awesome icon class (e.g., 'fa-home', 'fa-envelope')"
    )
    opens_new_window = models.BooleanField(
        default=False,
        verbose_name="Open in New Window",
        help_text="Check if this link should open in a new tab/window"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'title']
        verbose_name = "Navigation Item"
        verbose_name_plural = "Navigation Items"

    def __str__(self):
        if self.parent:
            return f"{self.parent.title} → {self.title}"
        return self.title

    @property
    def has_children(self):
        """Check if this item has dropdown children"""
        return self.children.filter(is_active=True).exists()

    def get_children(self):
        """Get active child menu items ordered by display order"""
        return self.children.filter(is_active=True).order_by('order')


class SocialMediaLink(models.Model):
    """Social media links for the header"""
    PLATFORM_CHOICES = [
        ('twitter', 'Twitter'),
        ('facebook-f', 'Facebook'),
        ('instagram', 'Instagram'),
        ('linkedin-in', 'LinkedIn'),
        ('youtube', 'YouTube'),
        ('snapchat-ghost', 'Snapchat'),
        ('medium-m', 'Medium'),
        ('github', 'GitHub'),
        ('envelope', 'Email'),
    ]

    platform = models.CharField(
        max_length=20,
        choices=PLATFORM_CHOICES,
        verbose_name="Social Platform",
        help_text="Choose the social media platform"
    )
    url = models.URLField(
        verbose_name="Profile URL",
        help_text="Full URL to your social media profile"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Active",
        help_text="Uncheck to temporarily hide this social link"
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Display Order",
        help_text="Lower numbers appear first"
    )

    class Meta:
        ordering = ['order', 'platform']
        verbose_name = "Social Media Link"
        verbose_name_plural = "Social Media Links"

    def __str__(self):
        return f"{self.get_platform_display()} - {self.url}"

    def get_icon_class(self):
        """Get the Font Awesome icon class for this platform"""
        return f"fa-{self.platform}"
