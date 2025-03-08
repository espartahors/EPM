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