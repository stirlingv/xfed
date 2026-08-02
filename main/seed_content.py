"""Seed content for the 8(a) / small business set-aside pivot.

Pure data — no model imports — so both the setup_hirexfed_content management
command and content migrations can share one source of truth. HireXFed's
primary audience is owners of 8(a) and other set-aside small businesses;
general tax help remains available but secondary.
"""

PIVOT_BANNER = {
    'heading': "8(a) Tax Experts",
    'subheading': "Former IRS Pros, On Your Side",
    'description1': (
        "Your 8(a) certification depends on clean records, not just a happy "
        "IRS. We keep your returns and books SBA-review-ready."
    ),
    'description2': (
        "SBA reviews are intensifying, and firms without clean records are "
        "losing certifications. Don't be one of them."
    ),
    'description3': (
        "<strong>General tax questions? Always welcome.</strong> "
        "<a href='/intake/client-consultation/'>Request a free consultation</a> "
        "— we reply within 24 hours."
    ),
    'button_text': "Get 8(a) Tax Help",
    'button_link': "/intake/client-consultation/",
}

# Feature icons must come from Feature.ICON_CHOICES.
PIVOT_FEATURES = [
    {
        'icon': 'fa-landmark',
        'title': '8(a) & SBA Compliance',
        'description': (
            'Keep your certification safe. We prepare the tax returns and '
            'financial statements the SBA expects at annual review, and help '
            'you respond quickly to document demands and continuing-eligibility '
            'checks.'
        ),
    },
    {
        'icon': 'fa-file-invoice-dollar',
        'title': 'Contractor Tax Prep & Planning',
        'description': (
            'Business and personal returns for government contractors — entity '
            'structure, estimated taxes on contract revenue, and multi-state '
            'filings handled by former IRS professionals.'
        ),
    },
    {
        'icon': 'fa-balance-scale',
        'title': 'IRS Audits & Problem Resolution',
        'description': (
            'Audits, back taxes, liens, and levies. Our former IRS agents have '
            'sat on the other side of the table — now they put that experience '
            'to work representing you.'
        ),
    },
    {
        'icon': 'fa-check-circle',
        'title': 'Set-Aside Certification Guidance',
        'description': (
            'Considering 8(a), SDVOSB, WOSB, or HUBZone status? Get an honest '
            'read on eligibility and the tax and financial records you will '
            'need before you apply.'
        ),
    },
]

# Old homepage feature tiles superseded by the pivot.
RETIRED_FEATURE_TITLES = [
    'Income Taxes (IRS)',
    'Social Security (SSA)',
    'Data Systems',
    'IT Systems',
]

PIVOT_POSTS = [
    {
        'title': 'SBA Suspended Over 1,000 8(a) Firms — Are You Audit-Ready?',
        'description': (
            'In late 2025 the SBA ordered every 8(a) participant to produce '
            'three years of financial documents, then suspended more than a '
            'thousand firms that could not comply. Learn what to keep ready so '
            'your certification is never at risk.'
        ),
        'button_text': 'Protect Your Certification',
        'button_link': '/8a-tax-help/',
    },
    {
        'title': 'The 8(a) Annual Review: Tax Documents You Need',
        'description': (
            'Every year the SBA expects business tax returns, personal returns '
            'for disadvantaged owners, and current financial statements. Use '
            'our checklist to walk into your annual review prepared.'
        ),
        'button_text': 'Get the Checklist',
        'button_link': '/8a-annual-review-tax-checklist/',
    },
    {
        'title': 'Why Your Tax Return Matters to Your SBA Certification',
        'description': (
            'Federal tax compliance is a condition of 8(a) eligibility. Unfiled '
            'returns, unpaid balances, and sloppy books can cost you contracts '
            'long before the IRS comes calling.'
        ),
        'button_text': 'Learn More',
        'button_link': '/8a-tax-help/',
    },
    {
        'title': 'Entity Structure for Government Contractors',
        'description': (
            'S-corp, C-corp, or LLC? For set-aside owners the answer affects '
            'ownership and control rules, size standards, and your tax bill. '
            'Get it right before it limits your certification.'
        ),
        'button_text': 'Ask an Expert',
        'button_link': '/intake/client-consultation/',
    },
    {
        'title': 'What To Do When You Receive an IRS Notice',
        'description': (
            'Receiving mail from the IRS can be stressful. Learn the first '
            'steps you should take and how to respond appropriately to protect '
            'your interests — and your contracts.'
        ),
        'button_text': 'Read More',
        'button_link': '/services/',
    },
    {
        'title': 'Why Hire a Former IRS Agent?',
        'description': (
            'When facing tax issues, insider knowledge matters. Discover the '
            'advantages of working with someone who has been on the other side.'
        ),
        'button_text': 'Find Out',
        'button_link': '/about/',
    },
]

RETIRED_POST_TITLES = [
    'Understanding Offers in Compromise',
    'Tax Liens vs. Tax Levies: Know the Difference',
    'Common Tax Filing Mistakes to Avoid',
    'Year-Round Tax Planning Tips',
]

PIVOT_MINI_POSTS = [
    {
        'description': (
            '📋 8(a) participants: SBA financial reviews are ongoing. Is your '
            'three-year tax and financial package ready to produce on demand?'
        ),
    },
    {
        'description': (
            '🆕 Now serving 8(a) and set-aside small businesses nationwide — '
            'contractor tax prep, SBA review support, and IRS representation.'
        ),
    },
    {
        'description': (
            '💡 Did you know? Federal tax compliance is a condition of 8(a) '
            'eligibility. One missed filing can jeopardize your certification.'
        ),
    },
]

RETIRED_MINI_POST_SNIPPETS = [
    'Tax Season 2025',
    'audit representation',
    'penalty abatement',
]

PAGE_8A_TAX_HELP = {
    'slug': '8a-tax-help',
    'title': '8(a) & Set-Aside Tax Help',
    'meta_description': (
        'Tax preparation, SBA annual review support, and IRS representation '
        'for 8(a) and small business set-aside owners, from former IRS '
        'professionals.'
    ),
    'content_title': 'Tax Help Built for 8(a) & Set-Aside Small Businesses',
    'content': '''<p class="lead">Your customer is the federal government. Your tax team should know how the government works.</p>

<p>Owners of 8(a) and other set-aside small businesses live under two sets of rules at once: the IRS's and the SBA's. Your tax returns, financial statements, and payroll filings are not just compliance paperwork — they are evidence the SBA uses to decide whether you keep your certification, your contracts, and your pipeline.</p>

<h3>Why This Matters Right Now</h3>
<p>The SBA has dramatically tightened oversight of the 8(a) program. In late 2025 it ordered every 8(a) participant — about 4,300 firms — to produce three years of financial documents, and in early 2026 it suspended more than 1,000 firms that failed to respond. Admissions standards have tightened as well. For set-aside owners, clean and current tax records have never mattered more.</p>

<h3>How We Help</h3>
<ul>
    <li><strong>8(a) &amp; SBA compliance:</strong> annual review packages, responses to SBA document demands, and continuing-eligibility support built on accurate returns and financial statements.</li>
    <li><strong>Contractor tax preparation &amp; planning:</strong> business returns (1120, 1120-S, 1065) and the personal returns the SBA reviews for disadvantaged owners, plus estimated tax planning for lumpy contract revenue.</li>
    <li><strong>IRS audits &amp; problem resolution:</strong> audit representation, back taxes, liens, and levies — handled by former IRS agents who know exactly how the process works from the inside.</li>
    <li><strong>Certification guidance:</strong> an honest, experienced read on 8(a) and other set-aside eligibility and the financial records you will need before you apply.</li>
</ul>

<h3>Why HireXFed</h3>
<p>Our network is built from former IRS professionals with decades of federal service. We have examined returns, worked collections, and administered the rules you now have to satisfy. That insider perspective — applied to your side of the table — is the difference between guessing what the government wants and knowing.</p>

<p style="margin-top: 2em;">
    <a href="/intake/client-consultation/" class="button primary large">Request a Free Consultation</a>
    <a href="/8a-annual-review-tax-checklist/" class="button" style="margin-left: 1em;">Annual Review Checklist</a>
</p>''',
}

PAGE_8A_CHECKLIST = {
    'slug': '8a-annual-review-tax-checklist',
    'title': '8(a) Annual Review: Tax & Financial Document Checklist',
    'meta_description': (
        'Checklist of the tax returns and financial documents 8(a) small '
        'businesses need for SBA annual reviews and document requests.'
    ),
    'content_title': 'Be Ready Before the SBA Asks',
    'content': '''<p class="lead">The SBA can ask for years of records with little warning. Firms that could not produce them have lost their 8(a) status.</p>

<p>Use this checklist to keep an "SBA-ready" package current at all times. Requirements vary by firm and change over time — always confirm the current list with the SBA or your representative.</p>

<h3>Business Tax &amp; Financial Records</h3>
<ul>
    <li>Business federal income tax returns — most recent three years, as filed, with all schedules</li>
    <li>Year-end financial statements (balance sheet and profit &amp; loss) for the same period</li>
    <li>Interim financial statements, current within 90 days, for reviews and size determinations</li>
    <li>Payroll tax filings (Forms 941/940) and proof of deposits</li>
    <li>Proof of federal estimated tax payments</li>
</ul>

<h3>Owner Records (Disadvantaged Individual)</h3>
<ul>
    <li>Personal federal income tax returns — most recent three years, with W-2s and all schedules</li>
    <li>Personal financial statement (SBA Form 413), updated annually</li>
    <li>Documentation of salary and any distributions taken from the firm</li>
</ul>

<h3>Compliance Status</h3>
<ul>
    <li>All federal tax filings current — business and personal (a condition of continuing eligibility)</li>
    <li>No unresolved federal tax delinquencies, or a compliant payment arrangement in place</li>
    <li>Books reconciled so financial statements tie to the returns the SBA will compare them against</li>
</ul>

<h3>Behind on Any of This?</h3>
<p>That's exactly what we do. Our former IRS professionals rebuild books, catch up unfiled returns, resolve balances, and assemble review-ready packages — before the SBA asks.</p>

<p style="margin-top: 2em;">
    <a href="/intake/client-consultation/" class="button primary large">Get Help With Your Package</a>
</p>''',
}

NAV_8A_ITEM = {
    'title': '8(a) Tax Help',
    'url': '/8a-tax-help/',
    'order': 15,
}

CONSULTATION_PIVOT = {
    'description': (
        'Tell us about your tax situation and one of our former IRS experts '
        'will contact you within 24 hours. We specialize in 8(a) and small '
        'business set-aside owners — and all tax questions are welcome. '
        'Everything you share is kept strictly confidential.'
    ),
    'issue_type_choices': (
        '8(a) / SBA Annual Review or Document Request\n'
        'Government Contractor Tax Compliance\n'
        'IRS Audit or Examination\n'
        'Back Taxes / Unfiled Returns\n'
        'Tax Liens or Levies\n'
        'Offer in Compromise\n'
        'Payment Plan / Installment Agreement\n'
        'Business Tax Issues\n'
        'Tax Planning\n'
        'Other Tax Matter'
    ),
}
