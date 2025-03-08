from django.test import TestCase
from .models import Equipment, Category

class EquipmentModelTests(TestCase):
    def setUp(self):
        # Create test category
        self.category = Category.objects.create(
            name="Test Category",
            description="Test Category Description"
        )
        
        # Create parent equipment
        self.parent_equipment = Equipment.objects.create(
            equipment_code="TEST-001",
            name="Test Parent Equipment",
            category=self.category,
            status="active",
            description="Test Parent Equipment Description"
        )
        
        # Create child equipment
        self.child_equipment = Equipment.objects.create(
            equipment_code="TEST-002",
            name="Test Child Equipment",
            parent=self.parent_equipment,
            position="101",
            category=self.category,
            status="active",
            description="Test Child Equipment Description"
        )
    
    def test_equipment_creation(self):
        """Test equipment creation"""
        self.assertEqual(self.parent_equipment.equipment_code, "TEST-001")
        self.assertEqual(self.parent_equipment.name, "Test Parent Equipment")
        self.assertEqual(self.parent_equipment.status, "active")
        
    def test_equipment_hierarchy(self):
        """Test equipment hierarchy"""
        self.assertEqual(self.child_equipment.parent, self.parent_equipment)
        self.assertTrue(self.parent_equipment in self.child_equipment.get_ancestors())
        
    def test_get_full_code(self):
        """Test get_full_code method"""
        self.assertEqual(self.parent_equipment.get_full_code(), "TEST-001")
        self.assertEqual(self.child_equipment.get_full_code(), "TEST-001 / TEST-002")