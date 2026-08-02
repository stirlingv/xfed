# Intake Form System Documentation

## Overview

The Intake Form system allows you to create multiple, fully customizable intake forms through the Django admin interface. Each form can have different fields and validation rules; every submission triggers a Slack notification.

## Features

### ✅ **Multiple Forms**
- Create unlimited intake forms for different purposes
- Each form has its own URL: `/intake/form-name/`
- Separate configuration and submissions for each form

### ✅ **Configurable Fields**
- **Text Input**: Single-line text fields
- **Email**: Email validation with proper input type
- **Phone**: Phone number fields with tel input type
- **Textarea**: Multi-line text for longer responses
- **Select Dropdown**: Choose from predefined options
- **Radio Buttons**: Single choice from multiple options
- **Checkboxes**: Yes/no or agreement fields
- **File Upload**: Allow document/image uploads

### ✅ **Field Customization**
- Required/Optional field settings
- Custom labels and placeholder text
- Help text for user guidance
- Display order control
- Validation rules

### ✅ **Slack Notifications**
- Automatic Slack alert for every submission
- Includes all submitted data and a link to the submission in the admin
- High-priority forms (consultation, network applications, contact) can @-mention the channel
- Custom success messages

### ✅ **File Upload Support**
- Multiple file upload capability
- File size validation (10MB max per file)
- Secure file storage
- File names listed in Slack notifications; files reviewed via the admin

## How to Use

### Creating Your First Intake Form

1. **Access Admin Panel**
   - Go to `/admin/`
   - Look for **"Intake Forms"** under MAIN section

2. **Create New Form**
   - Click **"Add Intake Form"**
   - Fill out basic information:
     - **Form Title**: "Client Intake Form"
     - **Form URL**: "client-intake" (creates `/intake/client-intake/`)
     - **Description**: Optional description shown to users
     - **Success Message**: Message shown after submission
     - **Form Active**: Check to make form accessible
     - **Allow File Uploads**: Enable document uploads

3. **Add Form Fields**
   - After saving the form, you'll see **"Form Fields"** section
   - Click **"Add Another Form Field"** to add fields
   - Configure each field:
     - **Label**: What users see
     - **Field Name**: Internal name (no spaces, letters/numbers/underscores only)
     - **Field Type**: Choose from available types
     - **Required**: Check if field must be filled
     - **Display Order**: Control field sequence (0=first, 1=second, etc.)

## Example: Client Intake Form

### Form Configuration:
```
Title: Client Intake Form
URL: client-intake
Description: Please fill out this form to help us understand your needs...
```

### Form Fields:
```
Order 0: First Name (text, required)
Order 1: Last Name (text, required)
Order 2: Email (email, required)
Order 3: Phone (phone, required)
Order 4: Service Needed (select, required)
  Options: Tax Preparation, Business Services, Consulting, Other
Order 5: Contact Method (radio, optional)
  Options: Phone, Email, Text
Order 6: Comments (textarea, optional)
```

## Field Types Explained

### **Text Input**
- Single-line text entry
- Good for: Names, addresses, short answers
- Validation: None (accepts any text)

### **Email**
- Email address with validation
- Good for: Contact emails
- Validation: Must be valid email format

### **Phone**
- Phone number input
- Good for: Contact numbers
- Validation: None (accepts any format)

### **Textarea**
- Multi-line text area
- Good for: Comments, descriptions, detailed questions
- Validation: None

### **Select Dropdown**
- Single choice from dropdown list
- Good for: Service types, categories, states
- Configuration: Add choices one per line in "Choices" field

### **Radio Buttons**
- Single choice displayed as radio buttons
- Good for: Preferences, yes/no questions
- Configuration: Add choices one per line in "Choices" field

### **Checkbox**
- Single checkbox for yes/no
- Good for: Agreements, opt-ins, confirmations
- Value: Stores "yes" when checked, nothing when unchecked

### **File Upload**
- File upload capability
- Good for: Documents, images, contracts
- Features: Multiple files, 10MB limit per file, reviewed in admin

## Multiple Forms Examples

### 1. **Client Intake Form** (`/intake/client-intake/`)
- Basic contact info
- Service needs assessment
- Document upload for existing clients

### 2. **Job Application Form** (`/intake/job-application/`)
- Personal information
- Experience details
- Resume upload
- References

### 3. **Service Request Form** (`/intake/service-request/`)
- Contact details
- Service type selection
- Urgent vs. standard processing
- Supporting documents

### 4. **Consultation Request** (`/intake/consultation/`)
- Basic info
- Preferred meeting times
- Topics to discuss
- Background documents

## Admin Management

### **Intake Forms Admin**
- View all forms and their status
- Enable/disable forms quickly
- See submission counts
- Edit form settings

### **Form Fields Admin**
- Manage all fields across all forms
- Reorder fields easily
- See which forms use which field types
- Bulk edit field properties

### **Form Submissions Admin**
- View all submissions by form
- See submission data and timestamps
- Download uploaded files
- Track submission trends

### **Uploaded Files Admin**
- Manage all uploaded files
- See file sizes and types
- Download files for review
- Clean up old uploads

## Integration with Dynamic Pages

### **Intake Template Type**
- You can create Dynamic Pages that use the "Intake Form Template"
- This allows you to create custom landing pages that lead to intake forms
- Combine with PageContent to create rich introduction pages

### **Navigation Integration**
- Intake forms automatically appear in navigation if enabled
- Create menu items that link directly to intake forms
- Use Dynamic Pages for marketing, intake forms for data collection

## Slack Notification Configuration

Set these environment variables in your deployment:

```
ENABLE_SLACK_NOTIFICATIONS=true            # on by default
SLACK_CONTACT_WEBHOOK_URL=<webhook url>    # #xfed-contact-us: contact form messages
SLACK_INTAKE_WEBHOOK_URL=<webhook url>     # channel for all other form alerts
SLACK_WEBHOOK_URL=<webhook url>            # fallback (also used for deploy alerts)
SLACK_NOTIFICATION_MENTION=<!here>         # optional @-mention for priority forms
OWNER_NOTIFICATION_FORM_SLUGS=join-our-team,client-consultation,contact-us
SITE_BASE_URL=https://hirexfed.com         # used for admin links in alerts
```

Routing: the `contact-us` form posts to `SLACK_CONTACT_WEBHOOK_URL`; every
other form posts to `SLACK_INTAKE_WEBHOOK_URL`. Each level falls back to the
next (`SLACK_CONTACT_WEBHOOK_URL` → `SLACK_INTAKE_WEBHOOK_URL` →
`SLACK_WEBHOOK_URL`), so alerts are never dropped just because a dedicated
channel webhook is missing.

### **Slack Alert Content Includes**:
- Form name and submission ID
- All submitted field data
- Names of any uploaded files
- Direct link to the submission in the Django admin

## Security Features

### ✅ **Data Protection**
- CSRF protection on all forms
- File type validation
- File size limits
- IP address logging
- Secure file storage

### ✅ **Spam Prevention**
- Built-in Django protection
- Rate limiting ready (can be added)
- Validation on all fields
- Required field enforcement

## Getting Started Checklist

1. ✅ **Run migrations** to create database tables
2. ✅ **Create your first form** in admin
3. ✅ **Add form fields** (start with basic contact info)
4. ✅ **Test the form** by visiting `/intake/your-form-slug/`
5. ✅ **Configure the Slack webhook** environment variables
6. ✅ **Add navigation links** to your forms

## Next Steps

- **Customize styling**: Modify `intake.html` template
- **Add more field types**: Extend the system with custom fields
- **Integration**: Connect with CRM systems or databases
- **Analytics**: Track form performance and conversion rates
- **Automation**: Set up automated responses and workflows

The intake system is now ready for production use and will grow with your business needs!
