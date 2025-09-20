from django.db import models

class Banner(models.Model):
    heading = models.CharField(max_length=200)
    subheading = models.CharField(max_length=200, blank=True)
    paragraph = models.TextField(blank=True)
    image = models.ImageField(upload_to='banner/', blank=True, null=True)
    button_text = models.CharField(max_length=100, blank=True)
    button_link = models.URLField(blank=True)

    def __str__(self):
        return self.heading

class Feature(models.Model):
    ICON_CHOICES = [
        ('fa-gem', 'Gem'),
        ('fa-paper-plane', 'Paper Plane'),
        ('fa-rocket', 'Rocket'),
        ('fa-signal', 'Signal'),
    ]
    icon = models.CharField(max_length=50, choices=ICON_CHOICES)
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title

class Post(models.Model):
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    button_text = models.CharField(max_length=100, blank=True)
    button_link = models.URLField(blank=True)

    def __str__(self):
        return self.title

class MiniPost(models.Model):
    image = models.ImageField(upload_to='miniposts/', blank=True, null=True)
    description = models.TextField()

    def __str__(self):
        return self.description[:30]

class ContactInfo(models.Model):
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    address = models.TextField()

    def __str__(self):
        return self.email

class Footer(models.Model):
    copyright = models.CharField(max_length=200)
    demo_images_link = models.URLField(blank=True)
    design_link = models.URLField(blank=True)

    def __str__(self):
        return self.copyright

class GenericPageSection(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='generic/', blank=True, null=True)

    def __str__(self):
        return self.title