from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from .models import Part, PartCategory, Supplier, PartSupplier
from .forms import PartForm, PartCategoryForm, SupplierForm, PartSupplierForm
from documentation.models import Document

@login_required
def part_list(request):
    """List all parts with filtering options"""
    parts = Part.objects.all()
    categories = PartCategory.objects.all()
    
    # Filter by search term
    search_term = request.GET.get('search', '')
    if search_term:
        parts = parts.filter(
            Q(part_number__icontains=search_term) | 
            Q(name__icontains=search_term) | 
            Q(description__icontains=search_term)
        )
    
    # Filter by category
    category_id = request.GET.get('category', '')
    if category_id:
        parts = parts.filter(category_id=category_id)
    
    # Filter by status
    status = request.GET.get('status', '')
    if status:
        parts = parts.filter(status=status)
    
    # Filter by stock level
    stock_filter = request.GET.get('stock', '')
    if stock_filter == 'low':
        parts = [part for part in parts if part.is_low_stock()]
    elif stock_filter == 'out':
        parts = [part for part in parts if part.is_out_of_stock()]
    
    context = {
        'parts': parts,
        'categories': categories,
        'search_term': search_term,
        'category_id': category_id,
        'status': status,
        'stock_filter': stock_filter,
    }
    return render(request, 'parts/part_list.html', context)

@login_required
def part_detail(request, pk):
    """View part details including associated equipment and documents"""
    part = get_object_or_404(Part, pk=pk)
    equipment_parts = part.equipmentpart_set.all()
    part_suppliers = PartSupplier.objects.filter(part=part)
    documents = Document.objects.filter(part=part)
    
    context = {
        'part': part,
        'equipment_parts': equipment_parts,
        'part_suppliers': part_suppliers,
        'documents': documents,
    }
    return render(request, 'parts/part_detail.html', context)

class PartCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Part
    form_class = PartForm
    template_name = 'parts/part_form.html'
    success_url = reverse_lazy('part-list')
    
    def test_func(self):
        return not self.request.user.is_read_only
    
    def form_valid(self, form):
        messages.success(self.request, 'Part created successfully!')
        return super().form_valid(form)

class PartUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Part
    form_class = PartForm
    template_name = 'parts/part_form.html'
    
    def test_func(self):
        return not self.request.user.is_read_only
    
    def get_success_url(self):
        return reverse_lazy('part-detail', kwargs={'pk': self.object.pk})

class PartDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Part
    template_name = 'parts/part_confirm_delete.html'
    success_url = reverse_lazy('part-list')
    
    def test_func(self):
        return not self.request.user.is_read_only and self.request.user.is_staff_user

# Part Category Views
class PartCategoryListView(LoginRequiredMixin, ListView):
    model = PartCategory
    template_name = 'parts/category_list.html'
    context_object_name = 'categories'

class PartCategoryCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = PartCategory
    form_class = PartCategoryForm
    template_name = 'parts/category_form.html'
    success_url = reverse_lazy('part-category-list')
    
    def test_func(self):
        return not self.request.user.is_read_only

# Supplier Views
class SupplierListView(LoginRequiredMixin, ListView):
    model = Supplier
    template_name = 'parts/supplier_list.html'
    context_object_name = 'suppliers'

class SupplierDetailView(LoginRequiredMixin, DetailView):
    model = Supplier
    template_name = 'parts/supplier_detail.html'
    
class SupplierCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'parts/supplier_form.html'
    success_url = reverse_lazy('supplier-list')
    
    def test_func(self):
        return not self.request.user.is_read_only

# Add supplier to part
@login_required
def add_supplier_to_part(request, part_id):
    """Add a supplier to a part"""
    part = get_object_or_404(Part, pk=part_id)
    
    if request.user.is_read_only:
        messages.error(request, 'You do not have permission to add suppliers.')
        return redirect('part-detail', pk=part.pk)
    
    if request.method == 'POST':
        form = PartSupplierForm(request.POST)
        if form.is_valid():
            part_supplier = form.save(commit=False)
            part_supplier.part = part
            part_supplier.save()
            messages.success(request, 'Supplier added to part successfully!')
            return redirect('part-detail', pk=part.pk)
    else:
        form = PartSupplierForm()
    
    context = {
        'form': form,
        'part': part,
    }
    return render(request, 'parts/add_supplier_to_part.html', context)

class PartCategoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = PartCategory
    form_class = PartCategoryForm
    template_name = 'parts/part_category_form.html'
    success_url = reverse_lazy('part-category-list')
    
    def test_func(self):
        return not self.request.user.is_read_only

class PartCategoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = PartCategory
    template_name = 'parts/part_category_confirm_delete.html'
    success_url = reverse_lazy('part-category-list')
    
    def test_func(self):
        return not self.request.user.is_read_only and self.request.user.is_staff_user