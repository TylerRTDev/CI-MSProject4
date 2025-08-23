from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from products.models import Product
from orders.models import Order, OrderItem

User = get_user_model()

class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.order = Order.objects.create(
            user=self.user,
            email='test@example.com',
            address='123 Test Street',
            city='Testville',
            postcode='AB12 3CD',
            total_amount=Decimal('99.99')
        )

    def test_order_str_method(self):
        self.assertEqual(str(self.order), f"Order #{self.order.id} - {self.order.user if hasattr(self.order, 'user') else 'None'}")

class OrderItemModelTest(TestCase):
    def setUp(self):
        self.order = Order.objects.create(
            email='item@example.com',
            total_amount=Decimal('0.00')
        )
        self.product = Product.objects.create(
            name='Test Product',
            description='A test product.',
            price=Decimal('10.00'),
            stock=5
        )
        self.item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=3,
            price=Decimal('10.00')
        )

    def test_get_subtotal(self):
        self.assertEqual(self.item.get_subtotal(), Decimal('30.00'))
    

