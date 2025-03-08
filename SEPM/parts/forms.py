from django import forms
from .models import Part, PartCategory, Supplier, PartSupplier

class PartForm(forms.ModelForm):
    class Meta:
        model = Part
        fields = ['part_number', 'name', 'category', 'description', 
                  'unit', 'current_stock', 'min_stock_level', 'status']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class PartCategoryForm(forms.ModelForm):
    class Meta:
        model = PartCategory
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact_person', 'email', 'phone', 'address', 'website']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }

class PartSupplierForm(forms.ModelForm):
    class Meta:
        model = PartSupplier
        fields = ['supplier', 'supplier_part_number', 'unit_cost', 
                  'lead_time_days', 'is_preferred', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 2}),
        }