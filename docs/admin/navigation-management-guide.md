# Navigation Management Guide

This guide explains how to manage your website's navigation menu through the Django admin interface.

## Overview

Your website now has a powerful, admin-configurable navigation system that allows you to:

- Create main menu items and dropdown submenus
- Control menu item order and visibility
- Add icons to menu items
- Manage social media links in the header
- Set up links that open in new windows

## Getting Started

### 1. After Migration Setup

After running your migrations, you can set up initial navigation in two ways:

**Option A: Using Management Command**
```bash
python manage.py create_default_navigation
```

**Option B: Using Fixtures**
```bash
python manage.py loaddata fixtures/navigation.json
```

### 2. Accessing Navigation Admin

1. Log into your Django admin at `/admin/`
2. Look for the "Navigation Items" and "Social Media Links" sections
3. Click on either to start managing your navigation

## Managing Navigation Items

### Creating Main Menu Items

1. Go to **Admin → Navigation Items → Add Navigation Item**
2. Fill in:
   - **Menu Title**: What appears in the menu (e.g., "Services")
   - **Link URL**: Where it goes (e.g., "/services/" or "#" for dropdown-only)
   - **Parent Menu Item**: Leave blank for main menu items
   - **Display Order**: Use 10, 20, 30... to leave room for reordering
   - **Icon Class**: Optional Font Awesome icon (e.g., "fa-briefcase")

### Creating Dropdown Submenus

1. First create the parent menu item with URL "#"
2. Then create child items:
   - Set **Parent Menu Item** to your dropdown parent
   - Use **Display Order** to control submenu order
   - Give each child a specific URL

### Example Menu Structure

```
Homepage (/) - Order 10
Services (#) - Order 20
  ├── Tax Preparation (/services/tax-preparation/) - Order 10
  ├── Financial Planning (/services/financial-planning/) - Order 20
  └── Business Consulting (/services/business-consulting/) - Order 30
About Us (/about/) - Order 30
Resources (#) - Order 40
  ├── Tax Documents (/resources/documents/) - Order 10
  └── Forms & Checklists (/resources/forms/) - Order 20
Contact (/contact/) - Order 50
```

## Managing Social Media Links

### Adding Social Media Icons

1. Go to **Admin → Social Media Links → Add Social Media Link**
2. Choose from available platforms:
   - Facebook, Twitter, Instagram, LinkedIn
   - YouTube, Snapchat, Medium, GitHub, Email
3. Enter the full URL to your profile
4. Set display order (lower numbers appear first)

### Social Media Best Practices

- Use full URLs: `https://facebook.com/yourcompany`
- Test links to ensure they work
- For email, use: `mailto:contact@yourcompany.com`
- Use order values like 10, 20, 30 for easy reordering

## Dynamic Pages Integration

Dynamic pages you create can automatically appear in navigation:

1. When creating a Dynamic Page, check "Show in Navigation"
2. Set the "Navigation Order" to control placement
3. The page will appear in the main menu automatically

## Advanced Features

### Icons

Use Font Awesome icon classes:
- `fa-home` - House icon
- `fa-briefcase` - Briefcase for services
- `fa-envelope` - Envelope for contact
- `fa-users` - People for about us
- `fa-folder-open` - Folder for resources

### Opening Links in New Windows

Check "Open in New Window" for:
- External links
- Client portals
- Document downloads
- Third-party tools

### Temporarily Hiding Items

Uncheck "Active" to temporarily hide menu items without deleting them.

## Deployment Workflow

### Local Development

1. Make changes in Django admin
2. Export changes to fixtures:
   ```bash
   python manage.py dumpdata main.NavigationItem main.SocialMediaLink --indent 2 > fixtures/navigation.json
   ```
3. Commit the fixture file:
   ```bash
   git add fixtures/navigation.json
   git commit -m "Update navigation menu"
   ```

### Production Deployment

1. Push changes to your repository
2. Render will run the build script
3. Uncomment this line in `build.sh`:
   ```bash
   python manage.py loaddata fixtures/navigation.json
   ```

## Troubleshooting

### Navigation Not Appearing

1. Check that items have `is_active = True`
2. Verify the context processor is working
3. Make sure migrations have been run

### Dropdown Not Working

1. Ensure parent item has `url = "#"`
2. Check that child items have the correct parent set
3. Verify JavaScript files are loading

### Icons Not Showing

1. Confirm Font Awesome CSS is loaded
2. Check icon class spelling (should start with "fa-")
3. Test with common icons like "fa-home" first

## Tips for Content Managers

1. **Use Consistent Ordering**: Space out order numbers (10, 20, 30) so you can insert items later
2. **Test Links**: Always verify URLs work correctly
3. **Mobile Friendly**: Keep menu titles short for mobile devices
4. **Logical Grouping**: Group related items under dropdown menus
5. **Regular Updates**: Review and update social media links periodically

## Support

- Check the admin interface help text for field-specific guidance
- Use the management command to reset to defaults if needed
- Refer to the main documentation for technical implementation details
