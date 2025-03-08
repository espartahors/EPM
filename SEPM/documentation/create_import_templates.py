import pandas as pd
import os

# Create directory for templates if it doesn't exist
templates_dir = 'import_templates'
os.makedirs(templates_dir, exist_ok=True)

# 1. Equipment Import Template
equipment_data = {
    'equipment_code': ['DP-XXXXX', 'DP-YYYYY'],
    'name': ['Equipment Name 1', 'Equipment Name 2'],
    'parent_code': ['', 'DP-XXXXX'],  # Leave blank for root equipment
    'position': ['010', '020'],
    'item_code': ['8.12345.A', '6.67890.B'],
    'revision': ['A', 'B'],
    'category': ['Mechanical', 'Electrical'],
    'status': ['active', 'active'],
    'description': ['Description for equipment 1', 'Description for equipment 2']
}

equipment_df = pd.DataFrame(equipment_data)
equipment_df.to_excel(f'{templates_dir}/equipment_import_template.xlsx', index=False)
equipment_df.to_csv(f'{templates_dir}/equipment_import_template.csv', index=False)

# 2. Parts Import Template
parts_data = {
    'part_number': ['5.12345.A', '6.67890.B'],
    'name': ['Part Name 1', 'Part Name 2'],
    'category': ['Mechanical', 'Electrical'],
    'description': ['Description for part 1', 'Description for part 2'],
    'unit': ['pcs', 'kg'],
    'current_stock': [10, 5],
    'min_stock_level': [5, 2],
    'status': ['active', 'active']
}

parts_df = pd.DataFrame(parts_data)
parts_df.to_excel(f'{templates_dir}/parts_import_template.xlsx', index=False)
parts_df.to_csv(f'{templates_dir}/parts_import_template.csv', index=False)

# 3. BOM Import Template
bom_data = {
    'equipment_code': ['DP-XXXXX', 'DP-XXXXX', 'DP-YYYYY'],
    'part_number': ['5.12345.A', '6.67890.B', '5.12345.A'],
    'position': ['102', '103', '201'],
    'quantity': [2, 1, 1],
    'notes': ['Part note 1', 'Part note 2', 'Part note 3']
}

bom_df = pd.DataFrame(bom_data)
bom_df.to_excel(f'{templates_dir}/bom_import_template.xlsx', index=False)
bom_df.to_csv(f'{templates_dir}/bom_import_template.csv', index=False)

# 4. Stock Update Template
stock_data = {
    'part_number': ['5.12345.A', '6.67890.B'],
    'current_stock': [15, 8],
    'update_date': ['2023-01-01', '2023-01-01'],
    'notes': ['Restocked from supplier', 'Received from order #12345']
}

stock_df = pd.DataFrame(stock_data)
stock_df.to_excel(f'{templates_dir}/stock_update_template.xlsx', index=False)
stock_df.to_csv(f'{templates_dir}/stock_update_template.csv', index=False)

print(f"Import templates created in '{templates_dir}' directory:")
print(f"1. Equipment Import Template (CSV & Excel)")
print(f"2. Parts Import Template (CSV & Excel)")
print(f"3. BOM Import Template (CSV & Excel)")
print(f"4. Stock Update Template (CSV & Excel)")