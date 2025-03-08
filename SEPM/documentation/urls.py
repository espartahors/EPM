from django.urls import path
from . import views

urlpatterns = [
    path('', views.document_list, name='document-list'),
    path('<int:pk>/', views.document_detail, name='document-detail'),
    path('new/', views.DocumentCreateView.as_view(), name='document-create'),
    path('<int:pk>/update/', views.DocumentUpdateView.as_view(), name='document-update'),
    path('<int:pk>/delete/', views.DocumentDeleteView.as_view(), name='document-delete'),
    path('<int:pk>/download/', views.document_download, name='document-download'),
    path('<int:pk>/view/', views.document_view, name='document-view'),
    path('import/', views.import_data, name='import-data'),
    path('export/', views.export_data, name='export-data'),
    path('import-logs/', views.import_logs, name='import-logs'),
    path('export-logs/', views.export_logs, name='export-logs'),
    path('download-export/<int:pk>/', views.download_export, name='download-export'),

    path('templates/equipment/<str:format>/', views.download_equipment_template, name='download-equipment-template'),
    path('templates/parts/<str:format>/', views.download_parts_template, name='download-parts-template'),
    path('templates/bom/<str:format>/', views.download_bom_template, name='download-bom-template'),
    path('templates/stock/<str:format>/', views.download_stock_template, name='download-stock-template'),

]