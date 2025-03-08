from django import forms
from .models import Equipment, Category, EquipmentPart
from parts.models import Part

class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['equipment_code', 'name', 'parent', 'position', 'item_code', 
                  'revision', 'category', 'status', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent'].queryset = Equipment.objects.exclude(pk=self.instance.pk if self.instance.pk else None)
        self.fields['parent'].required = False
        self.fields['parent'].label = 'Parent Equipment'

class EquipmentPartForm(forms.ModelForm):
    class Meta:
        model = EquipmentPart
        fields = ['part', 'position', 'quantity', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 2}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }