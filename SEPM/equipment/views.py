from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib import messages
from .models import Equipment, Category, EquipmentPart
from parts.models import Part
from .forms import EquipmentForm, EquipmentPartForm, CategoryForm
from documentation.models import Document

@login_required
def dashboard(request):
    equipment_count = Equipment.objects.count()
    part_count = Part.objects.count()
    category_count = Category.objects.count()
    document_count = Document.objects.count()
    
    context = {
        'equipment_count': equipment_count,
        'part_count': part_count,
        'category_count': category_count,
        'document_count': document_count,
        'recent_equipment': Equipment.objects.order_by('-updated_at')[:5],
        'recent_parts': Part.objects.order_by('-updated_at')[:5],
    }
    return render(request, 'equipment/dashboard.html', context)

@login_required
def equipment_tree_view(request):
    """Display the equipment hierarchy as a tree"""
    root_equipment = Equipment.objects.filter(parent=None)
    categories = Category.objects.all()
    
    context = {
        'root_equipment': root_equipment,
        'categories': categories,
    }
    return render(request, 'equipment/equipment_tree.html', context)

@login_required
def equipment_detail(request, pk):
    """View equipment details including associated parts and documents"""
    equipment = get_object_or_404(Equipment, pk=pk)
    equipment_parts = EquipmentPart.objects.filter(equipment=equipment)
    documents = Document.objects.filter(equipment=equipment)
    
    # If this is an AJAX request, return only the details panel
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        context = {
            'equipment': equipment,
            'equipment_parts': equipment_parts,
            'documents': documents,
        }
        return render(request, 'equipment/equipment_detail.html', context)

    # Otherwise, return the full page
    context = {
        'equipment': equipment,
        'equipment_parts': equipment_parts,
        'documents': documents,
    }
    return render(request, 'equipment/equipment_detail_page.html', context)

class EquipmentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Equipment
    form_class = EquipmentForm
    template_name = 'equipment/equipment_form.html'
    success_url = reverse_lazy('equipment-tree')
    
    def test_func(self):
        return not self.request.user.is_read_only
    
    def form_valid(self, form):
        messages.success(self.request, 'Equipment created successfully!')
        return super().form_valid(form)

class EquipmentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Equipment
    form_class = EquipmentForm
    template_name = 'equipment/equipment_form.html'
    
    def test_func(self):
        return not self.request.user.is_read_only
    
    def get_success_url(self):
        return reverse_lazy('equipment-detail', kwargs={'pk': self.object.pk})

class EquipmentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Equipment
    template_name = 'equipment/equipment_confirm_delete.html'
    success_url = reverse_lazy('equipment-tree')
    
    def test_func(self):
        return not self.request.user.is_read_only and self.request.user.is_staff_user

# Equipment Part Views
@login_required
def add_part_to_equipment(request, equipment_id):
    """Add a part to equipment"""
    equipment = get_object_or_404(Equipment, pk=equipment_id)
    
    if request.method == 'POST':
        form = EquipmentPartForm(request.POST)
        if form.is_valid():
            equipment_part = form.save(commit=False)
            equipment_part.equipment = equipment
            equipment_part.save()
            messages.success(request, 'Part added to equipment successfully!')
            return redirect('equipment-detail', pk=equipment.pk)
    else:
        form = EquipmentPartForm()
    
    context = {
        'form': form,
        'equipment': equipment,
    }
    return render(request, 'equipment/add_part_to_equipment.html', context)

@login_required
def remove_part_from_equipment(request, equipment_part_id):
    """Remove a part from equipment"""
    equipment_part = get_object_or_404(EquipmentPart, pk=equipment_part_id)
    equipment = equipment_part.equipment
    
    if request.user.is_read_only:
        messages.error(request, 'You do not have permission to remove parts.')
        return redirect('equipment-detail', pk=equipment.pk)
    
    if request.method == 'POST':
        equipment_part.delete()
        messages.success(request, 'Part removed from equipment successfully!')
        return redirect('equipment-detail', pk=equipment.pk)
    
    context = {
        'equipment_part': equipment_part,
        'equipment': equipment,
    }
    return render(request, 'equipment/remove_part_confirm.html', context)

# Category Views
class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'equipment/category_list.html'
    context_object_name = 'categories'

class CategoryCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'equipment/category_form.html'
    success_url = reverse_lazy('category-list')
    
    def test_func(self):
        return not self.request.user.is_read_only

@login_required
def equipment_dashboard(request):
    """Main equipment dashboard with tree view and details panel"""
    context = {
        'equipment_count': Equipment.objects.count(),
        'category_count': Category.objects.count(),
    }
    return render(request, 'equipment/equipment_dashboard.html', context)

@login_required
def equipment_details_panel(request, pk):
    """Return the equipment details panel HTML"""
    equipment = get_object_or_404(Equipment, pk=pk)
    parts = EquipmentPart.objects.filter(equipment=equipment)
    documents = Document.objects.filter(equipment=equipment)
    
    context = {
        'equipment': equipment,
        'parts': parts,
        'documents': documents,
    }
    return render(request, 'equipment/equipment_details_panel.html', context)

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
    
    context = {
        'equipment_count': equipment_count,
        'part_count': part_count,
        'category_count': category_count,
        'document_count': document_count,
        'maintenance_equipment': maintenance_equipment,
        'recent_equipment': Equipment.objects.order_by('-updated_at')[:5],
        'recent_parts': Part.objects.order_by('-updated_at')[:5],
        'low_stock_parts': low_stock_parts[:5]
    }
    return render(request, 'equipment/dashboard.html', context)

from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Equipment

@login_required
def equipment_tree_data(request, parent_id=None):
    """
    Return JSON data for jsTree.
    This is a dedicated endpoint just for the tree data.
    """
    if parent_id:
        equipment_items = Equipment.objects.filter(parent_id=parent_id)
    else:
        equipment_items = Equipment.objects.filter(parent=None)
    
    # Format data for jsTree
    tree_data = []
    for item in equipment_items:
        has_children = Equipment.objects.filter(parent=item).exists()
        tree_data.append({
            'id': str(item.id),
            'text': f"{item.equipment_code} - {item.name}",
            'children': has_children,
            'type': item.status,  # For node styling
            'a_attr': {
                'href': f"/equipment/{item.id}/"
            }
        })
    
    return JsonResponse(tree_data, safe=False)