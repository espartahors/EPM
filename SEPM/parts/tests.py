from django.test import TestCase
from .models import Part, PartCategory

class PartModelTests(TestCase):
    def setUp(self):
        # Create test category
        self.category = PartCategory.objects.create(
            name="Test Category",
            description="Test Category Description"
        )
        
        # Create test part
        self.part = Part.objects.create(
            part_number="PN-001",
            name="Test Part",
            category=self.category,
            description="Test Part Description",
            unit="pcs",
            current_stock=10,
            min_stock_level=5,
            status="active"
        )
        
        # Create low stock part
        self.low_stock_part = Part.objects.create(
            part_number="PN-002",
            name="Low Stock Part",
            category=self.category,
            description="Low Stock Part Description",
            unit="pcs",
            current_stock=3,
            min_stock_level=5,
            status="active"
        )
        
        # Create out of stock part
        self.out_of_stock_part = Part.objects.create(
            part_number="PN-003",
            name="Out of Stock Part",
            category=self.category,
            description="Out of Stock Part Description",
            unit="pcs",
            current_stock=0,
            min_stock_level=5,
            status="active"
        )
    
    def test_part_creation(self):
        """Test part creation"""
        self.assertEqual(self.part.part_number, "PN-001")
        self.assertEqual(self.part.name, "Test Part")
        self.assertEqual(self.part.status, "active")
        
    def test_is_low_stock(self):
        """Test is_low_stock method"""
        self.assertFalse(self.part.is_low_stock())
        self.assertTrue(self.low_stock_part.is_low_stock())
        self.assertFalse(self.out_of_stock_part.is_low_stock())
        
    def test_is_out_of_stock(self):
        """Test is_out_of_stock method"""
        self.assertFalse(self.part.is_out_of_stock())
        self.assertFalse(self.low_stock_part.is_out_of_stock())
        self.assertTrue(self.out_of_stock_part.is_out_of_stock())