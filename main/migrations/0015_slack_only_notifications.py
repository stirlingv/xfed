# Remove email notification plumbing (Google Workspace account retired) and
# seed the public contact form that replaces mailto: links site-wide.
from django.db import migrations, models


CONTACT_FORM_SLUG = 'contact-us'

CONTACT_FORM_DEFAULTS = {
    'title': 'Contact Us',
    'description': (
        'Have a question or need help? Send us a message and our team will '
        'get back to you within one business day.'
    ),
    'success_message': (
        'Thank you for reaching out! Your message has been delivered to our '
        'team and we will get back to you within one business day.'
    ),
    'is_active': True,
    'allow_file_uploads': False,
}

CONTACT_FORM_FIELDS = [
    {
        'label': 'Full Name',
        'field_name': 'full_name',
        'field_type': 'text',
        'placeholder': 'John Smith',
        'is_required': True,
        'order': 1,
    },
    {
        'label': 'Email Address',
        'field_name': 'email',
        'field_type': 'email',
        'placeholder': 'john@example.com',
        'is_required': True,
        'order': 2,
        'help_text': 'We will reply to this address.',
    },
    {
        'label': 'Subject',
        'field_name': 'subject',
        'field_type': 'select',
        'choices': (
            'General Question\n'
            'Tax Services\n'
            'Joining the Network\n'
            'Billing or Payments\n'
            'Website Feedback\n'
            'Other'
        ),
        'is_required': True,
        'order': 3,
    },
    {
        'label': 'Message',
        'field_name': 'message',
        'field_type': 'textarea',
        'placeholder': 'How can we help you?',
        'is_required': True,
        'order': 4,
    },
]


def create_contact_form(apps, schema_editor):
    IntakeForm = apps.get_model('main', 'IntakeForm')
    IntakeField = apps.get_model('main', 'IntakeField')

    form, _created = IntakeForm.objects.get_or_create(
        slug=CONTACT_FORM_SLUG,
        defaults=CONTACT_FORM_DEFAULTS,
    )

    for field_data in CONTACT_FORM_FIELDS:
        field_defaults = field_data.copy()
        field_name = field_defaults.pop('field_name')
        IntakeField.objects.get_or_create(
            form=form,
            field_name=field_name,
            defaults=field_defaults,
        )


def remove_contact_form(apps, schema_editor):
    IntakeForm = apps.get_model('main', 'IntakeForm')
    IntakeForm.objects.filter(slug=CONTACT_FORM_SLUG).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_intakefile_upload_path_routing'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='intakeform',
            name='email_recipients',
        ),
        migrations.AlterField(
            model_name='contactinfo',
            name='email',
            field=models.EmailField(
                blank=True,
                help_text=(
                    'Optional. Leave blank while inbound email is unmonitored — '
                    'the site links to the contact form instead.'
                ),
                max_length=254,
                verbose_name='Contact Email Address',
            ),
        ),
        migrations.RunPython(create_contact_form, remove_contact_form),
    ]
