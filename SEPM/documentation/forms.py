from django import forms
from .models import Document, ImportLog, ExportLog

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'document_type', 'file', 'description', 'equipment', 'part', 'revision', 'is_current']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['equipment'].required = False
        self.fields['part'].required = False

class ImportForm(forms.Form):
    IMPORT_CHOICES = (
        ('equipment', 'Equipment Import'),
        ('parts', 'Parts Import'),
        ('bom', 'BOM Import'),
        ('stock', 'Stock Update'),
    )
    
    import_type = forms.ChoiceField(choices=IMPORT_CHOICES)
    file = forms.FileField(help_text="Upload CSV or Excel file")
    header_row = forms.BooleanField(initial=True, required=False, help_text="File includes header row")
    update_existing = forms.BooleanField(initial=True, required=False, help_text="Update existing records")

class ExportForm(forms.Form):
    EXPORT_CHOICES = (
        ('equipment', 'Equipment Export'),
        ('parts', 'Parts Export'),
        ('bom', 'BOM Export'),
    )
    
    FORMAT_CHOICES = (
        ('csv', 'CSV File'),
        ('xlsx', 'Excel File'),
    )
    
    export_type = forms.ChoiceField(choices=EXPORT_CHOICES)
    export_format = forms.ChoiceField(choices=FORMAT_CHOICES, initial='xlsx')