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
        self.stdout.write('3. Add your real phone number and address')
        self.stdout.write('4. Add real images to posts')
        self.stdout.write('5. Customize as needed\n')

    def setup_banner(self):
        """Set up the homepage banner"""
        self.stdout.write('  → Setting up banner...')

        Banner.objects.all().delete()
        Banner.objects.create(
            heading="Former IRS Experts Solving Your Tax Problems",
            subheading="HireXFed connects you with seasoned federal tax professionals",
            description1="Facing an IRS audit? Dealing with back taxes? Need expert representation? Our network of former IRS agents, revenue officers, and tax specialists have the insider knowledge to resolve your tax issues efficiently.",
            description2="With decades of combined federal experience, our experts understand how the IRS works from the inside—and they'll put that knowledge to work for you.",
            description3="<strong>Get expert help today.</strong> Fill out our quick consultation form or call us to discuss your situation confidentially.",
            button_text="Request Free Consultation",
            button_link="/intake/client-consultation/"
        )
        self.stdout.write(self.style.SUCCESS(' Done'))

    def setup_features(self):
        """Set up the 'More About Us' features section"""
        self.stdout.write('  → Setting up features...')

        Feature.objects.all().delete()

        features = [
            {
                'icon': 'fa-shield-alt',
                'title': 'IRS Audit Defense',
                'description': 'Our former IRS auditors know exactly what the agency looks for. We\'ll guide you through the audit process and protect your interests.'
            },
            {
                'icon': 'fa-file-invoice-dollar',
                'title': 'Back Taxes & Unfiled Returns',
                'description': 'Years of unfiled returns? We help you get compliant with the IRS while minimizing penalties and finding the best path forward.'
            },
            {
                'icon': 'fa-handshake',
                'title': 'Offers in Compromise',
                'description': 'Settle your tax debt for less than you owe. Our experts have processed thousands of OICs and know what it takes to get approved.'
            },
            {
                'icon': 'fa-building',
                'title': 'Business Tax Services',
                'description': 'Complex business tax situations require expert guidance. From S-Corps to partnerships, we handle sophisticated tax matters.'
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
            phone='(888) HIRE-FED',
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
            success_message='Thank you for your inquiry! One of our tax experts will contact you within 24 hours to discuss your situation. If your matter is urgent, please call us directly.',
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
            email_recipients='recruiting@hirexfed.com',
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
                'meta_description': 'Learn about HireXFed - connecting clients with former IRS and federal tax experts for professional tax resolution services.',
                'is_published': True,
                'show_in_navigation': False
            }
        )

        # Delete existing content for this page and recreate
        PageContent.objects.filter(page='about').delete()
        PageContent.objects.create(
            page='about',
            section_type='main_content',
            title='Who We Are',
            content='''<p><strong>HireXFed</strong> is a professional network connecting individuals and businesses with former IRS agents, revenue officers, and federal tax specialists.</p>

<p>Our experts have spent decades inside the federal tax system. They've conducted audits, processed offers in compromise, resolved complex tax disputes, and helped shape tax policy. Now, they're using that insider knowledge to help taxpayers navigate the system.</p>

<h3>Why Former Federal Experts?</h3>
<p>When you're facing an IRS issue, you want someone who truly understands how the agency works. Our Subject Matter Experts (SMEs) have:</p>
<ul>
    <li>Processed thousands of tax cases from the government side</li>
    <li>Deep knowledge of IRS procedures, priorities, and decision-making</li>
    <li>Established professional relationships within the tax community</li>
    <li>The credentials and experience to represent you effectively</li>
</ul>

<h3>Our Mission</h3>
<p>We founded HireXFed with a simple belief: <strong>everyone deserves access to expert tax help at fair prices</strong>. Big accounting firms charge premium rates for overhead-heavy services. We connect you directly with the experts—cutting out the middleman and passing the savings to you.</p>

<h3>For Former Federal Employees</h3>
<p>After years of dedicated public service, many federal tax professionals retire with unmatched expertise and a desire to keep working on their own terms. HireXFed provides a platform to leverage your skills, work flexible hours, and earn what you're worth—typically 75-80% of client fees.</p>

<h3>Our Commitment to You</h3>
<p>Whether you're a taxpayer seeking help or a former federal employee looking to join our network, we're committed to:</p>
<ul>
    <li><strong>Transparency</strong> – Clear pricing with no hidden fees</li>
    <li><strong>Confidentiality</strong> – Your information is always protected</li>
    <li><strong>Excellence</strong> – Only vetted, experienced professionals in our network</li>
    <li><strong>Results</strong> – We don't stop until your issue is resolved</li>
</ul>

<p style="margin-top: 2em;"><a href="/intake/client-consultation/" class="button">Request a Free Consultation</a> <a href="/intake/join-our-team/" class="button" style="margin-left: 1em;">Join Our Expert Network</a></p>''',
            order=1,
            is_active=True
        )

        # Services Page
        services_page, _ = DynamicPage.objects.update_or_create(
            slug='services',
            defaults={
                'title': 'Our Services',
                'template_type': 'generic',
                'meta_description': 'IRS audit defense, back taxes, offers in compromise, tax liens, and business tax services from former IRS professionals.',
                'is_published': True,
                'show_in_navigation': False
            }
        )

        PageContent.objects.filter(page='services').delete()
        PageContent.objects.create(
            page='services',
            section_type='main_content',
            title='Tax Resolution Services',
            content='''<p>Our network of former IRS professionals provides expert assistance with complex tax matters. We specialize in cases where insider knowledge makes a real difference.</p>

<h3>🛡️ IRS Audit Defense</h3>
<p>Received an audit notice? Our former IRS auditors know exactly what the agency is looking for. We'll review your situation, prepare your documentation, and represent you throughout the examination process to achieve the best possible outcome.</p>
<p><em>Our experts have conducted thousands of audits—now they're on your side.</em></p>

<h3>📋 Back Taxes & Unfiled Returns</h3>
<p>Years of unfiled returns can feel overwhelming. We help you get back into compliance with the IRS while minimizing penalties and interest. Our experts will prepare your returns and negotiate with the IRS on your behalf.</p>
<p><em>It's never too late to get right with the IRS. Let us show you how.</em></p>

<h3>💰 Offers in Compromise</h3>
<p>An Offer in Compromise lets you settle your tax debt for less than you owe. Our former IRS specialists have processed thousands of OICs and know what it takes to get your offer accepted. We'll evaluate your eligibility and prepare a compelling case.</p>
<p><em>Not everyone qualifies—but when you do, the savings can be substantial.</em></p>

<h3>⚠️ Tax Liens & Levies</h3>
<p>IRS liens and levies can devastate your finances and credit. We work quickly to release levies, subordinate or discharge liens, and protect your assets while resolving the underlying tax debt.</p>
<p><em>Time is critical. Contact us immediately if you've received a levy notice.</em></p>

<h3>📅 Payment Plans & Installment Agreements</h3>
<p>Can't pay your tax bill in full? We'll negotiate an installment agreement that fits your budget while keeping the IRS from taking collection action. We can also help with Currently Not Collectible (CNC) status if you truly cannot pay.</p>

<h3>🏢 Business Tax Services</h3>
<p>From S-Corp elections to partnership returns, our experts handle complex business tax matters. We provide strategic planning and representation for businesses of all sizes, including:</p>
<ul>
    <li>Payroll tax issues and trust fund recovery penalties</li>
    <li>Business entity selection and restructuring</li>
    <li>Employment tax audits</li>
    <li>Sales tax and state tax compliance</li>
</ul>

<h3>🔒 Penalty Abatement</h3>
<p>The IRS assesses penalties automatically, but many can be reduced or eliminated with proper documentation. We'll identify opportunities for penalty abatement based on reasonable cause, first-time penalty abatement, or administrative waiver.</p>

<h3>🌐 International Tax Issues</h3>
<p>FBAR filings, FATCA compliance, foreign income reporting—international tax law is complex. Our experts help U.S. taxpayers with foreign accounts and foreign nationals with U.S. tax obligations navigate these complicated requirements.</p>

<hr>

<h3>📞 Ready to Get Started?</h3>
<p>Tell us about your situation and one of our former IRS experts will contact you within 24 hours.</p>
<p><a href="/intake/client-consultation/" class="button primary">Request Your Free Consultation</a></p>''',
            order=1,
            is_active=True
        )

        # How It Works Page
        how_it_works, _ = DynamicPage.objects.update_or_create(
            slug='how-it-works',
            defaults={
                'title': 'How It Works',
                'template_type': 'generic',
                'meta_description': 'Learn how HireXFed connects you with former IRS experts to resolve your tax issues.',
                'is_published': True,
                'show_in_navigation': False
            }
        )

        PageContent.objects.filter(page='how-it-works').delete()
        PageContent.objects.create(
            page='how-it-works',
            section_type='main_content',
            title='Simple Process, Expert Results',
            content='''<p>Getting expert help with your tax issue is straightforward. Here's how it works:</p>

<div style="background: #f5f5f5; padding: 1.5em; border-radius: 8px; margin: 1.5em 0;">
<h3>Step 1: Tell Us About Your Situation</h3>
<p>Fill out our <a href="/intake/client-consultation/">consultation request form</a> with details about your tax issue. Everything you share is completely confidential. You can also upload any IRS notices or documents you've received.</p>
<p><em>⏱️ Takes about 5 minutes</em></p>
</div>

<div style="background: #f5f5f5; padding: 1.5em; border-radius: 8px; margin: 1.5em 0;">
<h3>Step 2: We Match You With an Expert</h3>
<p>Based on your specific situation, we identify the ideal Subject Matter Expert from our network. Need audit defense? We'll connect you with a former IRS auditor. Dealing with collections? You'll work with a former Revenue Officer who knows exactly how to resolve your case.</p>
<p><em>🎯 Expertise matched to your exact situation</em></p>
</div>

<div style="background: #f5f5f5; padding: 1.5em; border-radius: 8px; margin: 1.5em 0;">
<h3>Step 3: Free Initial Consultation</h3>
<p>Your matched expert will contact you within 24 hours for a free consultation. They'll review your situation, explain your options, and provide a clear quote for their services—no surprises, no pressure.</p>
<p><em>💬 No obligation, no cost to explore your options</em></p>
</div>

<div style="background: #f5f5f5; padding: 1.5em; border-radius: 8px; margin: 1.5em 0;">
<h3>Step 4: Expert Representation</h3>
<p>Once you engage our services, your expert handles everything: communicating with the IRS, preparing necessary documents, representing you in meetings or calls, and working toward the best possible resolution.</p>
<p><em>✅ You focus on your life—we handle the IRS</em></p>
</div>

<div style="background: #f5f5f5; padding: 1.5em; border-radius: 8px; margin: 1.5em 0;">
<h3>Step 5: Resolution</h3>
<p>We don't consider the job done until your tax issue is fully resolved. Whether that's a favorable audit outcome, an accepted offer in compromise, or a manageable payment plan, we see it through to completion.</p>
<p><em>🏆 Results-driven approach from start to finish</em></p>
</div>

<hr>

<h3>💡 Why Our Model Works</h3>

<table style="width: 100%; border-collapse: collapse; margin: 1em 0;">
<tr style="background: #f9f9f9;">
<td style="padding: 1em; border: 1px solid #ddd;"><strong>For Clients</strong></td>
<td style="padding: 1em; border: 1px solid #ddd;">You get direct access to former IRS experts at rates significantly lower than big accounting firms—because we don't have their overhead.</td>
</tr>
<tr>
<td style="padding: 1em; border: 1px solid #ddd;"><strong>For Our Experts</strong></td>
<td style="padding: 1em; border: 1px solid #ddd;">Our SMEs earn 75-80% of fees, far more than they'd make as employees. This attracts and retains the best talent.</td>
</tr>
<tr style="background: #f9f9f9;">
<td style="padding: 1em; border: 1px solid #ddd;"><strong>The Result</strong></td>
<td style="padding: 1em; border: 1px solid #ddd;">Top-tier expertise at fair prices. Everyone wins.</td>
</tr>
</table>

<h3>Frequently Asked Questions</h3>

<p><strong>How much does it cost?</strong><br>
Your initial consultation is always free. Fees vary depending on the complexity of your case, but you'll receive a clear quote before any work begins. Most cases are handled on a flat-fee basis so you know exactly what to expect.</p>

<p><strong>How long does resolution take?</strong><br>
It depends on your situation and the IRS. Simple matters may resolve in weeks; complex cases involving appeals or offers in compromise can take several months. We'll give you a realistic timeline during your consultation.</p>

<p><strong>Is my information confidential?</strong><br>
Absolutely. All communications are protected by professional confidentiality standards. We never share your information without your explicit consent.</p>

<p><strong>What if I can't afford to pay?</strong><br>
That's one of the first things we assess. If you truly can't pay, we can help you apply for Currently Not Collectible status or explore Offer in Compromise options.</p>

<hr>

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
        # (we'll manage nav through NavigationItem instead)
        DynamicPage.objects.update(show_in_navigation=False)

        nav_items = [
            {'title': 'Home', 'url': '/', 'order': 1},
            {'title': 'Services', 'url': '/services/', 'order': 2},
            {'title': 'How It Works', 'url': '/how-it-works/', 'order': 3},
            {'title': 'About', 'url': '/about/', 'order': 4},
            {'title': 'Get Help Now', 'url': '/intake/client-consultation/', 'order': 5},
            {'title': 'Join Our Team', 'url': '/intake/join-our-team/', 'order': 6},
        ]

        for item in nav_items:
            NavigationItem.objects.create(**item, is_active=True)

        self.stdout.write(self.style.SUCCESS(' Done'))
