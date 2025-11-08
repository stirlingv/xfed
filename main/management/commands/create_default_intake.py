from django.core.management.base import BaseCommand
from main.models import IntakeForm, IntakeField

class Command(BaseCommand):
    help = 'Create a default client intake form'

    def handle(self, *args, **options):
        # Create the main intake form
        intake_form, created = IntakeForm.objects.get_or_create(
            slug='client-intake',
            defaults={
                'title': 'Client Intake Form',
                'description': 'Please fill out this form to help us understand your needs and provide the best possible service.',
                'success_message': 'Thank you for your submission! We will review your information and contact you within 24 hours.',
                'email_recipients': 'admin@xfedtax.com\ninfo@xfedtax.com',
                'is_active': True,
                'allow_file_uploads': True,
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS('Created Client Intake Form'))

            # Create default fields
            fields_to_create = [
                {
                    'label': 'First Name',
                    'field_name': 'first_name',
                    'field_type': 'text',
                    'placeholder': 'Enter your first name',
                    'is_required': True,
                    'order': 1,
                },
                {
                    'label': 'Last Name',
                    'field_name': 'last_name',
                    'field_type': 'text',
                    'placeholder': 'Enter your last name',
                    'is_required': True,
                    'order': 2,
                },
                {
                    'label': 'Email Address',
                    'field_name': 'email',
                    'field_type': 'email',
                    'placeholder': 'your.email@example.com',
                    'is_required': True,
                    'order': 3,
                },
                {
                    'label': 'Phone Number',
                    'field_name': 'phone',
                    'field_type': 'phone',
                    'placeholder': '(555) 123-4567',
                    'is_required': True,
                    'order': 4,
                },
                {
                    'label': 'Service Needed',
                    'field_name': 'service_needed',
                    'field_type': 'select',
                    'choices': 'Individual Tax Preparation\nBusiness Tax Services\nTax Planning\nFinancial Consulting\nBookkeeping Services\nOther',
                    'is_required': True,
                    'order': 5,
                },
                {
                    'label': 'Preferred Contact Method',
                    'field_name': 'contact_method',
                    'field_type': 'radio',
                    'choices': 'Phone\nEmail\nText Message',
                    'is_required': False,
                    'order': 6,
                },
                {
                    'label': 'Details & Comments',
                    'field_name': 'comments',
                    'field_type': 'textarea',
                    'placeholder': 'Please describe your needs or any questions you have...',
                    'help_text': 'Provide any additional details that would help us serve you better',
                    'is_required': False,
                    'order': 7,
                },
            ]

            for field_data in fields_to_create:
                IntakeField.objects.create(
                    form=intake_form,
                    **field_data
                )
                self.stdout.write(f'  Created field: {field_data["label"]}')

            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created intake form: /intake/{intake_form.slug}/'
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING('Client Intake Form already exists')
            )
