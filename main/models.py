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
    PAGE_CHOICES = [
        ('homepage', 'Homepage'),
        ('generic', 'Generic Page'),
        ('elements', 'Elements Page'),
    ]
    
    SECTION_TYPE_CHOICES = [
        ('header', 'Page Header'),
        ('main_content', 'Main Content Section'),
        ('sidebar', 'Sidebar Content'),
        ('footer', 'Footer Content'),
    ]
    
    page = models.CharField(
        max_length=50, 
        choices=PAGE_CHOICES,
        verbose_name="Page",
        help_text="Which page this content appears on"
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
        return f"{self.get_page_display()} - {self.title}"

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

# New model for managing navigation/menu items
class NavigationItem(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name="Menu Item Text",
        help_text="Text that appears in the navigation menu"
    )
    url = models.CharField(
        max_length=200,
        verbose_name="Link URL",
        help_text="Where this menu item links to (e.g., '/contact/' or 'https://example.com')"
    )
    parent = models.ForeignKey(
        'self', 
        null=True, 
        blank=True, 
        on_delete=models.CASCADE,
        verbose_name="Parent Menu Item",
        help_text="Leave blank for top-level menu items"
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Display Order",
        help_text="Order in which this item appears in the menu"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Show in Menu",
        help_text="Uncheck to hide this menu item"
    )
    
    class Meta:
        ordering = ['order']
        verbose_name = "Navigation Menu Item"
        verbose_name_plural = "Navigation Menu Items"
    
    def __str__(self):
        if self.parent:
            return f"{self.parent.title} > {self.title}"
        return self.title

# Model for managing social media links
class SocialMediaLink(models.Model):
    PLATFORM_CHOICES = [
        ('twitter', 'Twitter'),
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('linkedin', 'LinkedIn'),
        ('youtube', 'YouTube'),
        ('snapchat', 'Snapchat'),
        ('medium', 'Medium'),
    ]
    
    platform = models.CharField(
        max_length=50, 
        choices=PLATFORM_CHOICES,
        verbose_name="Social Media Platform"
    )
    url = models.URLField(
        verbose_name="Profile URL",
        help_text="Full URL to your social media profile"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Show on Website"
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Display Order"
    )
    
    class Meta:
        ordering = ['order']
        verbose_name = "Social Media Link"
        verbose_name_plural = "Social Media Links"
    
    def __str__(self):
        return f"{self.get_platform_display()}"