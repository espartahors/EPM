from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
import pandas as pd
import csv
import mimetypes
from .models import Document, ImportLog, ExportLog
from .forms import DocumentForm, ImportForm, ExportForm
from equipment.models import Equipment
from parts.models import Part
from django.http import HttpResponse, FileResponse

# Add these functions to download templates
def download_equipment_template(request, format='xlsx'):
    """Download equipment import template"""
    if format not in ['xlsx', 'csv']:
        format = 'xlsx'
    
    filename = f'equipment_import_template.{format}'
    filepath = os.path.join(settings.MEDIA_ROOT, 'templates', filename)
    
    if os.path.exists(filepath):
        response = FileResponse(open(filepath, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    
    return HttpResponse('Template file not found.', status=404)

def download_parts_template(request, format='xlsx'):
    """Download parts import template"""
    if format not in ['xlsx', 'csv']:
        format = 'xlsx'
    
    filename = f'parts_import_template.{format}'
    filepath = os.path.join(settings.MEDIA_ROOT, 'templates', filename)
    
    if os.path.exists(filepath):
        response = FileResponse(open(filepath, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    
    return HttpResponse('Template file not found.', status=404)

def download_bom_template(request, format='xlsx'):
    """Download BOM import template"""
    if format not in ['xlsx', 'csv']:
        format = 'xlsx'
    
    filename = f'bom_import_template.{format}'
    filepath = os.path.join(settings.MEDIA_ROOT, 'templates', filename)
    
    if os.path.exists(filepath):
        response = FileResponse(open(filepath, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    
    return HttpResponse('Template file not found.', status=404)

def download_stock_template(request, format='xlsx'):
    """Download stock update template"""
    if format not in ['xlsx', 'csv']:
        format = 'xlsx'
    
    filename = f'stock_update_template.{format}'
    filepath = os.path.join(settings.MEDIA_ROOT, 'templates', filename)
    
    if os.path.exists(filepath):
        response = FileResponse(open(filepath, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    
    return HttpResponse('Template file not found.', status=404)

@login_required
def document_list(request):
    """List all documents with filtering options"""
    documents = Document.objects.all()
    
    # Filter by document type
    doc_type = request.GET.get('type', '')
    if doc_type:
        documents = documents.filter(document_type=doc_type)
    
    # Filter by equipment or part
    equipment_id = request.GET.get('equipment', '')
    if equipment_id:
        documents = documents.filter(equipment_id=equipment_id)
    
    part_id = request.GET.get('part', '')
    if part_id:
        documents = documents.filter(part_id=part_id)
    
    context = {
        'documents': documents,
        'doc_type': doc_type,
        'equipment_id': equipment_id,
        'part_id': part_id,
    }
    return render(request, 'documentation/document_list.html', context)

@login_required
def document_detail(request, pk):
    """View document details"""
    document = get_object_or_404(Document, pk=pk)
    
    context = {
        'document': document,
    }
    return render(request, 'documentation/document_detail.html', context)

class DocumentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Document
    form_class = DocumentForm
    template_name = 'documentation/document_form.html'
    success_url = reverse_lazy('document-list')
    
    def test_func(self):
        return not self.request.user.is_read_only
    
    def form_valid(self, form):
        form.instance.uploaded_by = self.request.user
        messages.success(self.request, 'Document uploaded successfully!')
        return super().form_valid(form)

class DocumentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Document
    form_class = DocumentForm
    template_name = 'documentation/document_form.html'
    
    def test_func(self):
        return not self.request.user.is_read_only
    
    def get_success_url(self):
        return reverse_lazy('document-detail', kwargs={'pk': self.object.pk})

class DocumentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Document
    template_name = 'documentation/document_confirm_delete.html'
    success_url = reverse_lazy('document-list')
    
    def test_func(self):
        return not self.request.user.is_read_only

@login_required
def document_download(request, pk):
    """Download document file"""
    document = get_object_or_404(Document, pk=pk)
    file_path = document.file.path
    
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type=mimetypes.guess_type(file_path)[0])
            response['Content-Disposition'] = f'attachment; filename={document.filename}'
            return response
    
    messages.error(request, 'File not found.')
    return redirect('document-detail', pk=document.pk)

@login_required
def document_view(request, pk):
    """View document inline (for PDFs and images)"""
    document = get_object_or_404(Document, pk=pk)
    file_path = document.file.path
    
    if document.is_pdf() or document.is_image():
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type=mimetypes.guess_type(file_path)[0])
                response['Content-Disposition'] = f'inline; filename={document.filename}'
                return response
    
    messages.error(request, 'File cannot be viewed inline.')
    return redirect('document-detail', pk=document.pk)

# Import/Export Views
@login_required
def import_data(request):
    """Import data from CSV or Excel"""
    if request.user.is_read_only:
        messages.error(request, 'You do not have permission to import data.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = ImportForm(request.POST, request.FILES)
        if form.is_valid():
            import_type = form.cleaned_data['import_type']
            file = request.FILES['file']
            
            # Create import log
            import_log = ImportLog.objects.create(
                import_type=import_type,
                file=file,
                imported_by=request.user,
                status='processing'
            )
            
            # Process the import based on type
            try:
                if file.name.endswith('.csv'):
                    df = pd.read_csv(file)
                elif file.name.endswith(('.xls', '.xlsx')):
                    df = pd.read_excel(file)
                else:
                    raise ValueError("Unsupported file format")
                
                # Process dataframe based on import type
                if import_type == 'equipment':
                    result = process_equipment_import(df, import_log)
                elif import_type == 'parts':
                    result = process_parts_import(df, import_log)
                elif import_type == 'bom':
                    result = process_bom_import(df, import_log)
                elif import_type == 'stock':
                    result = process_stock_update(df, import_log)
                
                import_log.complete()
                messages.success(request, f'Import completed successfully. {result["created"]} items created, {result["updated"]} items updated.')
            
            except Exception as e:
                import_log.status = 'failed'
                import_log.log_details = str(e)
                import_log.save()
                messages.error(request, f'Import failed: {str(e)}')
            
            return redirect('import-logs')
    else:
        form = ImportForm()
    
    context = {
        'form': form,
    }
    return render(request, 'documentation/import_form.html', context)

@login_required
def export_data(request):
    """Export data to CSV or Excel"""
    if request.method == 'POST':
        form = ExportForm(request.POST)
        if form.is_valid():
            export_type = form.cleaned_data['export_type']
            export_format = form.cleaned_data['export_format']
            
            # Generate export based on type
            try:
                if export_type == 'equipment':
                    data = list(Equipment.objects.values('equipment_code', 'name', 'position', 'item_code', 'revision', 'status', 'description'))
                elif export_type == 'parts':
                    data = list(Part.objects.values('part_number', 'name', 'description', 'unit', 'current_stock', 'min_stock_level', 'status'))
                elif export_type == 'bom':
                    # This would need more complex logic to generate BOM data
                    data = []
                
                # Create export file
                filename = f"{export_type}_export_{request.user.username}.{export_format}"
                file_path = os.path.join(settings.MEDIA_ROOT, 'exports', filename)
                
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                
                if export_format == 'csv':
                    with open(file_path, 'w', newline='') as f:
                        writer = csv.DictWriter(f, fieldnames=data[0].keys() if data else [])
                        writer.writeheader()
                        writer.writerows(data)
                elif export_format == 'xlsx':
                    df = pd.DataFrame(data)
                    df.to_excel(file_path, index=False)
                
                # Create export log
                export_log = ExportLog.objects.create(
                    export_type=export_type,
                    file=f'exports/{filename}',
                    items_exported=len(data),
                    exported_by=request.user
                )
                
                return redirect('download-export', pk=export_log.pk)
            
            except Exception as e:
                messages.error(request, f'Export failed: {str(e)}')
                return redirect('export-data')
    else:
        form = ExportForm()
    
    context = {
        'form': form,
    }
    return render(request, 'documentation/export_form.html', context)

@login_required
def download_export(request, pk):
    """Download exported file"""
    export_log = get_object_or_404(ExportLog, pk=pk)
    file_path = export_log.file.path
    
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type=mimetypes.guess_type(file_path)[0])
            response['Content-Disposition'] = f'attachment; filename={os.path.basename(file_path)}'
            return response
    
    messages.error(request, 'Export file not found.')
    return redirect('export-data')

@login_required
def import_logs(request):
    """View import logs"""
    logs = ImportLog.objects.order_by('-imported_at')
    
    context = {
        'logs': logs,
    }
    return render(request, 'documentation/import_logs.html', context)

@login_required
def export_logs(request):
    """View export logs"""
    logs = ExportLog.objects.order_by('-exported_at')
    
    context = {
        'logs': logs,
    }
    return render(request, 'documentation/export_logs.html', context)

# Helper functions for import processing
def process_equipment_import(df, import_log):
    """Process equipment import from dataframe"""
    created = 0
    updated = 0
    
    for _, row in df.iterrows():
        equipment_code = row.get('equipment_code')
        if not equipment_code:
            continue
        
        equipment, created_flag = Equipment.objects.update_or_create(
            equipment_code=equipment_code,
            defaults={
                'name': row.get('name', ''),
                'position': row.get('position', ''),
                'item_code': row.get('item_code', ''),
                'revision': row.get('revision', ''),
                'status': row.get('status', 'active'),
                'description': row.get('description', '')
            }
        )
        
        if created_flag:
            created += 1
        else:
            updated += 1
    
    import_log.items_processed = created + updated
    import_log.items_created = created
    import_log.items_updated = updated
    import_log.save()
    
    return {'created': created, 'updated': updated}

def process_parts_import(df, import_log):
    """Process parts import from dataframe"""
    created = 0
    updated = 0
    
    for _, row in df.iterrows():
        part_number = row.get('part_number')
        if not part_number:
            continue
        
        part, created_flag = Part.objects.update_or_create(
            part_number=part_number,
            defaults={
                'name': row.get('name', ''),
                'description': row.get('description', ''),
                'unit': row.get('unit', 'pcs'),
                'current_stock': row.get('current_stock', 0),
                'min_stock_level': row.get('min_stock_level', 0),
                'status': row.get('status', 'active')
            }
        )
        
        if created_flag:
            created += 1
        else:
            updated += 1
    
    import_log.items_processed = created + updated
    import_log.items_created = created
    import_log.items_updated = updated
    import_log.save()
    
    return {'created': created, 'updated': updated}

def process_bom_import(df, import_log):
    """Process BOM import from dataframe"""
    created = 0
    updated = 0
    
    # Implement BOM import logic
    
    import_log.items_processed = created + updated
    import_log.items_created = created
    import_log.items_updated = updated
    import_log.save()
    
    return {'created': created, 'updated': updated}

def process_stock_update(df, import_log):
    """Process stock update from dataframe"""
    updated = 0
    
    for _, row in df.iterrows():
        part_number = row.get('part_number')
        if not part_number:
            continue
        
        try:
            part = Part.objects.get(part_number=part_number)
            part.current_stock = row.get('current_stock', part.current_stock)
            part.save()
            updated += 1
        except Part.DoesNotExist:
            continue
    
    import_log.items_processed = updated
    import_log.items_updated = updated
    import_log.save()
    
    return {'created': 0, 'updated': updated}

@login_required
def document_view(request, pk):
    """View document inline (for PDFs and images)"""
    document = get_object_or_404(Document, pk=pk)
    
    context = {
        'document': document,
    }
    return render(request, 'documentation/document_view.html', context)
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