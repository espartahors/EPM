from django.shortcuts import render
from django.db.models import Q
from equipment.models import Equipment
from parts.models import Part
from documentation.models import Document
from django.contrib.auth.decorators import login_required

@login_required
def global_search(request):
    """Global search across equipment, parts and documents"""
    query = request.GET.get('q', '')
    
    if not query:
        return render(request, 'global_search.html', {'query': query})
    
    # Search equipment
    equipment_results = Equipment.objects.filter(
        Q(equipment_code__icontains=query) |
        Q(name__icontains=query) |
        Q(item_code__icontains=query) |
        Q(description__icontains=query)
    )[:20]
    
    # Search parts
    parts_results = Part.objects.filter(
        Q(part_number__icontains=query) |
        Q(name__icontains=query) |
        Q(description__icontains=query)
    )[:20]
    
    # Search documents
    document_results = Document.objects.filter(
        Q(title__icontains=query) |
        Q(description__icontains=query) |
        Q(filename__icontains=query)
    )[:20]
    
    context = {
        'query': query,
        'equipment_results': equipment_results,
        'parts_results': parts_results,
        'document_results': document_results,
        'total_results': len(equipment_results) + len(parts_results) + len(document_results)
    }
    
    return render(request, 'global_search.html', context)