from django.test import TestCase
from decimal import Decimal
from products.models import Product, Category

class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name="Vinyl")
        cls.product = Product.objects.create(
            name="Test Album",
            category=cls.category,
            price=Decimal('19.99'),
            stock=10
        )

    def test_product_str_method(self):
        self.assertEqual(str(self.product), "Test Album")

    def test_product_category_relation(self):
        self.assertEqual(self.product.category.name, "Vinyl")

    def test_stock_quantity(self):
        self.assertEqual(self.product.stock, 10)

    def test_product_price_decimal(self):
        self.assertIsInstance(self.product.price, Decimal)  # or Decimal if using DecimalField
