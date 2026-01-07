# Architecture Diagrams (Mermaid)

These diagrams reflect the current codebase as implemented in `main/models.py` and `main/views.py`.

Notes on security markings:
- The app does not implement field-level encryption. At-rest encryption depends on database/storage configuration.
- In-transit encryption depends on HTTPS/TLS and SMTP/TLS configuration in deployment.

## Intake Data Model (Submissions + Uploads)

```mermaid
classDiagram
    class IntakeForm {
        +string title
        +string slug
        +text description
        +text success_message
        +text email_recipients
        +bool is_active
        +bool allow_file_uploads
        +datetime created_at
        +datetime updated_at
    }

    class IntakeField {
        +string label
        +string field_name
        +string field_type
        +string placeholder
        +text choices
        +bool is_required
        +int order
        +string help_text
    }

    class IntakeSubmission {
        +datetime submitted_at
        +ip ip_address
        +json data (sensitive)
        +string status
        +string priority
        +datetime first_contacted_at
        +datetime last_contact_at
        +date next_followup_date
        +text admin_notes
        +datetime status_updated_at
    }

    class IntakeFile {
        +file file (sensitive)
        +string original_filename
        +datetime uploaded_at
    }

    class User {
        +string username
        +string email
    }

    IntakeForm "1" --> "many" IntakeField : has fields
    IntakeForm "1" --> "many" IntakeSubmission : receives submissions
    IntakeSubmission "1" --> "many" IntakeFile : stores uploads
    IntakeSubmission "0..1" --> "1" User : assigned_to

    note for IntakeSubmission "At rest: relies on DB encryption. In transit: HTTPS/TLS (assumed)."
    note for IntakeFile "At rest: relies on file storage encryption. In transit: HTTPS/TLS upload (assumed)."
```

## Content + Navigation Data Model

```mermaid
classDiagram
    class Banner {
        +string heading
        +string subheading
        +text description1
        +text description2
        +text description3
        +string button_text
        +string button_link
        +image image
    }

    class Feature {
        +string icon
        +string title
        +text description
    }

    class Post {
        +image image
        +string title
        +text description
        +string button_text
        +url button_link
    }

    class MiniPost {
        +image image
        +text description
    }

    class ContactInfo {
        +email email
        +string phone
        +text address
    }

    class Footer {
        +string copyright
        +url demo_images_link
        +url design_link
    }

    class DynamicPage {
        +string title
        +string slug
        +string template_type
        +text meta_description
        +bool is_published
        +bool show_in_navigation
        +int navigation_order
        +datetime created_at
        +datetime updated_at
    }

    class PageContent {
        +string page
        +string section_type
        +string title
        +text content
        +image image
        +int order
        +bool is_active
    }

    class NavigationItem {
        +string title
        +string url
        +int order
        +bool is_active
        +string icon_class
        +bool opens_new_window
        +datetime created_at
        +datetime updated_at
    }

    class SocialMediaLink {
        +string platform
        +url url
        +bool is_active
        +int order
    }

    DynamicPage "1" --> "many" PageContent : owns sections
    NavigationItem "0..1" --> "many" NavigationItem : parent/children
```

## Intake Form Submission Data Flow

```mermaid
flowchart LR
    user[User Browser] -->|HTTPS POST (assumed TLS)| intake_form[Intake form endpoint]
    intake_form --> validate[Validate required fields + email]
    validate -->|ok| save_submission[Create IntakeSubmission]
    validate -->|error| return_error[Return error message]

    save_submission --> save_files[Create IntakeFile records]
    save_submission --> send_email[Send email notification]

    save_files --> storage[(File storage)]
    save_submission --> db[(Database)]
    send_email --> smtp[SMTP service]

    admin[Admin/Staff] --> admin_ui[Admin UI]
    admin_ui --> db
    admin_ui --> storage

    note_sec[Transport security depends on HTTPS/TLS and SMTP TLS configuration in deployment.]:::note

    classDef note fill:#f5f5f5,stroke:#999,stroke-width:1px,color:#333;
    note_sec -.-> intake_form
    note_sec -.-> smtp
```

## Content Publishing Flow (Dynamic Pages)

```mermaid
flowchart LR
    editor[Admin/Staff] --> admin_ui[Admin UI]
    admin_ui --> create_page[Create/Update DynamicPage]
    admin_ui --> edit_sections[Create/Update PageContent]

    create_page --> db[(Database)]
    edit_sections --> db

    visitor[Site Visitor] --> request_page[Request /{slug}/]
    request_page --> page_view[dynamic_page_view]
    page_view --> db
    page_view --> render[Render template + page sections]
    render --> visitor
```

## Admin Workflow (Intake Review)

```mermaid
flowchart LR
    staff[Admin/Staff] --> admin_login[Admin Login]
    admin_login --> intake_list[View Intake Submissions]
    intake_list --> view_submission[Open Submission Detail]
    view_submission --> update_status[Update Status/Priority]
    view_submission --> assign_user[Assign Staff Owner]
    view_submission --> add_notes[Add Admin Notes]

    update_status --> db[(Database)]
    assign_user --> db
    add_notes --> db
```

## Navigation Rendering Flow (Sidebar)

```mermaid
flowchart LR
    request[Page Request] --> context_proc[context_processors]
    context_proc --> nav_items[Fetch NavigationItem tree]
    context_proc --> dyn_pages[Fetch DynamicPage (show_in_navigation)]
    nav_items --> render_menu[Render base.html menu]
    dyn_pages --> render_menu
    render_menu --> response[HTML Response]
```

## Email Notification Path (Intake Submission)

```mermaid
flowchart LR
    submission[Create IntakeSubmission] --> build_email[Build EmailMessage]
    build_email --> attach_files[Attach Uploaded Files]
    attach_files --> smtp[SMTP Server]
    smtp --> recipients[Email Recipients]

    note_email[Delivery and TLS depend on SMTP configuration.]:::note
    note_email -.-> smtp

    classDef note fill:#f5f5f5,stroke:#999,stroke-width:1px,color:#333;
```
