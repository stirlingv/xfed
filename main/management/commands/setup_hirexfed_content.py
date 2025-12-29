"""
Management command to set up initial HireXFed content.
Run with: python manage.py setup_hirexfed_content
"""
from django.core.management.base import BaseCommand
from main.models import (
    Banner, Feature, Post, MiniPost, ContactInfo, Footer,
    IntakeForm, IntakeField, DynamicPage, PageContent,
    NavigationItem, SocialMediaLink
)


class Command(BaseCommand):
    help = 'Set up initial HireXFed website content'

    def handle(self, *args, **options):
        self.stdout.write('Setting up HireXFed content...\n')

        self.setup_banner()
        self.setup_features()
        self.setup_posts()
        self.setup_mini_posts()
        self.setup_contact_info()
        self.setup_footer()
        self.setup_client_intake_form()
        self.setup_sme_intake_form()
        self.setup_pages()
        self.setup_navigation()

        self.stdout.write(self.style.SUCCESS('\n✅ HireXFed content setup complete!'))
        self.stdout.write('\nNext steps:')
        self.stdout.write('1. Review content in Django Admin')
        self.stdout.write('2. Update contact email in Intake Forms')
        self.stdout.write('3. Add your business address (optional)')
        self.stdout.write('4. Add real images to posts')
        self.stdout.write('5. Customize as needed\n')

    def setup_banner(self):
        """Set up the homepage banner"""
        self.stdout.write('  → Setting up banner...')

        Banner.objects.all().delete()
        Banner.objects.create(
            heading="Former Federal Experts Ready to Help You!",
            subheading="HireXFed connects you with seasoned federal professionals",
            description1="Whether you need help with taxes, Social Security, data systems, or IT—our network of former federal employees has the insider knowledge to solve your problems efficiently.",
            description2="With centuries of combined federal experience, our experts understand how government agencies work from the inside—and they'll put that knowledge to work for you.",
            description3="<strong>Get expert help today.</strong> Select a service category below or fill out our quick consultation form.",
            button_text="Request a Consultation",
            button_link="/intake/client-consultation/"
        )
        self.stdout.write(self.style.SUCCESS(' Done'))

    def setup_features(self):
        """Set up the service categories section (formerly 'More About Us')"""
        self.stdout.write('  → Setting up features...')

        Feature.objects.all().delete()

        features = [
            {
                'icon': 'fa-file-invoice-dollar',
                'title': 'Income Taxes (IRS)',
                'description': 'Our former IRS experts can assist with tax preparation, audit support, audit representation, tax planning, and resolving back taxes.'
            },
            {
                'icon': 'fa-id-card',
                'title': 'Social Security (SSA)',
                'description': 'Our former SSA experts can assist with needs related to Social Security payments and processing. <em>(Coming Soon)</em>'
            },
            {
                'icon': 'fa-database',
                'title': 'Data Systems',
                'description': 'Our experts can assist with needs related to agency-specific processes and data. <em>(Coming Soon)</em>'
            },
            {
                'icon': 'fa-laptop-code',
                'title': 'IT Systems',
                'description': 'Our experts can assist with needs related to agency-specific IT systems. <em>(Coming Soon)</em>'
            },
        ]

        for i, feature in enumerate(features):
            Feature.objects.create(
                icon=feature['icon'],
                title=feature['title'],
                description=feature['description']
            )
        self.stdout.write(self.style.SUCCESS(' Done'))

    def setup_posts(self):
        """Set up the 'Tax Resources & Insights' posts section"""
        self.stdout.write('  → Setting up posts...')

        Post.objects.all().delete()

        posts = [
            {
                'title': 'What To Do When You Receive an IRS Notice',
                'description': 'Receiving mail from the IRS can be stressful. Learn the first steps you should take and how to respond appropriately to protect your interests.',
                'button_text': 'Read More',
                'button_link': '/services/'
            },
            {
                'title': 'Understanding Offers in Compromise',
                'description': 'An OIC lets you settle tax debt for less than you owe. Find out if you qualify and what the process involves from our former IRS experts.',
                'button_text': 'Learn More',
                'button_link': '/services/'
            },
            {
                'title': 'Tax Liens vs. Tax Levies: Know the Difference',
                'description': 'Both can impact your finances, but they work differently. Understanding the distinction is crucial for protecting your assets.',
                'button_text': 'Read More',
                'button_link': '/services/'
            },
            {
                'title': 'Why Hire a Former IRS Agent?',
                'description': 'When facing tax issues, insider knowledge matters. Discover the advantages of working with someone who\'s been on the other side.',
                'button_text': 'Find Out',
                'button_link': '/about/'
            },
            {
                'title': 'Common Tax Filing Mistakes to Avoid',
                'description': 'Simple errors can trigger audits and penalties. Our experts share the most frequent mistakes they\'ve seen—and how to avoid them.',
                'button_text': 'Read More',
                'button_link': '/services/'
            },
            {
                'title': 'Year-Round Tax Planning Tips',
                'description': 'Tax planning shouldn\'t be a once-a-year scramble. Learn strategies to stay organized and minimize your tax burden throughout the year.',
                'button_text': 'Get Tips',
                'button_link': '/services/'
            },
        ]

        for post_data in posts:
            Post.objects.create(**post_data)

        self.stdout.write(self.style.SUCCESS(' Done'))

    def setup_mini_posts(self):
        """Set up sidebar mini posts / recent updates"""
        self.stdout.write('  → Setting up mini posts...')

        MiniPost.objects.all().delete()

        mini_posts = [
            {
                'description': '📅 Tax Season 2025: Key deadlines and what you need to know. Get prepared early to avoid last-minute stress.',
            },
            {
                'description': '🆕 Now accepting new clients for IRS audit representation. Our former agents have a 95% success rate.',
            },
            {
                'description': '💡 Did you know? You may qualify for penalty abatement if you have reasonable cause. Ask us how.',
            },
        ]

        for mini_post_data in mini_posts:
            MiniPost.objects.create(**mini_post_data)

        self.stdout.write(self.style.SUCCESS(' Done'))

    def setup_contact_info(self):
        """Set up contact information"""
        self.stdout.write('  → Setting up contact info...')

        ContactInfo.objects.all().delete()
        ContactInfo.objects.create(
            email='help@hirexfed.com',
            phone='',  # No phone - use Request a Callback instead
            address='Serving clients nationwide\nRemote consultations available'
        )

        self.stdout.write(self.style.SUCCESS(' Done'))

    def setup_footer(self):
        """Set up footer"""
        self.stdout.write('  → Setting up footer...')

        Footer.objects.all().delete()
        Footer.objects.create(
            copyright='© 2025 HireXFed. All rights reserved. Former federal expertise, working for you.'
        )

        self.stdout.write(self.style.SUCCESS(' Done'))

    def setup_client_intake_form(self):
        """Set up the client consultation intake form"""
        self.stdout.write('  → Setting up client intake form...')

        # Delete existing form if it exists
        IntakeForm.objects.filter(slug='client-consultation').delete()

        form = IntakeForm.objects.create(
            title='Request a Free Consultation',
            slug='client-consultation',
            description='Tell us about your tax situation and one of our former IRS experts will contact you within 24 hours. All information is kept strictly confidential.',
            success_message='Thank you for your inquiry! One of our tax experts will contact you within 24 hours to discuss your situation.',
            email_recipients='admin@hirexfed.com',
            is_active=True,
            allow_file_uploads=True
        )

        # Create form fields
        fields = [
            {
                'label': 'Full Name',
                'field_name': 'full_name',
                'field_type': 'text',
                'placeholder': 'John Smith',
                'is_required': True,
                'order': 1
            },
            {
                'label': 'Email Address',
                'field_name': 'email',
                'field_type': 'email',
                'placeholder': 'john@example.com',
                'is_required': True,
                'order': 2
            },
            {
                'label': 'Phone Number',
                'field_name': 'phone',
                'field_type': 'phone',
                'placeholder': '(555) 123-4567',
                'is_required': True,
                'order': 3
            },
            {
                'label': 'Best Time to Contact',
                'field_name': 'contact_time',
                'field_type': 'select',
                'choices': 'Morning (9am-12pm)\nAfternoon (12pm-5pm)\nEvening (5pm-8pm)\nAnytime',
                'is_required': False,
                'order': 4
            },
            {
                'label': 'Type of Tax Issue',
                'field_name': 'issue_type',
                'field_type': 'select',
                'choices': 'IRS Audit or Examination\nBack Taxes / Unfiled Returns\nTax Liens or Levies\nOffer in Compromise\nPayment Plan / Installment Agreement\nBusiness Tax Issues\nTax Planning\nOther Tax Matter',
                'is_required': True,
                'order': 5
            },
            {
                'label': 'Is this for an individual or business?',
                'field_name': 'client_type',
                'field_type': 'radio',
                'choices': 'Individual\nBusiness\nBoth',
                'is_required': True,
                'order': 6
            },
            {
                'label': 'Approximate Amount Owed (if applicable)',
                'field_name': 'amount_owed',
                'field_type': 'select',
                'choices': 'Less than $10,000\n$10,000 - $25,000\n$25,000 - $50,000\n$50,000 - $100,000\nOver $100,000\nNot Sure\nNot Applicable',
                'is_required': False,
                'order': 7
            },
            {
                'label': 'How urgent is your situation?',
                'field_name': 'urgency',
                'field_type': 'radio',
                'choices': 'Urgent - IRS deadline approaching\nSoon - Within the next few weeks\nPlanning ahead - No immediate deadline',
                'is_required': True,
                'order': 8
            },
            {
                'label': 'Describe Your Situation',
                'field_name': 'description',
                'field_type': 'textarea',
                'placeholder': 'Please provide details about your tax situation, including any relevant dates, amounts, or IRS notices you\'ve received...',
                'is_required': True,
                'order': 9,
                'help_text': 'The more detail you provide, the better we can prepare for your consultation.'
            },
            {
                'label': 'Upload IRS Notices or Documents (optional)',
                'field_name': 'documents',
                'field_type': 'file',
                'is_required': False,
                'order': 10,
                'help_text': 'You can upload IRS letters, notices, or other relevant documents. Accepted formats: PDF, JPG, PNG'
            },
            {
                'label': 'How did you hear about us?',
                'field_name': 'referral_source',
                'field_type': 'select',
                'choices': 'Google Search\nReferred by Friend/Family\nReferred by Another Professional\nSocial Media\nOnline Advertisement\nOther',
                'is_required': False,
                'order': 11
            },
        ]

        for field_data in fields:
            IntakeField.objects.create(form=form, **field_data)

        self.stdout.write(self.style.SUCCESS(' Done'))

    def setup_sme_intake_form(self):
        """Set up the SME (Subject Matter Expert) application form"""
        self.stdout.write('  → Setting up SME application form...')

        # Delete existing form if it exists
        IntakeForm.objects.filter(slug='join-our-team').delete()

        form = IntakeForm.objects.create(
            title='Join Our Expert Network',
            slug='join-our-team',
            description='Are you a former federal employee with tax expertise? Join HireXFed\'s network of Subject Matter Experts and help clients while earning competitive compensation. Our SMEs typically earn 75-80% of client fees.',
            success_message='Thank you for your interest in joining HireXFed! Our team will review your application and contact you within 3-5 business days to discuss next steps.',
            email_recipients='admin@hirexfed.com',
            is_active=True,
            allow_file_uploads=True
        )

        # Create form fields
        fields = [
            {
                'label': 'Full Name',
                'field_name': 'full_name',
                'field_type': 'text',
                'placeholder': 'John Smith',
                'is_required': True,
                'order': 1
            },
            {
                'label': 'Email Address',
                'field_name': 'email',
                'field_type': 'email',
                'placeholder': 'john@example.com',
                'is_required': True,
                'order': 2
            },
            {
                'label': 'Phone Number',
                'field_name': 'phone',
                'field_type': 'phone',
                'placeholder': '(555) 123-4567',
                'is_required': True,
                'order': 3
            },
            {
                'label': 'City, State',
                'field_name': 'location',
                'field_type': 'text',
                'placeholder': 'Washington, DC',
                'is_required': True,
                'order': 4
            },
            {
                'label': 'Former Federal Agency',
                'field_name': 'agency',
                'field_type': 'select',
                'choices': 'Internal Revenue Service (IRS)\nDepartment of Treasury\nGovernment Accountability Office (GAO)\nTax Court\nDepartment of Justice - Tax Division\nState Tax Agency\nOther Federal Agency',
                'is_required': True,
                'order': 5
            },
            {
                'label': 'Last Position/Title Held',
                'field_name': 'last_position',
                'field_type': 'text',
                'placeholder': 'e.g., Revenue Agent, Revenue Officer, Appeals Officer',
                'is_required': True,
                'order': 6
            },
            {
                'label': 'Years of Federal Service',
                'field_name': 'years_service',
                'field_type': 'select',
                'choices': 'Less than 5 years\n5-10 years\n10-15 years\n15-20 years\n20-25 years\n25+ years',
                'is_required': True,
                'order': 7
            },
            {
                'label': 'Year Retired/Separated',
                'field_name': 'separation_year',
                'field_type': 'text',
                'placeholder': 'e.g., 2023',
                'is_required': True,
                'order': 8
            },
            {
                'label': 'Professional Credentials (check all that apply)',
                'field_name': 'credentials',
                'field_type': 'select',
                'choices': 'Enrolled Agent (EA)\nCertified Public Accountant (CPA)\nAttorney (JD)\nCertified Financial Planner (CFP)\nOther Professional License\nNone Currently',
                'is_required': True,
                'order': 9
            },
            {
                'label': 'Areas of Expertise (select primary area)',
                'field_name': 'expertise',
                'field_type': 'select',
                'choices': 'Individual Tax Examination/Audit\nBusiness Tax Examination\nCollection (Liens, Levies, Seizures)\nOffers in Compromise\nAppeals\nCriminal Investigation\nInternational Tax\nEstate & Gift Tax\nExcise Tax\nTax-Exempt Organizations\nEmployee Plans\nOther',
                'is_required': True,
                'order': 10
            },
            {
                'label': 'Describe Your Federal Experience',
                'field_name': 'experience_description',
                'field_type': 'textarea',
                'placeholder': 'Please describe your federal experience, key accomplishments, and the types of cases you worked on...',
                'is_required': True,
                'order': 11,
                'help_text': 'This helps us match you with appropriate client cases.'
            },
            {
                'label': 'Current Work Situation',
                'field_name': 'availability',
                'field_type': 'radio',
                'choices': 'Fully retired - available for significant work\nPartially retired - available for limited engagements\nCurrently employed - looking for side work\nSelf-employed - looking to expand client base',
                'is_required': True,
                'order': 12
            },
            {
                'label': 'Preferred Work Arrangement',
                'field_name': 'work_preference',
                'field_type': 'select',
                'choices': 'Remote only\nIn-person only (local clients)\nHybrid (remote + occasional in-person)\nNo preference',
                'is_required': True,
                'order': 13
            },
            {
                'label': 'Upload Resume/CV',
                'field_name': 'resume',
                'field_type': 'file',
                'is_required': True,
                'order': 14,
                'help_text': 'Please upload your current resume. Accepted formats: PDF, DOC, DOCX'
            },
            {
                'label': 'LinkedIn Profile URL (optional)',
                'field_name': 'linkedin',
                'field_type': 'text',
                'placeholder': 'https://linkedin.com/in/yourprofile',
                'is_required': False,
                'order': 15
            },
            {
                'label': 'How did you hear about HireXFed?',
                'field_name': 'referral_source',
                'field_type': 'select',
                'choices': 'Former colleague\nLinkedIn\nGoogle search\nFederal retirement community\nOther',
                'is_required': False,
                'order': 16
            },
            {
                'label': 'Anything else you\'d like us to know?',
                'field_name': 'additional_info',
                'field_type': 'textarea',
                'placeholder': 'Optional additional information...',
                'is_required': False,
                'order': 17
            },
        ]

        for field_data in fields:
            IntakeField.objects.create(form=form, **field_data)

        self.stdout.write(self.style.SUCCESS(' Done'))

    def setup_pages(self):
        """Set up dynamic pages"""
        self.stdout.write('  → Setting up pages...')

        # About Page
        about_page, _ = DynamicPage.objects.update_or_create(
            slug='about',
            defaults={
                'title': 'About HireXFed',
                'template_type': 'generic',
                'meta_description': 'Learn about HireXFed - connecting clients with former federal experts for professional services.',
                'is_published': True,
                'show_in_navigation': False
            }
        )

        PageContent.objects.filter(page='about').delete()
        PageContent.objects.create(
            page='about',
            section_type='main_content',
            title='Who We Are',
            content='''<p><strong>HireXFed</strong> is a professional network connecting individuals and businesses with former federal employees—IRS agents, SSA specialists, data experts, and IT professionals.</p>

<p>Our experts have spent decades inside federal agencies. They understand how these systems work from the inside, and now they're using that insider knowledge to help you navigate government processes.</p>

<h3>Why Former Federal Experts?</h3>
<p>When you're dealing with a federal agency, you want someone who truly understands how it works. Our network members have:</p>
<ul>
    <li>Processed thousands of cases from the government side</li>
    <li>Deep knowledge of agency procedures, priorities, and decision-making</li>
    <li>Established professional relationships within their fields</li>
    <li>The credentials and experience to represent you effectively</li>
</ul>

<h3>Our Mission</h3>
<p>Since January 20, 2025, thousands of experienced federal employees have been forced out through various actions. HireXFed was founded to harness this expertise for the benefit of the American public.</p>

<p><strong>Individually we are Valuable. Collectively, we are Unstoppable!</strong></p>

<p>By banding together as a national network of former federal professionals, we are in a unique position to offer you the benefit of thousands of years of combined government experience.</p>

<h3>Our Commitment to You</h3>
<ul>
    <li><strong>Transparency</strong> – Clear pricing with no hidden fees</li>
    <li><strong>Confidentiality</strong> – Your information is always protected</li>
    <li><strong>Excellence</strong> – Only vetted, experienced professionals in our network</li>
    <li><strong>Results</strong> – We don't stop until your issue is resolved</li>
</ul>

<p style="margin-top: 2em;"><a href="/intake/client-consultation/" class="button">Get Help Now</a> <a href="/members/" class="button" style="margin-left: 1em;">Join the Network</a></p>''',
            order=1,
            is_active=True
        )

        # Tax Solutions Landing Page
        tax_solutions, _ = DynamicPage.objects.update_or_create(
            slug='tax-solutions',
            defaults={
                'title': 'Tax Solutions',
                'template_type': 'generic',
                'meta_description': 'Former IRS experts solving your tax problems. Tax preparation, audit support, representation, and more.',
                'is_published': True,
                'show_in_navigation': False
            }
        )

        PageContent.objects.filter(page='tax-solutions').delete()
        PageContent.objects.create(
            page='tax-solutions',
            section_type='main_content',
            title='Former IRS Experts Solving Your Tax Problems',
            content='''<p class="lead">Seasoned federal tax professionals are ready to help.</p>

<p>Need tax preparation? Facing an IRS audit? Dealing with back taxes? Need expert assistance?</p>

<p>Our network of former IRS agents, revenue officers, and tax specialists have the insider knowledge to resolve your tax issues. With <strong>centuries of combined federal experience</strong>, our experts understand how the IRS works from the inside—and they'll put that knowledge to work for you.</p>

<h3>Network Benefits</h3>
<ul>
    <li>Enjoy the benefits of thousands of years of IRS experience</li>
    <li><strong>Free Audit Coaching</strong> – You are not alone during any IRS action</li>
    <li>Competitive rates with exceptional value</li>
    <li>100% Online – Simply complete a questionnaire and upload your tax information to our secure client portal</li>
</ul>

<h3>Our Services Include:</h3>
<ul>
    <li>Tax Return Preparation</li>
    <li>Audit Consultation</li>
    <li>Audit Representation</li>
    <li>Tax Planning</li>
    <li>Bookkeeping</li>
    <li>Accounting System Setup</li>
</ul>

<p style="margin-top: 2em;">
    <a href="/tax-solutions/services/" class="button primary">View Services & Pricing</a>
    <a href="/intake/client-consultation/" class="button" style="margin-left: 1em;">Request Information</a>
</p>''',
            order=1,
            is_active=True
        )

        # Tax Services Pricing Page
        tax_services, _ = DynamicPage.objects.update_or_create(
            slug='tax-solutions/services',
            defaults={
                'title': 'Tax Services & Pricing',
                'template_type': 'generic',
                'meta_description': 'Tax preparation, audit support, and representation pricing from former IRS professionals.',
                'is_published': True,
                'show_in_navigation': False
            }
        )

        PageContent.objects.filter(page='tax-solutions/services').delete()
        PageContent.objects.create(
            page='tax-solutions/services',
            section_type='main_content',
            title='Available Services',
            content='''<p>Our network of former IRS professionals offers transparent, competitive pricing for all tax services.</p>

<h3>Tax Preparation – Individual (Form 1040)</h3>
<table style="width: 100%; border-collapse: collapse; margin: 1em 0;">
<tr style="background: #f9f9f9;">
    <td style="padding: 0.75em; border: 1px solid #ddd;"><strong>Form 1040 (Base Return)</strong></td>
    <td style="padding: 0.75em; border: 1px solid #ddd; text-align: right;"><strong>$300</strong></td>
</tr>
<tr>
    <td style="padding: 0.75em; border: 1px solid #ddd;">Schedule A – Itemized Deductions</td>
    <td style="padding: 0.75em; border: 1px solid #ddd; text-align: right;">Included</td>
</tr>
<tr style="background: #f9f9f9;">
    <td style="padding: 0.75em; border: 1px solid #ddd;">Schedule C or F – Business Return</td>
    <td style="padding: 0.75em; border: 1px solid #ddd; text-align: right;">$500 per schedule</td>
</tr>
<tr>
    <td style="padding: 0.75em; border: 1px solid #ddd;">Schedule D – Capital Gains/Losses</td>
    <td style="padding: 0.75em; border: 1px solid #ddd; text-align: right;">$200</td>
</tr>
<tr style="background: #f9f9f9;">
    <td style="padding: 0.75em; border: 1px solid #ddd;">Schedule E, Part I – Rental Properties</td>
    <td style="padding: 0.75em; border: 1px solid #ddd; text-align: right;">$500 per property</td>
</tr>
<tr>
    <td style="padding: 0.75em; border: 1px solid #ddd;">Schedule E, Part II – Flow Through Entities</td>
    <td style="padding: 0.75em; border: 1px solid #ddd; text-align: right;">$200</td>
</tr>
</table>

<h3>Tax Preparation – Business Returns</h3>
<table style="width: 100%; border-collapse: collapse; margin: 1em 0;">
<tr style="background: #f9f9f9;">
    <td style="padding: 0.75em; border: 1px solid #ddd;"><strong>Form 1120S – S-Corporation</strong></td>
    <td style="padding: 0.75em; border: 1px solid #ddd; text-align: right;"><strong>$2,500</strong></td>
</tr>
<tr>
    <td style="padding: 0.75em; border: 1px solid #ddd;"><strong>Form 1120 – Corporation</strong></td>
    <td style="padding: 0.75em; border: 1px solid #ddd; text-align: right;"><strong>$2,500</strong></td>
</tr>
<tr style="background: #f9f9f9;">
    <td style="padding: 0.75em; border: 1px solid #ddd;"><strong>Form 1065 – Partnership</strong></td>
    <td style="padding: 0.75em; border: 1px solid #ddd; text-align: right;"><strong>$3,000</strong></td>
</tr>
<tr>
    <td style="padding: 0.75em; border: 1px solid #ddd;">Amended Returns</td>
    <td style="padding: 0.75em; border: 1px solid #ddd; text-align: right;">20% of original fee</td>
</tr>
</table>

<h3>Audit & Representation Services</h3>
<table style="width: 100%; border-collapse: collapse; margin: 1em 0;">
<tr style="background: #f9f9f9;">
    <td style="padding: 0.75em; border: 1px solid #ddd;"><strong>Audit Support (Existing Clients)</strong></td>
    <td style="padding: 0.75em; border: 1px solid #ddd; text-align: right;"><strong>FREE</strong></td>
</tr>
<tr>
    <td style="padding: 0.75em; border: 1px solid #ddd;">Audit Support (Non-Clients)</td>
    <td style="padding: 0.75em; border: 1px solid #ddd; text-align: right;">$100/hour</td>
</tr>
<tr style="background: #f9f9f9;">
    <td style="padding: 0.75em; border: 1px solid #ddd;"><strong>Audit Representation</strong></td>
    <td style="padding: 0.75em; border: 1px solid #ddd; text-align: right;"><strong>$250/hour</strong></td>
</tr>
</table>

<h3>Additional Services</h3>
<table style="width: 100%; border-collapse: collapse; margin: 1em 0;">
<tr style="background: #f9f9f9;">
    <td style="padding: 0.75em; border: 1px solid #ddd;">Accounting System Setup</td>
    <td style="padding: 0.75em; border: 1px solid #ddd; text-align: right;">$500 per business</td>
</tr>
<tr>
    <td style="padding: 0.75em; border: 1px solid #ddd;">Tax Planning Consultation</td>
    <td style="padding: 0.75em; border: 1px solid #ddd; text-align: right;">$500 (1-hour session)</td>
</tr>
<tr style="background: #f9f9f9;">
    <td style="padding: 0.75em; border: 1px solid #ddd;">Bookkeeping</td>
    <td style="padding: 0.75em; border: 1px solid #ddd; text-align: right;">$100/hour</td>
</tr>
</table>

<hr>

<p style="text-align: center; margin-top: 2em;">
    <a href="/intake/client-consultation/" class="button primary large">Request a Free Consultation</a>
</p>''',
            order=1,
            is_active=True
        )

        # Members Landing Page
        members_page, _ = DynamicPage.objects.update_or_create(
            slug='members',
            defaults={
                'title': 'Join the Network',
                'template_type': 'generic',
                'meta_description': 'Join America\'s largest network of former federal employees. Work from home, set your own schedule, keep more of what you earn.',
                'is_published': True,
                'show_in_navigation': False
            }
        )

        PageContent.objects.filter(page='members').delete()
        PageContent.objects.create(
            page='members',
            section_type='main_content',
            title='Individually We Are Valuable. Collectively, We Are Unstoppable!',
            content='''<p class="lead">Add your years of experience and expertise to the Network.</p>

<p>Whether you ended your Federal career prematurely due to recent actions or any other reason, and you want to help both the Nation and your fellow former Federal Employees succeed, join the Nationwide Network.</p>

<p>Adding your years of experience and expertise will be valuable as the Federal Government begins to rebuild after the sudden and disastrous departures of thousands of experienced federal employees.</p>

<h3>Membership Benefits</h3>
<ul>
    <li>Enjoy the benefits of shared knowledge from the Network</li>
    <li><strong>Work from home, or anywhere!</strong></li>
    <li>Members are independent contractors—work as much or as little as you like</li>
    <li>Enjoy independent contractor business deductions</li>
    <li>Have your own clients? GREAT! Take advantage of our cloud-based software and shared knowledge</li>
    <li>Keep a larger percentage of profits due to low operating costs</li>
</ul>

<h3>Membership Requirements</h3>
<ul>
    <li>✓ Federal agency experience</li>
    <li>✓ A computer</li>
    <li>✓ Internet access</li>
    <li>✓ Valid PTIN (for tax professionals)</li>
    <li>✓ $100 Annual Membership Fee</li>
</ul>

<h3>How It Works</h3>
<p>As a Network member, you will be an independent contractor who determines your own work schedule and projects. Projects will be offered, as available, according to each member's specific knowledge and experience.</p>

<p>While the initial workflow may amount to little more than a side hustle, there is expected to be a sharp increase in available work for members as the true repercussions of recent federal workforce changes are realized.</p>

<p>The Network provides customers (e.g., Federal contractors, taxpayers, etc.) with a consolidated and separate pool of knowledge to leverage on an ad hoc basis. Similarly, Members can leverage knowledge of the entire Network.</p>

<h3>Join a Division</h3>
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1em; margin: 1.5em 0;">
    <div style="background: #f5f5f5; padding: 1.5em; border-radius: 8px; text-align: center;">
        <strong>Income Taxes (IRS)</strong><br>
        <a href="/members/tax-solutions/">Learn More</a>
    </div>
    <div style="background: #f5f5f5; padding: 1.5em; border-radius: 8px; text-align: center;">
        <strong>Social Security (SSA)</strong><br>
        <em>Coming Soon</em>
    </div>
    <div style="background: #f5f5f5; padding: 1.5em; border-radius: 8px; text-align: center;">
        <strong>Data Systems</strong><br>
        <em>Coming Soon</em>
    </div>
    <div style="background: #f5f5f5; padding: 1.5em; border-radius: 8px; text-align: center;">
        <strong>IT Systems</strong><br>
        <em>Coming Soon</em>
    </div>
</div>

<p style="text-align: center; margin-top: 2em;">
    <a href="/intake/join-our-team/" class="button primary large">Apply to Join the Network</a>
</p>''',
            order=1,
            is_active=True
        )

        # Tax Solutions Members Page
        tax_members, _ = DynamicPage.objects.update_or_create(
            slug='members/tax-solutions',
            defaults={
                'title': 'Tax Solutions Members',
                'template_type': 'generic',
                'meta_description': 'Join America\'s largest network of former IRS examiners. Work from home and leverage your federal tax experience.',
                'is_published': True,
                'show_in_navigation': False
            }
        )

        PageContent.objects.filter(page='members/tax-solutions').delete()
        PageContent.objects.create(
            page='members/tax-solutions',
            section_type='main_content',
            title='Join America\'s Largest Network of Ex-IRS Examiners',
            content='''<p class="lead">Our network of tax professionals helps individuals and small businesses with their tax needs.</p>

<h3>Services You Can Provide</h3>
<ul>
    <li>Tax Return Preparation</li>
    <li>Audit Consultation</li>
    <li>Audit Representation</li>
    <li>Tax Planning</li>
    <li>Bookkeeping</li>
    <li>Accounting System Setup</li>
</ul>

<h3>Membership Benefits</h3>
<ul>
    <li>Enjoy the benefits of shared knowledge from the Network</li>
    <li>Work from home, or anywhere!</li>
    <li>Members are independent contractors, so work as much, or little, as you like</li>
    <li>Enjoy independent contractor business deductions</li>
    <li>Have your own clients? GREAT! Take advantage of our cloud-based tax preparation software and shared knowledge</li>
</ul>

<h3>Membership Requirements</h3>
<ul>
    <li>✓ IRS Experience</li>
    <li>✓ A Computer</li>
    <li>✓ Internet Access</li>
    <li>✓ Valid PTIN</li>
    <li>✓ $100 Annual Membership Fee</li>
</ul>

<p>By banding together as a national network of tax professionals, we are in a unique position to offer taxpayers the benefit of thousands of years of IRS experience to maximize their tax savings and provide effective support for navigating any IRS interaction.</p>

<p style="text-align: center; margin-top: 2em;">
    <a href="/intake/join-our-team/" class="button primary large">Apply to Join</a>
</p>''',
            order=1,
            is_active=True
        )

        # Coming Soon pages for other services
        for slug, title, description in [
            ('social-security', 'Social Security Services', 'Former SSA experts helping with Social Security payments and processing.'),
            ('data-systems', 'Data Systems Services', 'Former federal experts helping with agency-specific processes and data.'),
            ('it-systems', 'IT Systems Services', 'Former federal experts helping with agency-specific IT systems.'),
        ]:
            page, _ = DynamicPage.objects.update_or_create(
                slug=slug,
                defaults={
                    'title': title,
                    'template_type': 'generic',
                    'meta_description': description,
                    'is_published': True,
                    'show_in_navigation': False
                }
            )

            PageContent.objects.filter(page=slug).delete()
            PageContent.objects.create(
                page=slug,
                section_type='main_content',
                title='Coming Soon',
                content=f'''<p class="lead">{description}</p>

<p>We are currently building our network of former federal professionals in this area. Check back soon for updates!</p>

<h3>Interested in Joining?</h3>
<p>If you're a former federal employee with expertise in this area, we'd love to hear from you. Join our network and help us build this service.</p>

<p style="margin-top: 2em;">
    <a href="/intake/join-our-team/" class="button primary">Apply to Join the Network</a>
    <a href="/" class="button" style="margin-left: 1em;">Back to Home</a>
</p>''',
                order=1,
                is_active=True
            )

        # Keep legacy services and how-it-works pages but update them
        services_page, _ = DynamicPage.objects.update_or_create(
            slug='services',
            defaults={
                'title': 'All Services',
                'template_type': 'generic',
                'meta_description': 'Professional services from former federal employees - tax, Social Security, data, and IT expertise.',
                'is_published': True,
                'show_in_navigation': False
            }
        )

        PageContent.objects.filter(page='services').delete()
        PageContent.objects.create(
            page='services',
            section_type='main_content',
            title='How Can We Help You?',
            content='''<p class="lead">Our network of former federal professionals offers expertise across multiple disciplines.</p>

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5em; margin: 2em 0;">
    <div style="background: #f5f5f5; padding: 2em; border-radius: 8px;">
        <h3>💰 Income Taxes (IRS)</h3>
        <p>Tax preparation, audit support, audit representation, tax planning, bookkeeping, and accounting system setup.</p>
        <a href="/tax-solutions/" class="button">Learn More</a>
    </div>
    <div style="background: #f5f5f5; padding: 2em; border-radius: 8px;">
        <h3>🆔 Social Security (SSA)</h3>
        <p>Assistance with Social Security payments and processing needs.</p>
        <em>Coming Soon</em>
    </div>
    <div style="background: #f5f5f5; padding: 2em; border-radius: 8px;">
        <h3>📊 Data Systems</h3>
        <p>Help with agency-specific processes and data needs.</p>
        <em>Coming Soon</em>
    </div>
    <div style="background: #f5f5f5; padding: 2em; border-radius: 8px;">
        <h3>💻 IT Systems</h3>
        <p>Assistance with agency-specific IT systems.</p>
        <em>Coming Soon</em>
    </div>
</div>

<hr>

<h3>Are You a Former Federal Employee?</h3>
<p>Join our growing network of professionals. Work from anywhere, set your own schedule, and leverage your federal experience.</p>
<p><a href="/members/" class="button">Join the Network</a></p>''',
            order=1,
            is_active=True
        )

        # How It Works Page (updated)
        how_it_works, _ = DynamicPage.objects.update_or_create(
            slug='how-it-works',
            defaults={
                'title': 'How It Works',
                'template_type': 'generic',
                'meta_description': 'Learn how HireXFed connects you with former federal experts to solve your problems.',
                'is_published': True,
                'show_in_navigation': False
            }
        )

        PageContent.objects.filter(page='how-it-works').delete()
        PageContent.objects.create(
            page='how-it-works',
            section_type='main_content',
            title='Simple Process, Expert Results',
            content='''<p>Getting expert help is straightforward. Here's how it works:</p>

<div style="background: #f5f5f5; padding: 1.5em; border-radius: 8px; margin: 1.5em 0;">
<h3>Step 1: Tell Us About Your Situation</h3>
<p>Complete our online questionnaire with details about your needs. Everything you share is completely confidential. You can also upload relevant documents to our secure portal.</p>
<p><em>⏱️ Takes about 5 minutes</em></p>
</div>

<div style="background: #f5f5f5; padding: 1.5em; border-radius: 8px; margin: 1.5em 0;">
<h3>Step 2: We Match You With an Expert</h3>
<p>Based on your specific situation, we identify the ideal expert from our network. Our members have the insider knowledge and experience to handle your exact needs.</p>
<p><em>🎯 Expertise matched to your exact situation</em></p>
</div>

<div style="background: #f5f5f5; padding: 1.5em; border-radius: 8px; margin: 1.5em 0;">
<h3>Step 3: Expert Assistance</h3>
<p>A network member will contact you to review your situation, explain your options, and provide clear pricing—no surprises, no pressure.</p>
<p><em>💬 100% online convenience</em></p>
</div>

<div style="background: #f5f5f5; padding: 1.5em; border-radius: 8px; margin: 1.5em 0;">
<h3>Step 4: Resolution</h3>
<p>We don't consider the job done until your issue is fully resolved. Our experts see it through to completion.</p>
<p><em>🏆 Results-driven approach</em></p>
</div>

<hr>

<h3>💡 Why Our Model Works</h3>
<p><strong>For Clients:</strong> You get direct access to former federal experts at competitive rates—because we don't have the overhead of big firms.</p>
<p><strong>For Our Members:</strong> Network members keep more of what they earn as independent contractors, attracting and retaining top talent.</p>
<p><strong>The Result:</strong> Top-tier expertise at fair prices. Everyone wins.</p>

<p style="text-align: center; margin-top: 2em;"><a href="/intake/client-consultation/" class="button primary large">Get Started Today</a></p>''',
            order=1,
            is_active=True
        )

        self.stdout.write(self.style.SUCCESS(' Done'))

    def setup_navigation(self):
        """Set up navigation menu"""
        self.stdout.write('  → Setting up navigation...')

        # Clear existing navigation
        NavigationItem.objects.all().delete()

        # Turn off show_in_navigation for all dynamic pages
        DynamicPage.objects.update(show_in_navigation=False)

        # Main navigation items
        nav_items = [
            {'title': 'Home', 'url': '/', 'order': 10},
            {'title': 'Services', 'url': '/services/', 'order': 20},
            {'title': 'Tax Solutions', 'url': '/tax-solutions/', 'order': 30},
            {'title': 'How It Works', 'url': '/how-it-works/', 'order': 40},
            {'title': 'About', 'url': '/about/', 'order': 50},
            {'title': 'Join the Network', 'url': '/members/', 'order': 60},
            {'title': 'Get Help Now', 'url': '/intake/client-consultation/', 'order': 70},
        ]

        for item in nav_items:
            NavigationItem.objects.create(**item, is_active=True)

        self.stdout.write(self.style.SUCCESS(' Done'))
