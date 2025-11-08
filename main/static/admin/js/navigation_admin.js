// Navigation Admin JavaScript
// Enhances the NavigationItem admin interface

document.addEventListener('DOMContentLoaded', function() {
    const pageUrlField = document.getElementById('id_page_url');
    const titleField = document.getElementById('id_title');

    // Only run enhanced UI for add form (when page_url field exists)
    if (!pageUrlField) {
        console.log('Navigation Admin: Edit mode - using simple form');
        return;
    }

    // Set up the "Add New Page" button
    setupAddNewPageButton();

    if (!urlChoiceField || !customUrlField) return;

    // Function to toggle field states
    function toggleFields() {
        if (urlChoiceField.value && urlChoiceField.value !== '') {
            // If a page is selected, disable custom URL and auto-fill title
            customUrlField.disabled = true;
            customUrlField.style.opacity = '0.5';
            customUrlField.required = false;

            // Auto-fill title if empty
            if (!titleField.value && urlChoiceField.options[urlChoiceField.selectedIndex]) {
                const selectedText = urlChoiceField.options[urlChoiceField.selectedIndex].text;
                if (selectedText !== '-- Select a page --') {
                    // Extract title from "Dynamic Page: Title" or "Intake Form: Title" format
                    let suggestedTitle = selectedText;
                    if (selectedText.includes(': ')) {
                        suggestedTitle = selectedText.split(': ')[1];
                    }
                    titleField.value = suggestedTitle;
                }
            }
        } else {
            // If no page selected, enable custom URL
            customUrlField.disabled = false;
            customUrlField.style.opacity = '1';
        }
    }

    // Function to clear other field when one is filled
    function handleUrlChoiceChange() {
        if (urlChoiceField.value && urlChoiceField.value !== '') {
            customUrlField.value = '';
        }
        toggleFields();
    }

    function handleCustomUrlChange() {
        if (customUrlField.value) {
            urlChoiceField.value = '';
        }
        toggleFields();
    }

    // Add event listeners
    urlChoiceField.addEventListener('change', handleUrlChoiceChange);
    customUrlField.addEventListener('input', handleCustomUrlChange);

    // Initial state
    toggleFields();

    // Add helpful styling
    const fieldset = urlChoiceField.closest('fieldset');
    if (fieldset) {
        // Add quick action buttons
        const quickActions = document.createElement('div');
        quickActions.style.marginTop = '10px';
        quickActions.style.padding = '10px';
        quickActions.style.backgroundColor = '#f8f9fa';
        quickActions.style.border = '1px solid #dee2e6';
        quickActions.style.borderRadius = '4px';

        quickActions.innerHTML = `
            <strong>Quick Actions:</strong>
            <button type="button" onclick="fillDropdownMenu()" style="margin-left: 10px;">Create Dropdown Menu</button>
            <button type="button" onclick="fillContactPage()" style="margin-left: 5px;">Contact Page</button>
            <button type="button" onclick="fillAboutPage()" style="margin-left: 5px;">About Page</button>
        `;

        // Insert after the custom_url field
        const customUrlRow = customUrlField.closest('.form-row') || customUrlField.closest('div');
        if (customUrlRow && customUrlRow.nextSibling) {
            customUrlRow.parentNode.insertBefore(quickActions, customUrlRow.nextSibling);
        }
    }
});

// Quick action functions
function fillDropdownMenu() {
    const titleField = document.getElementById('id_title');
    const customUrlField = document.getElementById('id_custom_url');
    const urlChoiceField = document.getElementById('id_url_choice');

    titleField.value = 'Services'; // Example dropdown title
    customUrlField.value = '#';
    urlChoiceField.value = '';
}

function fillContactPage() {
    const titleField = document.getElementById('id_title');
    const customUrlField = document.getElementById('id_custom_url');
    const urlChoiceField = document.getElementById('id_url_choice');

    titleField.value = 'Contact';
    customUrlField.value = '/contact/';
    urlChoiceField.value = '';
}

function fillAboutPage() {
    const titleField = document.getElementById('id_title');
    const customUrlField = document.getElementById('id_custom_url');
    const urlChoiceField = document.getElementById('id_url_choice');

    titleField.value = 'About Us';
    customUrlField.value = '/about/';
    urlChoiceField.value = '';
}
