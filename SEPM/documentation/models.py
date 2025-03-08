from django.db import models
from django.utils import timezone
from equipment.models import Equipment
from parts.models import Part

class Document(models.Model):
    """Model for storing documents"""
    DOCUMENT_TYPES = (
        ('drawing', 'Drawing'),
        ('manual', 'Manual'),
        ('bom', 'Bill of Materials'),
        ('datasheet', 'Datasheet'),
        ('certificate', 'Certificate'),
        ('report', 'Report'),
        ('other', 'Other'),
    )
    
    title = models.CharField(max_length=200)
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    file = models.FileField(upload_to='documents/')
    filename = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, null=True, blank=True)
    part = models.ForeignKey(Part, on_delete=models.CASCADE, null=True, blank=True)
    revision = models.CharField(max_length=20, blank=True)
    is_current = models.BooleanField(default=True)
    uploaded_by = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def get_file_extension(self):
        """Get the file extension"""
        return self.file.name.split('.')[-1].lower()
    
    def is_image(self):
        """Check if the document is an image"""
        image_extensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'svg']
        return self.get_file_extension() in image_extensions
    
    def is_pdf(self):
        """Check if the document is a PDF"""
        return self.get_file_extension() == 'pdf'
    
    def save(self, *args, **kwargs):
        """Override save to store the original filename"""
        if not self.filename and self.file:
            self.filename = self.file.name.split('/')[-1]
        super().save(*args, **kwargs)

class ImportLog(models.Model):
    """Log for import operations"""
    IMPORT_TYPES = (
        ('equipment', 'Equipment Import'),
        ('parts', 'Parts Import'),
        ('bom', 'BOM Import'),
        ('stock', 'Stock Update'),
    )
    
    import_type = models.CharField(max_length=20, choices=IMPORT_TYPES)
    file = models.FileField(upload_to='imports/')
    status = models.CharField(max_length=20, default='processing')
    items_processed = models.IntegerField(default=0)
    items_created = models.IntegerField(default=0)
    items_updated = models.IntegerField(default=0)
    items_failed = models.IntegerField(default=0)
    log_details = models.TextField(blank=True)
    imported_by = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True)
    imported_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.import_type} - {self.imported_at}"
    
    def complete(self):
        """Mark the import as complete"""
        self.status = 'completed'
        self.completed_at = timezone.now()
        self.save()

class ExportLog(models.Model):
    """Log for export operations"""
    EXPORT_TYPES = (
        ('equipment', 'Equipment Export'),
        ('parts', 'Parts Export'),
        ('bom', 'BOM Export'),
    )
    
    export_type = models.CharField(max_length=20, choices=EXPORT_TYPES)
    file = models.FileField(upload_to='exports/')
    items_exported = models.IntegerField(default=0)
    exported_by = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True)
    exported_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.export_type} - {self.exported_at}"