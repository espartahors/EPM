# SEPM Project Improvements

## 1. Security Enhancements

### Move sensitive information to environment variables

```python
# SEPM/SEPM/settings.py - Replace hardcoded credentials with environment variables

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'sepm_db'),
        'USER': os.environ.get('DB_USER', 'sepm_user'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),  # Remove hardcoded password
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
        'OPTIONS': {
            'client_encoding': 'UTF8',
        },
    }
}

# Secret key
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-rh2^y5=p+e7nua3ff7+t=t_@h!m&izwb)tx1z&zd*q#dj@2jl8')

# Set debug based on environment
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
```

### Create a .env file template

```
# .env.example - Template for environment variables
DB_NAME=sepm_db
DB_USER=sepm_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=your_secure_secret_key
DEBUG=False
```

## 2. Frontend Improvements

### Consolidate equipment tree view JavaScript

```javascript
// static/js/equipment-tree.js - Replace redundant tree implementations

/**
 * EquipmentTree - Unified component for equipment tree management
 */
class EquipmentTree {
    constructor(config) {
        this.treeElementId = config.treeElementId || 'equipment-tree';
        this.detailsElementId = config.detailsElementId || 'equipment-details';
        this.emptyDetailsElementId = config.emptyDetailsElementId || 'empty-details';
        this.searchElementId = config.searchElementId || 'equipmentSearch';
        this.baseApiUrl = config.baseApiUrl || '/api/tree/';
        this.baseEquipmentUrl = config.baseEquipmentUrl || '/equipment/';
        this.debug = config.debug || false;
        
        this.initTree();
        this.initSearch();
        this.initButtons();
    }
    
    /**
     * Initialize the equipment tree
     */
    initTree() {
        const self = this;
        
        $(`#${this.treeElementId}`).jstree({
            'core': {
                'themes': {
                    'name': 'proton',
                    'responsive': true
                },
                'data': {
                    'url': (node) => {
                        const url = node.id === '#' ? 
                            this.baseApiUrl : 
                            `${this.baseApiUrl}${node.id}/`;
                        
                        if (this.debug) this.logDebug(`Data URL: ${url}`);
                        return url;
                    },
                    'data': (node) => {
                        if (this.debug) this.logDebug(`Requesting data for node: ${JSON.stringify(node)}`);
                        return {'id': node.id};
                    },
                    'error': (jqXHR, textStatus, errorThrown) => {
                        if (this.debug) this.logDebug(`Error loading data: ${textStatus} - ${errorThrown}`);
                        this.showError(`Error loading tree data: ${errorThrown}`);
                    }
                }
            },
            'plugins': ['wholerow', 'types', 'search', 'state'],
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
            'search': {
                'show_only_matches': true,
                'show_only_matches_children': true
            }
        }).on('select_node.jstree', function(e, data) {
            // Load equipment details when a node is selected
            if (self.debug) self.logDebug(`Node selected: ${data.node.id}`);
            self.loadEquipmentDetails(data.node.id);
        }).on('loaded.jstree', function() {
            if (self.debug) self.logDebug("Tree loaded successfully");
        });
    }
    
    /**
     * Initialize equipment search
     */
    initSearch() {
        const self = this;
        $(`#${this.searchElementId}`).keyup(function() {
            const searchTerm = $(this).val();
            if (self.debug) self.logDebug(`Searching for: ${searchTerm}`);
            $(`#${self.treeElementId}`).jstree('search', searchTerm);
        });
    }
    
    /**
     * Initialize action buttons
     */
    initButtons() {
        const self = this;
        $('.expand-all').click(function() {
            if (self.debug) self.logDebug("Expanding all nodes");
            $(`#${self.treeElementId}`).jstree('open_all');
        });
        
        $('.collapse-all').click(function() {
            if (self.debug) self.logDebug("Collapsing all nodes");
            $(`#${self.treeElementId}`).jstree('close_all');
        });
    }
    
    /**
     * Load equipment details via AJAX
     */
    loadEquipmentDetails(equipmentId) {
        $(`#${this.emptyDetailsElementId}`).hide();
        $(`#${this.detailsElementId}`)
            .html('<div class="text-center py-5"><i class="fas fa-spinner fa-spin fa-3x"></i><p class="mt-2">Loading details...</p></div>')
            .show();
        
        if (this.debug) this.logDebug(`Loading details for equipment ID: ${equipmentId}`);
        $.ajax({
            url: `${this.baseEquipmentUrl}${equipmentId}/`,
            type: 'GET',
            dataType: 'html',
            success: (data) => {
                if (this.debug) this.logDebug("Details loaded successfully");
                $(`#${this.detailsElementId}`).html(data);
            },
            error: (jqXHR, textStatus, errorThrown) => {
                if (this.debug) this.logDebug(`Error loading details: ${textStatus} - ${errorThrown}`);
                this.showError(`Error loading equipment details: ${errorThrown}`);
            }
        });
    }
    
    /**
     * Show error message
     */
    showError(message) {
        $(`#${this.detailsElementId}`).html(`<div class="alert alert-danger">${message}</div>`);
    }
    
    /**
     * Log debug message
     */
    logDebug(message) {
        if (!this.debug) return;
        
        console.log(`[EquipmentTree] ${message}`);
        
        const debugElement = $('#debug-info');
        if (debugElement.length) {
            const timestamp = new Date().toLocaleTimeString();
            debugElement.append(`<div>[${timestamp}] ${message}</div>`);
            debugElement.scrollTop(debugElement[0].scrollHeight);
        }
    }
}

// Initialize equipment tree on document ready
$(document).ready(function() {
    // Only initialize if the tree element exists
    if ($('#equipment-tree').length) {
        window.equipmentTree = new EquipmentTree({
            debug: false  // Set to true only in development
        });
    }
});
```

### Create a new consolidated equipment tree template

```html
<!-- templates/equipment/equipment_tree_view.html -->
{% extends 'base.html' %}
{% load static %}

{% block title %}Equipment Tree | Parts Manager{% endblock %}

{% block extra_css %}
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/jstree@3.3.12/dist/themes/proton/style.min.css">
<style>
    #equipment-tree {
        overflow-y: auto;
        max-height: calc(100vh - 250px);
        background: #f8f9fa;
        border: 1px solid #ddd;
        border-radius: 4px;
        padding: 10px;
    }
    
    .details-panel {
        background-color: #f8f9fa;
        border: 1px solid #ddd;
        border-radius: 4px;
        padding: 20px;
        height: calc(100vh - 250px);
        overflow-y: auto;
    }
    
    /* Search Bar */
    .search-container {
        position: relative;
        margin-bottom: 20px;
    }
    
    .search-icon {
        position: absolute;
        left: 10px;
        top: 10px;
        color: #999;
    }
    
    .search-input {
        padding-left: 35px;
        border-radius: 20px;
    }
</style>
{% endblock %}

{% block content %}
<div class="row mb-3">
    <div class="col-12">
        <h2><i class="fas fa-sitemap me-2"></i> Equipment Hierarchy</h2>
        <p class="text-muted">Browse equipment hierarchy, view details, and manage related parts</p>
    </div>
</div>

{% if not request.user.is_read_only %}
<div class="row mb-3">
    <div class="col-12">
        <div class="card mb-3">
            <div class="card-header bg-light">
                <div class="d-flex justify-content-between align-items-center">
                    <span><i class="fas fa-cog me-2"></i> Equipment Controls</span>
                    <div>
                        <a href="{% url 'equipment-create' %}" class="btn btn-success">
                            <i class="fas fa-plus me-1"></i> Add Equipment
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endif %}

<div class="row">
    <!-- Equipment Tree View -->
    <div class="col-md-4">
        <div class="card mb-3">
            <div class="card-header bg-light">
                <div class="d-flex justify-content-between align-items-center">
                    <span><i class="fas fa-sitemap me-2"></i> Equipment Hierarchy</span>
                    <div>
                        <button class="btn btn-sm btn-outline-secondary expand-all" title="Expand All">
                            <i class="fas fa-expand-arrows-alt"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-secondary collapse-all" title="Collapse All">
                            <i class="fas fa-compress-arrows-alt"></i>
                        </button>
                    </div>
                </div>
            </div>
            <div class="card-body p-0">
                <div class="search-container p-2">
                    <i class="fas fa-search search-icon"></i>
                    <input type="text" class="form-control search-input" id="equipmentSearch" placeholder="Search equipment...">
                </div>
                <div id="equipment-tree"></div>
            </div>
        </div>
    </div>
    
    <!-- Equipment Details Panel -->
    <div class="col-md-8">
        <div class="card details-panel">
            <div class="card-header bg-light">
                <h5 class="mb-0"><i class="fas fa-info-circle me-2"></i> Equipment Details</h5>
            </div>
            <div class="card-body">
                <div class="text-center py-5" id="empty-details">
                    <i class="fas fa-sitemap fa-4x text-muted mb-3"></i>
                    <h4 class="text-muted">Select an equipment from the tree</h4>
                    <p class="text-muted">Equipment details will appear here</p>
                </div>
                <div id="equipment-details" style="display: none;">
                    <!-- Equipment details loaded via AJAX will go here -->
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script src="https://cdn.jsdelivr.net/npm/jstree@3.3.12/dist/jstree.min.js"></script>
<script src="{% static 'js/equipment-tree.js' %}"></script>
{% endblock %}
```

## 3. Complete Missing BOM Import Implementation

```python
# documentation/views.py - Implement BOM import functionality

def process_bom_import(df, import_log):
    """Process BOM import from dataframe"""
    from equipment.models import Equipment, EquipmentPart
    from parts.models import Part
    
    created = 0
    updated = 0
    failed = 0
    errors = []
    
    for index, row in df.iterrows():
        try:
            equipment_code = row.get('equipment_code')
            part_number = row.get('part_number')
            position = row.get('position', '')
            quantity = row.get('quantity', 1)
            notes = row.get('notes', '')
            
            if not equipment_code or not part_number:
                errors.append(f"Row {index+1}: Missing equipment_code or part_number")
                failed += 1
                continue
            
            try:
                equipment = Equipment.objects.get(equipment_code=equipment_code)
            except Equipment.DoesNotExist:
                errors.append(f"Row {index+1}: Equipment {equipment_code} not found")
                failed += 1
                continue
                
            try:
                part = Part.objects.get(part_number=part_number)
            except Part.DoesNotExist:
                errors.append(f"Row {index+1}: Part {part_number} not found")
                failed += 1
                continue
            
            # Check if this equipment-part relationship already exists
            equipment_part, created_flag = EquipmentPart.objects.update_or_create(
                equipment=equipment,
                part=part,
                position=position,
                defaults={
                    'quantity': quantity,
                    'notes': notes
                }
            )
            
            if created_flag:
                created += 1
            else:
                updated += 1
                
        except Exception as e:
            errors.append(f"Row {index+1}: Error - {str(e)}")
            failed += 1
    
    import_log.items_processed = created + updated + failed
    import_log.items_created = created
    import_log.items_updated = updated
    import_log.items_failed = failed
    import_log.log_details = "\n".join(errors)
    import_log.save()
    
    return {'created': created, 'updated': updated, 'failed': failed}
```

## 4. Error Handling Improvements

### Add middleware for global error handling

```python
# SEPM/middleware.py - Add global error handling middleware

import logging
from django.http import HttpResponseServerError
from django.template.response import TemplateResponse

logger = logging.getLogger(__name__)

class GlobalErrorHandlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        # Log the error
        logger.exception(f"Unhandled exception: {str(exception)}")
        
        # Return a custom error response
        context = {
            'error_message': str(exception),
            'error_type': exception.__class__.__name__,
        }
        
        return TemplateResponse(request, 'error.html', context, status=500)
```

### Create a custom error template

```html
<!-- templates/error.html -->
{% extends 'base.html' %}

{% block title %}Error | Parts Manager{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-8">
        <div class="card border-danger">
            <div class="card-header bg-danger text-white">
                <h5 class="mb-0"><i class="fas fa-exclamation-triangle me-2"></i> Error</h5>
            </div>
            <div class="card-body text-center">
                <i class="fas fa-bug fa-4x text-danger mb-3"></i>
                <h4>Oops! Something went wrong.</h4>
                
                <div class="alert alert-danger mt-3">
                    <strong>{{ error_type }}:</strong> {{ error_message }}
                </div>
                
                <p class="mt-3">Please try again or contact your system administrator if the problem persists.</p>
                
                <div class="mt-4">
                    <a href="javascript:history.back()" class="btn btn-outline-secondary">
                        <i class="fas fa-arrow-left me-1"></i> Go Back
                    </a>
                    <a href="{% url 'dashboard' %}" class="btn btn-primary">
                        <i class="fas fa-home me-1"></i> Go to Dashboard
                    </a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### Add the middleware to settings

```python
# SEPM/settings.py - Add the middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'SEPM.middleware.GlobalErrorHandlingMiddleware',  # Add this line
]
```

## 5. Maintenance-focused Enhancements

### Add a maintenance work order model

```python
# equipment/models.py - Add maintenance work order model

class MaintenanceWorkOrder(models.Model):
    """Model for maintenance work orders"""
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    )
    
    TYPE_CHOICES = (
        ('preventive', 'Preventive'),
        ('corrective', 'Corrective'),
        ('predictive', 'Predictive'),
        ('emergency', 'Emergency'),
    )
    
    work_order_number = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=200)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='work_orders')
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    work_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='corrective')
    
    # Scheduling
    scheduled_start_date = models.DateField()
    scheduled_end_date = models.DateField()
    estimated_hours = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    
    # Actual execution
    actual_start_date = models.DateField(null=True, blank=True)
    actual_end_date = models.DateField(null=True, blank=True)
    actual_hours = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    
    # Assignment
    assigned_to = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, 
                                    null=True, blank=True, related_name='assigned_work_orders')
    created_by = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, 
                                   null=True, related_name='created_work_orders')
    
    # Parts used
    parts = models.ManyToManyField('parts.Part', through='MaintenanceWorkOrderPart', blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.work_order_number} - {self.title}"
    
    def is_overdue(self):
        """Check if work order is overdue"""
        from django.utils import timezone
        today = timezone.now().date()
        
        if self.status in ['open', 'in_progress'] and self.scheduled_end_date < today:
            return True
        return False
    
    def get_status_display_class(self):
        """Return the CSS class for the status display"""
        status_classes = {
            'open': 'bg-info',
            'in_progress': 'bg-primary',
            'completed': 'bg-success',
            'cancelled': 'bg-secondary',
        }
        return status_classes.get(self.status, 'bg-secondary')
    
    def get_priority_display_class(self):
        """Return the CSS class for the priority display"""
        priority_classes = {
            'low': 'bg-success',
            'medium': 'bg-info',
            'high': 'bg-warning',
            'critical': 'bg-danger',
        }
        return priority_classes.get(self.priority, 'bg-secondary')

class MaintenanceWorkOrderPart(models.Model):
    """Parts used in maintenance work orders"""
    work_order = models.ForeignKey(MaintenanceWorkOrder, on_delete=models.CASCADE)
    part = models.ForeignKey('parts.Part', on_delete=models.CASCADE)
    quantity_used = models.PositiveIntegerField(default=1)
    notes = models.TextField(blank=True)
    
    class Meta:
        unique_together = ('work_order', 'part')
    
    def __str__(self):
        return f"{self.work_order.work_order_number} - {self.part.part_number}"
```

### Add a dashboard widget for maintenance work orders

```html
<!-- templates/equipment/dashboard.html - Add maintenance work orders widget -->

<!-- Maintenance Work Orders -->
<div class="col-md-6 mb-4">
    <div class="card h-100">
        <div class="card-header bg-light">
            <div class="d-flex justify-content-between align-items-center">
                <h5 class="mb-0"><i class="fas fa-tasks me-2"></i> Maintenance Work Orders</h5>
                <a href="{% url 'work-order-list' %}" class="btn btn-sm btn-outline-primary">View All</a>
            </div>
        </div>
        <div class="card-body p-0">
            <div class="table-responsive">
                <table class="table table-hover mb-0">
                    <thead class="table-light">
                        <tr>
                            <th>WO #</th>
                            <th>Equipment</th>
                            <th>Status</th>
                            <th>Priority</th>
                            <th>Scheduled</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for wo in recent_work_orders %}
                        <tr>
                            <td>{{ wo.work_order_number }}</td>
                            <td>
                                <a href="{% url 'equipment-detail' wo.equipment.pk %}">
                                    {{ wo.equipment.equipment_code }}
                                </a>
                            </td>
                            <td>
                                <span class="badge {{ wo.get_status_display_class }}">
                                    {{ wo.get_status_display }}
                                </span>
                            </td>
                            <td>
                                <span class="badge {{ wo.get_priority_display_class }}">
                                    {{ wo.get_priority_display }}
                                </span>
                            </td>
                            <td>
                                {{ wo.scheduled_start_date|date:"Y-m-d" }}
                                {% if wo.is_overdue %}
                                <span class="badge bg-danger ms-1">Overdue</span>
                                {% endif %}
                            </td>
                            <td>
                                <a href="{% url 'work-order-detail' wo.pk %}" class="btn btn-sm btn-outline-info">
                                    <i class="fas fa-eye"></i>
                                </a>
                            </td>
                        </tr>
                        {% empty %}
                        <tr>
                            <td colspan="6" class="text-center py-3">No work orders found.</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>
```

### Update dashboard view to include work orders

```python
# equipment/views.py - Update dashboard view to include work orders

@login_required
def dashboard(request):
    equipment_count = Equipment.objects.count()
    part_count = Part.objects.count()
    category_count = Category.objects.count()
    document_count = Document.objects.count()
    
    # Get equipment that need maintenance
    maintenance_equipment = Equipment.objects.filter(status='maintenance').count()
    
    # Get low stock parts
    low_stock_parts = []
    for part in Part.objects.all():
        if part.is_low_stock() or part.is_out_of_stock():
            low_stock_parts.append(part)
    
    # Get recent work orders
    from django.utils import timezone
    today = timezone.now().date()
    
    recent_work_orders = MaintenanceWorkOrder.objects.filter(
        scheduled_end_date__gte=today
    ).order_by('scheduled_start_date')[:5]
    
    # Get overdue work orders
    overdue_work_orders_count = MaintenanceWorkOrder.objects.filter(
        status__in=['open', 'in_progress'],
        scheduled_end_date__lt=today
    ).count()
    
    context = {
        'equipment_count': equipment_count,
        'part_count': part_count,
        'category_count': category_count,
        'document_count': document_count,
        'maintenance_equipment': maintenance_equipment,
        'recent_equipment': Equipment.objects.order_by('-updated_at')[:5],
        'recent_parts': Part.objects.order_by('-updated_at')[:5],
        'low_stock_parts': low_stock_parts[:5],
        'recent_work_orders': recent_work_orders,
        'overdue_work_orders_count': overdue_work_orders_count
    }
    return render(request, 'equipment/dashboard.html', context)
```

## 6. Testing Improvements

### Create a basic test for equipment model

```python
# equipment/tests.py - Add basic tests

from django.test import TestCase
from .models import Equipment, Category

class EquipmentModelTests(TestCase):
    def setUp(self):
        # Create test category
        self.category = Category.objects.create(
            name="Test Category",
            description="Test Category Description"
        )
        
        # Create parent equipment
        self.parent_equipment = Equipment.objects.create(
            equipment_code="TEST-001",
            name="Test Parent Equipment",
            category=self.category,
            status="active",
            description="Test Parent Equipment Description"
        )
        
        # Create child equipment
        self.child_equipment = Equipment.objects.create(
            equipment_code="TEST-002",
            name="Test Child Equipment",
            parent=self.parent_equipment,
            position="101",
            category=self.category,
            status="active",
            description="Test Child Equipment Description"
        )
    
    def test_equipment_creation(self):
        """Test equipment creation"""
        self.assertEqual(self.parent_equipment.equipment_code, "TEST-001")
        self.assertEqual(self.parent_equipment.name, "Test Parent Equipment")
        self.assertEqual(self.parent_equipment.status, "active")
        
    def test_equipment_hierarchy(self):
        """Test equipment hierarchy"""
        self.assertEqual(self.child_equipment.parent, self.parent_equipment)
        self.assertTrue(self.parent_equipment in self.child_equipment.get_ancestors())
        
    def test_get_full_code(self):
        """Test get_full_code method"""
        self.assertEqual(self.parent_equipment.get_full_code(), "TEST-001")
        self.assertEqual(self.child_equipment.get_full_code(), "TEST-001 / TEST-002")
```

### Create a basic test for parts model

```python
# parts/tests.py - Add basic tests

from django.test import TestCase
from .models import Part, PartCategory

class PartModelTests(TestCase):
    def setUp(self):
        # Create test category
        self.category = PartCategory.objects.create(
            name="Test Category",
            description="Test Category Description"
        )
        
        # Create test part
        self.part = Part.objects.create(
            part_number="PN-001",
            name="Test Part",
            category=self.category,
            description="Test Part Description",
            unit="pcs",
            current_stock=10,
            min_stock_level=5,
            status="active"
        )
        
        # Create low stock part
        self.low_stock_part = Part.objects.create(
            part_number="PN-002",
            name="Low Stock Part",
            category=self.category,
            description="Low Stock Part Description",
            unit="pcs",
            current_stock=3,
            min_stock_level=5,
            status="active"
        )
        
        # Create out of stock part
        self.out_of_stock_part = Part.objects.create(
            part_number="PN-003",
            name="Out of Stock Part",
            category=self.category,
            description="Out of Stock Part Description",
            unit="pcs",
            current_stock=0,
            min_stock_level=5,
            status="active"
        )
    
    def test_part_creation(self):
        """Test part creation"""
        self.assertEqual(self.part.part_number, "PN-001")
        self.assertEqual(self.part.name, "Test Part")
        self.assertEqual(self.part.status, "active")
        
    def test_is_low_stock(self):
        """Test is_low_stock method"""
        self.assertFalse(self.part.is_low_stock())
        self.assertTrue(self.low_stock_part.is_low_stock())
        self.assertFalse(self.out_of_stock_part.is_low_stock())
        
    def test_is_out_of_stock(self):
        """Test is_out_of_stock method"""
        self.assertFalse(self.part.is_out_of_stock())
        self.assertFalse(self.low_stock_part.is_out_of_stock())
        self.assertTrue(self.out_of_stock_part.is_out_of_stock())
```

## 7. Installation and Setup Instructions

Create a proper README.md file:

```markdown
# Service Equipment and Parts Management (SEPM)

A comprehensive system for maintenance engineering departments to manage equipment, parts, documentation, and maintenance work orders.

## Features

- **Equipment Management**: Hierarchical equipment structure with categories, status tracking, and detailed information
- **Parts Inventory**: Track parts, suppliers, stock levels, and associations with equipment
- **Documentation**: Upload and manage equipment and part documentation
- **Maintenance Work Orders**: Create and track maintenance work orders
- **Import/Export**: Import and export data in CSV or Excel formats
- **User Management**: Role-based access control (admin, staff, read-only)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/sepm.git
   cd sepm
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file based on the template:
   ```
   cp .env.example .env
   ```
   Update the `.env` file with your database credentials and other settings.

5. Run migrations:
   ```
   python manage.py migrate
   ```

6. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```
   python manage.py runserver
   ```

8. Access the application at http://127.0.0.1:8000/

## Usage

1. Log in with your credentials
2. Use the dashboard to navigate to different sections
3. Add equipment, parts, suppliers, and documentation
4. Create maintenance work orders
5. Generate reports

## Environment Variables

- `DB_NAME`: Database name
- `DB_USER`: Database user
- `DB_PASSWORD`: Database password
- `DB_HOST`: Database host
- `DB_PORT`: Database port
- `SECRET_KEY`: Django secret key
- `DEBUG`: Set to 'True' for development, 'False' for production

## Requirements

- Python 3.8+
- PostgreSQL 12+
- Additional requirements are listed in requirements.txt
```

## 8. Update requirements.txt

```
Django==5.1.6
psycopg2-binary==2.9.9
django-mptt==0.15.0
django-crispy-forms==2.0
crispy-bootstrap5==0.7
Pillow==10.1.0
pandas==2.1.2
openpyxl==3.1.2
python-dotenv==1.0.0  # Added for environment variables
whitenoise==6.5.0     # Added for static file serving
gunicorn==21.2.0      # Added for production deployment
pytest==7.4.0         # Added for testing
pytest-django==4.5.2  # Added for Django testing
```