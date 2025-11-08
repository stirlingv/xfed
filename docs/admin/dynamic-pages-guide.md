# Dynamic Page Creation System

This system allows non-technical users to create new static pages through the Django admin interface.

## How to Create a New Page

### Step 1: Access the Admin Panel
1. Go to your website's admin panel: `/admin/`
2. Log in with your admin credentials
3. Look for **"Custom Pages"** under the **MAIN** section

### Step 2: Create a New Page
1. Click **"Add Custom Page"**
2. Fill out the page information:
   - **Page Title**: The title that appears in browser tabs and page headers
   - **Page URL**: The web address for your page (auto-generated from title, but you can edit it)
   - **Page Template**: Choose the layout style:
     - **Generic Template**: Simple layout for basic content pages
     - **Elements Template**: Feature-rich layout with forms, tables, etc.
     - **Homepage Template**: Banner + features + posts layout

### Step 3: Configure Page Settings
- **SEO Description**: Brief description for search engines (optional but recommended)
- **Publish Page**: Check to make the page visible on your website
- **Show in Main Navigation**: Check to add this page to your main menu
- **Navigation Order**: Control the order in the navigation menu (lower numbers appear first)

### Step 4: Add Content
After saving your page, you'll be redirected to add content sections:

1. Click **"Add Page Section"** to create content blocks
2. Choose the section type:
   - **Page Header**: Main page heading and intro
   - **Main Content**: Primary page content
   - **Sidebar**: Additional information or navigation
   - **Footer Content**: Bottom page content

3. For each section, provide:
   - **Title**: Section heading
   - **Content**: Your text content (HTML formatting allowed)
   - **Image**: Optional image for the section
   - **Display Order**: Control the order sections appear

## Template Types Explained

### Generic Template
- Perfect for: About pages, contact info, service descriptions
- Layout: Simple header and content area
- Best for: Text-heavy pages with minimal design elements

### Elements Template
- Perfect for: Feature showcases, service pages, interactive content
- Layout: Flexible sections with support for forms, tables, buttons
- Best for: Pages that need rich design elements

### Homepage Template
- Perfect for: Landing pages, service overviews
- Layout: Banner section, features grid, posts/news section
- Best for: Pages that need to showcase multiple elements

## Managing Your Pages

### Editing Existing Pages
1. Go to **Admin Panel > Custom Pages**
2. Click on the page you want to edit
3. Make your changes and click **Save**

### Managing Page Content
1. Go to **Admin Panel > Page Sections**
2. Filter by your page name to see all content sections
3. Edit, reorder, or add new sections as needed

### Publishing/Unpublishing Pages
- Uncheck **"Publish Page"** to temporarily hide a page
- Check **"Show in Main Navigation"** to add/remove from menu
- Use **"Navigation Order"** to control menu positioning

## Tips for Non-Technical Users

### Creating Good URLs
- Keep URLs short and descriptive
- Use hyphens instead of spaces: `about-us` not `about us`
- Only use letters, numbers, and hyphens
- Avoid special characters like `& % $ @`

### Writing SEO Descriptions
- Keep under 160 characters
- Describe what visitors will find on the page
- Include important keywords naturally

### Organizing Content Sections
- Use **Display Order** to control section sequence
- Start with order 0 for the first section, then 1, 2, etc.
- Use **Page Header** for your main title and intro
- Use **Main Content** for your primary information
- Use **Sidebar** for secondary information or navigation

### HTML Formatting in Content
You can use basic HTML tags in content areas:
- `<p>` for paragraphs
- `<strong>` for bold text
- `<em>` for italic text
- `<a href="URL">` for links
- `<ul><li>` for bullet lists
- `<h3>`, `<h4>` for subheadings

## Troubleshooting

### "Page not found" errors
- Check that **"Publish Page"** is checked
- Verify the URL doesn't conflict with existing pages
- Make sure there are no typos in the page URL

### Page not appearing in navigation
- Check **"Show in Main Navigation"** is enabled
- Verify **"Publish Page"** is enabled
- Check **"Navigation Order"** - higher numbers appear later

### Content not displaying
- Make sure content sections have **"Show on Website"** checked
- Check the **"Display Order"** of your sections
- Verify content is assigned to the correct page

## Need Help?

If you need assistance with creating or managing pages, contact your website administrator. They can help with:
- Complex HTML formatting
- Custom styling requirements
- Advanced page layouts
- Troubleshooting technical issues
