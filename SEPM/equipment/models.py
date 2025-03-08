from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from parts.models import Part
from django.utils import timezone

class Category(models.Model):
    """Model for equipment categories"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name

class Equipment(MPTTModel):
    """Equipment model with hierarchical structure"""
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('maintenance', 'Under Maintenance'),
        ('retired', 'Retired'),
    )
    
    equipment_code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, 
                            related_name='children')
    position = models.CharField(max_length=20, blank=True)
    item_code = models.CharField(max_length=50, blank=True)
    revision = models.CharField(max_length=10, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    description = models.TextField(blank=True)
    parts = models.ManyToManyField(Part, through='EquipmentPart', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class MPTTMeta:
        order_insertion_by = ['equipment_code']
    
    def __str__(self):
        return f"{self.equipment_code} - {self.name}"
    
    def get_full_code(self):
        """Returns the full hierarchical code"""
        ancestors = self.get_ancestors(include_self=True)
        return ' / '.join([ancestor.equipment_code for ancestor in ancestors])

class EquipmentPart(models.Model):
    """Association model between Equipment and Part"""
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    part = models.ForeignKey('parts.Part', on_delete=models.CASCADE)
    position = models.CharField(max_length=20, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    notes = models.TextField(blank=True)
    
    class Meta:
        unique_together = ('equipment', 'part', 'position')
    
    def __str__(self):
        return f"{self.equipment.equipment_code} - {self.part.part_number} (Pos: {self.position})"

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