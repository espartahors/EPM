from django.db import models
from django.utils import timezone

class PartCategory(models.Model):
    """Categories for parts"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = 'Part Categories'
    
    def __str__(self):
        return self.name

class Supplier(models.Model):
    """Suppliers for parts"""
    name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    website = models.URLField(blank=True)
    
    def __str__(self):
        return self.name

class Part(models.Model):
    """Part model for individual components"""
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('obsolete', 'Obsolete'),
        ('discontinued', 'Discontinued'),
    )
    
    part_number = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    category = models.ForeignKey(PartCategory, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True)
    suppliers = models.ManyToManyField(Supplier, through='PartSupplier', blank=True)
    unit = models.CharField(max_length=20, default='pcs')
    current_stock = models.PositiveIntegerField(default=0)
    min_stock_level = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.part_number} - {self.name}"
    
    def is_low_stock(self):
        """Check if the part is in low stock"""
        return self.current_stock <= self.min_stock_level and self.current_stock > 0
    
    def is_out_of_stock(self):
        """Check if the part is out of stock"""
        return self.current_stock == 0

class PartSupplier(models.Model):
    """Association model between Part and Supplier"""
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    supplier_part_number = models.CharField(max_length=50, blank=True)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    lead_time_days = models.PositiveIntegerField(null=True, blank=True)
    is_preferred = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    
    class Meta:
        unique_together = ('part', 'supplier')
    
    def __str__(self):
        return f"{self.part.part_number} from {self.supplier.name}"