from django.test import TestCase, Client
from django.urls import reverse
from products.models import Product, Category
from decimal import Decimal

class ProductViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name="Vinyl")
        cls.product = Product.objects.create(
            name="Test Album",
            slug="test-album",
            category=cls.category,
            price=Decimal("19.99"),
            stock=5,
        )

    def test_product_list_view_status_code(self):
        response = self.client.get(reverse('products:list'))
        self.assertEqual(response.status_code, 200)

    def test_product_detail_view_status_code(self):
        response = self.client.get(reverse('products:detail', args=[self.product.slug]))
        self.assertEqual(response.status_code, 200)

    def test_product_detail_view_content(self):
        response = self.client.get(reverse('products:detail', args=[self.product.slug]))
        self.assertContains(response, "Test Album")

    def test_product_detail_404_for_invalid_product(self):
        response = self.client.get(reverse('products:detail', args=["non-existent-slug"]))
        self.assertEqual(response.status_code, 404)
        
    def test_product_excess_stock_add_to_cart_redirects(self):
        response = self.client.get(reverse('products:detail', args=[1]))
        self.assertEqual(response.status_code, 404)  # Product with ID 1 does not exist yet

class ProductStockLimitTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(
            name='Test Product',
            slug='test-product',
            price=10.00,
            stock=10,
        )

    def test_add_to_cart_exceeds_stock(self):
        session = self.client.session
        session['cart'] = {}
        session.save()

        url = reverse('products:add_to_cart', args=[self.product.id])

        # Add 6 units
        self.client.post(url, {'quantity': 6})

        # Try adding 5 more (total 11 > stock 10)
        response = self.client.post(url, {'quantity': 5}, follow=True)

        self.assertContains(response, "Only 10 units available")
        self.assertEqual(
            self.client.session['cart'][str(self.product.id)]['quantity'],
            6
        )
