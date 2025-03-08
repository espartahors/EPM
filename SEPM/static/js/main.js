/**
 * Equipment & Parts Management System main JavaScript
 */

// Toggle all checkboxes in a table
function toggleAllCheckboxes(source, name) {
    const checkboxes = document.getElementsByName(name);
    for (let i = 0; i < checkboxes.length; i++) {
        checkboxes[i].checked = source.checked;
    }
}

// Initialize tooltips and popovers
document.addEventListener('DOMContentLoaded', function() {
    // Enable tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Enable popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Add active class to nav links based on current page
    const currentLocation = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentLocation) {
            link.classList.add('active');
            
            // If it's in a dropdown, also mark the parent dropdown as active
            const dropdown = link.closest('.dropdown');
            if (dropdown) {
                const dropdownToggle = dropdown.querySelector('.dropdown-toggle');
                if (dropdownToggle) {
                    dropdownToggle.classList.add('active');
                }
            }
        }
    });
});

// Confirm delete
function confirmDelete(message) {
    return confirm(message || 'Are you sure you want to delete this item?');
}

// Handle form submission with file uploads
function handleFormSubmit(formId, submitBtnId) {
    const form = document.getElementById(formId);
    const submitBtn = document.getElementById(submitBtnId);
    
    if (form && submitBtn) {
        submitBtn.addEventListener('click', function() {
            // Disable the button to prevent multiple submissions
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i> Processing...';
            
            // Submit the form
            form.submit();
        });
    }
}