from django.urls import path
from . import views

urlpatterns = [
    path('', views.part_list, name='part-list'),
    path('<int:pk>/', views.part_detail, name='part-detail'),
    path('new/', views.PartCreateView.as_view(), name='part-create'),
    path('<int:pk>/update/', views.PartUpdateView.as_view(), name='part-update'),
    path('<int:pk>/delete/', views.PartDeleteView.as_view(), name='part-delete'),
    path('categories/', views.PartCategoryListView.as_view(), name='part-category-list'),
    path('categories/new/', views.PartCategoryCreateView.as_view(), name='part-category-create'),
    path('categories/<int:pk>/update/', views.PartCategoryUpdateView.as_view(), name='part-category-update'),
    path('categories/<int:pk>/delete/', views.PartCategoryDeleteView.as_view(), name='part-category-delete'),
    path('suppliers/', views.SupplierListView.as_view(), name='supplier-list'),
    path('suppliers/<int:pk>/', views.SupplierDetailView.as_view(), name='supplier-detail'),
    path('suppliers/new/', views.SupplierCreateView.as_view(), name='supplier-create'),
    path('<int:part_id>/add-supplier/', views.add_supplier_to_part, name='add-supplier-to-part'),
]