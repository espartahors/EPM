from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('equipment/', views.equipment_tree_view, name='equipment-tree'),
    path('equipment/<int:pk>/', views.equipment_detail, name='equipment-detail'),
    path('equipment/new/', views.EquipmentCreateView.as_view(), name='equipment-create'),
    path('equipment/<int:pk>/update/', views.EquipmentUpdateView.as_view(), name='equipment-update'),
    path('equipment/<int:pk>/delete/', views.EquipmentDeleteView.as_view(), name='equipment-delete'),
    path('equipment/<int:equipment_id>/add-part/', views.add_part_to_equipment, name='add-part-to-equipment'),
    path('equipment-part/<int:equipment_part_id>/remove/', views.remove_part_from_equipment, name='remove-part-from-equipment'),
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/new/', views.CategoryCreateView.as_view(), name='category-create'),
]