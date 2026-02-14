import json
import logging
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import EmailMessage
from django.core.exceptions import ValidationError
from django.conf import settings
from .models import Banner, Feature, Post, PageContent, DynamicPage, IntakeForm, IntakeSubmission, IntakeFile
from .validators import (
    ALLOWED_RESUME_EXTENSIONS_DISPLAY,
    MAX_FILES_PER_SUBMISSION,
    MAX_RESUME_FILE_SIZE_MB,
    RESUME_FILE_ACCEPT_ATTRIBUTE,
    normalize_and_validate_submission_email,
    validate_resume_upload,
)

logger = logging.getLogger(__name__)


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
        'allowed_resume_extensions': ALLOWED_RESUME_EXTENSIONS_DISPLAY,
        'resume_max_file_size_mb': MAX_RESUME_FILE_SIZE_MB,
        'resume_file_accept_attribute': RESUME_FILE_ACCEPT_ATTRIBUTE,
    }

    return render(request, 'intake.html', context)

def handle_intake_submission(request, form):
    """Handle form submission and file uploads"""
    try:
        # Collect form data
        form_data = {}
        email_value = None
        email_field_label = None
        configured_fields = list(form.fields.all())

        # Process non-file fields first.
        for field in configured_fields:
            if field.field_type == 'file':
                continue

            if field.field_type == 'checkbox':
                field_value = 'yes' if request.POST.get(field.field_name) else ''
            else:
                field_value = (request.POST.get(field.field_name) or '').strip()

            if field_value:
                if field.field_type == 'email':
                    try:
                        normalized_email = normalize_and_validate_submission_email(field_value)
                    except ValidationError as exc:
                        messages.error(request, exc.messages[0])
                        return redirect('intake_form', slug=form.slug)
                    email_value = normalized_email
                    email_field_label = field.label
                    form_data[field.label] = normalized_email
                else:
                    form_data[field.label] = field_value
            elif field.is_required:
                messages.error(request, f"{field.label} is required.")
                return redirect('intake_form', slug=form.slug)

        if not email_value:
            messages.error(request, "Email address is required.")
            return redirect('intake_form', slug=form.slug)

        # Prevent duplicate submissions per email per form
        if _submission_exists_for_email(form, email_value, email_field_label):
            messages.error(request, "A submission with this email address has already been received for this form. Please contact us if you need to update your information.")
            return redirect('intake_form', slug=form.slug)

        # Handle file uploads
        uploaded_files = []

        # Handle configured file fields
        for field in [f for f in configured_fields if f.field_type == 'file']:
            files = [uploaded for uploaded in request.FILES.getlist(field.field_name) if uploaded]
            if field.is_required and not files:
                messages.error(request, f"{field.label} is required.")
                return redirect('intake_form', slug=form.slug)
            for uploaded_file in files:
                uploaded_files.append((uploaded_file, field.label))

        # Handle default document uploads if form allows uploads
        if form.allow_file_uploads and 'documents' in request.FILES:
            files = [uploaded for uploaded in request.FILES.getlist('documents') if uploaded]
            for uploaded_file in files:
                uploaded_files.append((uploaded_file, 'Documents'))

        if len(uploaded_files) > MAX_FILES_PER_SUBMISSION:
            messages.error(
                request,
                f"You can upload up to {MAX_FILES_PER_SUBMISSION} files per submission.",
            )
            return redirect('intake_form', slug=form.slug)

        # Enforce resume-safe file types and file size on the server.
        for uploaded_file, _field_label in uploaded_files:
            try:
                validate_resume_upload(uploaded_file)
            except ValidationError as exc:
                messages.error(request, exc.messages[0])
                return redirect('intake_form', slug=form.slug)

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


def _submission_exists_for_email(form, email_value, email_field_label):
    """Check duplicate submissions using an exact, case-insensitive email match."""
    normalized_email = email_value.strip().lower()
    existing_data = IntakeSubmission.objects.filter(form=form).values_list('data', flat=True)
    for data in existing_data:
        if not isinstance(data, dict):
            continue

        existing_email = ''
        if email_field_label:
            existing_email = (data.get(email_field_label) or '').strip().lower()

        if not existing_email:
            existing_email = (
                data.get('Email Address')
                or data.get('email')
                or ''
            ).strip().lower()

        if existing_email == normalized_email:
            return True

    return False

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
    # Prepare shared subject/body for all notification channels.
    subject = f"New {form.title} Submission"
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

    recipients = [email.strip() for email in form.email_recipients.split('\n') if email.strip()]
    if recipients:
        try:
            email = EmailMessage(
                subject=subject,
                body=message_body,
                from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@xfedtax.com'),
                to=recipients,
            )

            # Attach files if any
            for uploaded_file, _field_label in uploaded_files:
                uploaded_file.seek(0)
                email.attach(
                    uploaded_file.name,
                    uploaded_file.read(),
                    uploaded_file.content_type or "application/octet-stream",
                )

            email.send()
        except Exception as exc:
            logger.exception(
                "Error sending intake recipient email for form '%s': %s",
                form.slug,
                str(exc),
            )

    if _should_notify_owners(form):
        try:
            _send_owner_email_alert(subject, message_body)
        except Exception as exc:
            logger.exception(
                "Error sending owner alert email for form '%s': %s",
                form.slug,
                str(exc),
            )

        try:
            _send_owner_slack_alert(form, submission, form_data, uploaded_files)
        except Exception as exc:
            logger.exception(
                "Error sending owner Slack alert for form '%s': %s",
                form.slug,
                str(exc),
            )


def _should_notify_owners(form):
    owner_form_slugs = getattr(settings, 'OWNER_NOTIFICATION_FORM_SLUGS', [])
    if not owner_form_slugs:
        return False
    return (form.slug or '').lower() in {slug.lower() for slug in owner_form_slugs}


def _send_owner_email_alert(subject, message_body):
    owner_emails = getattr(settings, 'OWNER_NOTIFICATION_EMAILS', [])
    recipients = sorted({email.strip() for email in owner_emails if email.strip()})
    if not recipients:
        return

    owner_email = EmailMessage(
        subject=f"[Owner Alert] {subject}",
        body=message_body,
        from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@xfedtax.com'),
        to=recipients,
    )
    owner_email.send()


def _send_owner_slack_alert(form, submission, form_data, uploaded_files):
    if not getattr(settings, 'ENABLE_SLACK_NOTIFICATIONS', False):
        return

    webhook_url = getattr(settings, 'SLACK_WEBHOOK_URL', '').strip()
    if not webhook_url:
        logger.warning("Slack owner notifications skipped because SLACK_WEBHOOK_URL is not set.")
        return

    client_identifier = _extract_client_identifier(form_data)
    file_count = len(uploaded_files)
    mention = (getattr(settings, 'SLACK_NOTIFICATION_MENTION', '') or '').strip()
    intro = f"{mention} " if mention else ""
    message = (
        f"{intro}HireXFed alert: New *{form.title}* submission "
        f"(ID `{submission.id}`) from *{client_identifier}*. Files: *{file_count}*."
    )

    details = []
    for label, value in form_data.items():
        if value:
            details.append(f"• *{label}:* {value}")
    if not details:
        details.append("• No non-file fields captured.")

    if uploaded_files:
        details.append(f"• *Uploaded files:* {file_count}")

    payload = {
        "text": message,
        "mrkdwn": True,
        "blocks": [
            {"type": "section", "text": {"type": "mrkdwn", "text": message}},
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "\n".join(details[:20]),
                },
            },
        ],
    }
    _post_slack_webhook(webhook_url, payload)


def _extract_client_identifier(form_data):
    preferred_keys = (
        'Email Address',
        'email',
        'First Name',
    )
    for key in preferred_keys:
        value = (form_data.get(key) or '').strip()
        if value:
            return value
    return "unknown sender"


def _post_slack_webhook(webhook_url, payload):
    request = Request(
        webhook_url,
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
    )
    request.add_header("Content-Type", "application/json")
    try:
        with urlopen(request, timeout=10):
            return
    except (HTTPError, URLError) as exc:
        logger.exception("Failed to send Slack notification: %s", str(exc))


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
