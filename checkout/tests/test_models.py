from django.test import TestCase
from decimal import Decimal
from django.contrib.auth import get_user_model
from products.models import Product
from checkout.models import CheckoutOrder, CheckoutItem

User = get_user_model()

class CheckoutOrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='checkoutuser', password='password123')
        self.order = CheckoutOrder.objects.create(
            user=self.user,
            email='checkout@example.com',
            full_name='Tyler RT',
            total_amount=Decimal('49.99')
        )

    def test_order_str_method(self):
        expected = f"Order #{self.order.order_number} - {self.order.full_name}"
        self.assertEqual(str(self.order), expected)
    
    def test_order_number_is_generated_on_save(self):
        self.assertIsNotNone(self.order.order_number)
        self.assertTrue(CheckoutOrder.objects.filter(order_number=self.order.order_number).exists())

class CheckoutItemModelTest(TestCase):
    def setUp(self):
        self.order = CheckoutOrder.objects.create(
            email='itemcheckout@example.com',
            full_name='Guest User',
            total_amount=Decimal('0.00')
        )
        self.product = Product.objects.create(
            name='Checkout Product',
            description='Test checkout product',
            price=Decimal('25.00'),
            stock=10
        )
        self.item = CheckoutItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            price=Decimal('25.00')
        )

    def test_get_subtotal(self):
        self.assertEqual(self.item.get_subtotal(), Decimal('50.00'))