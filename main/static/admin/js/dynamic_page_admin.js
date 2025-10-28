// Dynamic Page Admin JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Auto-populate slug from title
    var titleField = document.querySelector('#id_title');
    var slugField = document.querySelector('#id_slug');
    
    if (titleField && slugField && !slugField.value) {
        titleField.addEventListener('input', function() {
            var slug = titleField.value
                .toLowerCase()
                .replace(/[^a-z0-9\s-]/g, '') // Remove special characters
                .replace(/\s+/g, '-') // Replace spaces with hyphens
                .replace(/-+/g, '-') // Replace multiple hyphens with single
                .replace(/^-|-$/g, ''); // Remove leading/trailing hyphens
            
            slugField.value = slug;
        });
    }
    
    // Template type change handler
    var templateField = document.querySelector('#id_template_type');
    if (templateField) {
        templateField.addEventListener('change', function() {
            var helpTexts = {
                'generic': 'Simple page layout perfect for about pages, contact info, and basic content.',
                'elements': 'Feature-rich layout with forms, tables, buttons, and interactive elements.',
                'index': 'Homepage-style layout with banner, features grid, and posts sections.'
            };
            
            var helpDiv = templateField.parentElement.querySelector('.template-help');
            if (!helpDiv) {
                helpDiv = document.createElement('div');
                helpDiv.className = 'template-help';
                helpDiv.style.cssText = 'margin-top: 8px; padding: 8px; background: #e8f4fd; border-radius: 4px; font-size: 12px; color: #31708f;';
                templateField.parentElement.appendChild(helpDiv);
            }
            
            helpDiv.textContent = helpTexts[templateField.value] || '';
        });
        
        // Trigger on page load
        templateField.dispatchEvent(new Event('change'));
    }
    
    // Add save and continue editing success message
    if (window.location.search.includes('page__exact=')) {
        var changeForm = document.querySelector('#changelist-form');
        if (changeForm) {
            var message = document.createElement('div');
            message.className = 'success-message';
            message.innerHTML = '<strong>Success!</strong> Your page has been created. You can now add content sections below.';
            changeForm.parentElement.insertBefore(message, changeForm);
        }
    }
});