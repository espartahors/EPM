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

// Enhanced Equipment Tree View
function initializeEquipmentTree() {
    $('#equipment-tree').jstree({
        'core': {
            'themes': {
                'name': 'proton',
                'responsive': true
            },
            'data': {
                'url': function(node) {
                    return node.id === '#' ?
                        '/equipment/api/tree/' :
                        '/equipment/api/tree/' + node.id + '/';
                },
                'data': function(node) {
                    return {'id': node.id};
                }
            }
        },
        'plugins': ['wholerow', 'types', 'state', 'contextmenu'],
        'types': {
            'default': {
                'icon': 'fas fa-cog'
            },
            'active': {
                'icon': 'fas fa-cog text-success'
            },
            'maintenance': {
                'icon': 'fas fa-wrench text-warning'
            },
            'inactive': {
                'icon': 'fas fa-cog text-secondary'
            },
            'retired': {
                'icon': 'fas fa-cog text-danger'
            }
        },
        'contextmenu': {
            'items': customMenuItems
        }
    }).on('select_node.jstree', function(e, data) {
        loadEquipmentDetails(data.node.id);
    });
}

// Define custom context menu items
function customMenuItems(node) {
    return {
        'view': {
            'label': 'View Details',
            'action': function() {
                loadEquipmentDetails(node.id);
            },
            'icon': 'fas fa-eye'
        },
        'drawings': {
            'label': 'View Drawings',
            'action': function() {
                window.location.href = '/equipment/' + node.id + '/drawings/';
            },
            'icon': 'fas fa-file-image'
        },
        'parts': {
            'label': 'View Parts',
            'action': function() {
                window.location.href = '/equipment/' + node.id + '/parts/';
            },
            'icon': 'fas fa-tools'
        }
    };
}

// Load equipment details via AJAX
function loadEquipmentDetails(equipmentId) {
    $('#detail-panel').html('<div class="text-center my-5"><i class="fas fa-spinner fa-spin fa-3x"></i><p class="mt-3">Loading details...</p></div>');
    
    $.ajax({
        url: '/equipment/' + equipmentId + '/details/',
        type: 'GET',
        success: function(data) {
            $('#detail-panel').html(data);
            initDetailPanelFunctions();
        },
        error: function() {
            $('#detail-panel').html('<div class="alert alert-danger">Error loading equipment details</div>');
        }
    });
}

// Initialize all functions when document is ready
$(document).ready(function() {
    if ($('#equipment-tree').length) {
        initializeEquipmentTree();
    }
});