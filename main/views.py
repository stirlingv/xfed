from django.shortcuts import render, get_object_or_404, redirect
from django.templatetags.static import static
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
import json
from .models import Banner, Feature, Post, PageContent, DynamicPage, IntakeForm, IntakeSubmission, IntakeFile

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
            description3="For specific information about how we can help you, please <a href='/intake/client-consultation/'>request a consultation</a> and one of our experts will contact you within 24 hours.",
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

def dynamic_page_view(request, slug):
    """View for handling dynamically created pages"""
    page = get_object_or_404(DynamicPage, slug=slug, is_published=True)

    # Get page content sections
    page_sections = PageContent.objects.filter(
        page=page.slug,
        is_active=True
    ).order_by('section_type', 'order')

    # Most dynamic pages should use dynamic_page.html which properly renders page_sections
    # Only use special templates for specific page types that need them
    template_map = {
        'index': 'index.html',
        'intake': 'intake.html',
    }

    # Default to dynamic_page.html for generic and other page types
    template_name = template_map.get(page.template_type, 'dynamic_page.html')

    context = {
        'page': page,
        'page_sections': page_sections,
        'meta_description': page.meta_description,
    }

    # For index template type, we need to include special context
    if page.template_type == 'index':
        # Get banner content (only one should exist)
        banner = Banner.objects.first()
        features = Feature.objects.all()
        posts = Post.objects.all()[:6]

        context.update({
            'banner': banner,
            'features': features,
            'posts': posts,
        })

    return render(request, template_name, context)

def intake_form_view(request, slug):
    """View for handling intake forms"""
    form = get_object_or_404(IntakeForm, slug=slug, is_active=True)

    if request.method == 'POST':
        return handle_intake_submission(request, form)

    # Get form fields ordered by display order
    form_fields = form.fields.all().order_by('order')

    # Check if there are any file fields configured
    has_file_fields = form_fields.filter(field_type='file').exists()

    context = {
        'form': form,
        'form_fields': form_fields,
        'has_file_fields': has_file_fields,
    }

    return render(request, 'intake.html', context)

def handle_intake_submission(request, form):
    """Handle form submission and file uploads"""
    try:
        # Collect form data
        form_data = {}
        files_uploaded = []


        # Process configured form fields and collect email for validation
        email_value = None
        email_field_name = None
        for field in form.fields.all():
            field_value = request.POST.get(field.field_name)
            if field.field_type == 'email':
                email_value = field_value
                email_field_name = field.field_name
            if field_value:
                form_data[field.label] = field_value
            elif field.is_required:
                messages.error(request, f"{field.label} is required.")
                return redirect('intake_form', slug=form.slug)

        # Email format validation
        from django.core.validators import validate_email
        from django.core.exceptions import ValidationError
        if email_value:
            try:
                validate_email(email_value)
            except ValidationError:
                messages.error(request, "Please enter a valid email address.")
                return redirect('intake_form', slug=form.slug)
        else:
            messages.error(request, "Email address is required.")
            return redirect('intake_form', slug=form.slug)

        # Prevent duplicate submissions per email per form
        # IntakeSubmission stores data as JSON, so we need to search for submissions with the same form and email
        from django.db.models import Q
        duplicate = IntakeSubmission.objects.filter(
            form=form,
            data__icontains=email_value
        ).exists()
        if duplicate:
            messages.error(request, "A submission with this email address has already been received for this form. Please contact us if you need to update your information.")
            return redirect('intake_form', slug=form.slug)

        # Handle file uploads
        uploaded_files = []

        # Handle configured file fields
        for field in form.fields.filter(field_type='file'):
            files = request.FILES.getlist(field.field_name)
            for uploaded_file in files:
                uploaded_files.append((uploaded_file, field.label))

        # Handle default document uploads if form allows uploads
        if form.allow_file_uploads and 'documents' in request.FILES:
            files = request.FILES.getlist('documents')
            for uploaded_file in files:
                uploaded_files.append((uploaded_file, 'Documents'))

        # Create submission record
        submission = IntakeSubmission.objects.create(
            form=form,
            data=form_data,
            ip_address=get_client_ip(request)
        )

        # Save uploaded files
        for uploaded_file, field_label in uploaded_files:
            IntakeFile.objects.create(
                submission=submission,
                file=uploaded_file,
                original_filename=uploaded_file.name
            )

        # Send email notification
        send_intake_notification(form, submission, form_data, uploaded_files)

        # Show confirmation page after successful submission
        return render(request, 'intake_confirmation.html', { 'form': form })

    except Exception as e:
        messages.error(request, f"There was an error processing your submission: {str(e)}")
        return redirect('intake_form', slug=form.slug)

def get_client_ip(request):
    """Get the client's IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def send_intake_notification(form, submission, form_data, uploaded_files):
    """Send email notification for new intake submission"""
    try:
        # Prepare email content
        subject = f"New {form.title} Submission"

        # Build message body
        message_lines = [
            f"New submission received for: {form.title}",
            f"Submitted at: {submission.submitted_at.strftime('%Y-%m-%d %H:%M:%S')}",
            f"IP Address: {submission.ip_address}",
            "",
            "Form Data:",
            "-" * 40,
        ]

        for field_label, value in form_data.items():
            message_lines.append(f"{field_label}: {value}")

        if uploaded_files:
            message_lines.extend([
                "",
                f"Files Uploaded: {len(uploaded_files)}",
                "-" * 40,
            ])
            for uploaded_file, field_label in uploaded_files:
                message_lines.append(f"- {uploaded_file.name} ({field_label})")

        message_body = "\n".join(message_lines)

        # Get email recipients
        recipients = [email.strip() for email in form.email_recipients.split('\n') if email.strip()]

        if recipients:
            email = EmailMessage(
                subject=subject,
                body=message_body,
                from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@xfedtax.com'),
                to=recipients,
            )

            # Attach files if any
            for uploaded_file, field_label in uploaded_files:
                email.attach(uploaded_file.name, uploaded_file.read(), uploaded_file.content_type)

            email.send()

    except Exception as e:
        print(f"Error sending intake notification email: {str(e)}")


# Admin helper views
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.text import slugify


@staff_member_required
def add_page_popup(request):
    """Popup view for creating new pages from navigation admin"""
    if request.method == 'GET':
        # Show the page creation form
        template_choices = [
            ('generic', 'Generic Page', 'Simple content page - good for About, Contact, etc.'),
            ('elements', 'Elements Page', 'Feature-rich page with forms and interactive elements'),
            ('index', 'Homepage Style', 'Banner + features layout (advanced)'),
        ]

        context = {
            'template_choices': template_choices,
        }
        return render(request, 'admin/add_page_popup.html', context)

    elif request.method == 'POST':
        # Handle page creation
        try:
            title = request.POST.get('title', '').strip()
            template_type = request.POST.get('template_type', 'generic')
            content = request.POST.get('content', '').strip()
            meta_description = request.POST.get('meta_description', '').strip()

            if not title:
                return JsonResponse({
                    'success': False,
                    'error': 'Page title is required'
                })

            # Generate slug from title
            slug = slugify(title)
            if not slug:
                return JsonResponse({
                    'success': False,
                    'error': 'Could not generate URL from title. Please use letters and numbers.'
                })

            # Check if slug already exists
            if DynamicPage.objects.filter(slug=slug).exists():
                return JsonResponse({
                    'success': False,
                    'error': f'A page with URL "/{slug}/" already exists. Please choose a different title.'
                })

            # Create the page
            page = DynamicPage.objects.create(
                title=title,
                slug=slug,
                template_type=template_type,
                meta_description=meta_description or f'{title} - XFED Tax Solutions',
                is_published=True,
                show_in_navigation=True,
                navigation_order=(DynamicPage.objects.count() + 1) * 10,
            )

            # Create initial content if provided
            if content:
                PageContent.objects.create(
                    page=page.slug,
                    section_type='main_content',
                    title=f'{title} Content',
                    content=content,
                    order=1,
                    is_active=True
                )

            # Return success with page URL
            return JsonResponse({
                'success': True,
                'page_url': f'/{page.slug}/',
                'page_title': page.title,
                'message': f'Page "{page.title}" created successfully!'
            })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Error creating page: {str(e)}'
            })

    return JsonResponse({'success': False, 'error': 'Invalid request method'})


def add_page_popup(request):
    """Admin popup for creating new pages from navigation admin"""
    from django.contrib.admin.views.decorators import staff_member_required
    from django.http import JsonResponse
    from django.template.response import TemplateResponse

    @staff_member_required
    def _add_page_popup_view(request):
        if request.method == 'GET':
            # Show the popup form
            template_choices = DynamicPage._meta.get_field('template_type').choices
            return TemplateResponse(request, 'admin/add_page_popup.html', {
                'template_choices': template_choices,
            })

        elif request.method == 'POST':
            # Handle form submission
            try:
                title = request.POST.get('title', '').strip()
                slug = request.POST.get('slug', '').strip()
                template_type = request.POST.get('template_type', 'generic')
                meta_description = request.POST.get('meta_description', '').strip()

                if not title:
                    return JsonResponse({
                        'success': False,
                        'error': 'Page title is required'
                    })

                if not slug:
                    # Auto-generate slug from title
                    from django.utils.text import slugify
                    slug = slugify(title)

                # Check if slug already exists
                if DynamicPage.objects.filter(slug=slug).exists():
                    return JsonResponse({
                        'success': False,
                        'error': f'A page with URL "/{slug}/" already exists. Please choose a different title or slug.'
                    })

                # Create the page
                page = DynamicPage.objects.create(
                    title=title,
                    slug=slug,
                    template_type=template_type,
                    meta_description=meta_description,
                    is_published=True,
                    show_in_navigation=True,
                    navigation_order=100  # Add to end of navigation
                )

                # Create initial page content
                PageContent.objects.create(
                    page=page.slug,
                    section_type='main_content',
                    title=f'{page.title} Content',
                    content=f'<h2>Welcome to {page.title}</h2>\n<p>This page was created from the navigation admin. You can edit this content through the admin interface.</p>',
                    order=1,
                    is_active=True
                )

                return JsonResponse({
                    'success': True,
                    'page_url': f'/{page.slug}/',
                    'page_title': page.title,
                    'message': f'Page "{page.title}" created successfully!'
                })

            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'error': f'Error creating page: {str(e)}'
                })

        return JsonResponse({'success': False, 'error': 'Invalid request method'})

    return _add_page_popup_view(request)
