from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from decimal import Decimal
from products.models import Product, Category
from orders.models import Order, OrderItem


class CheckoutViewTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Vinyl")
        self.product = Product.objects.create(
            name="Test Record",
            slug="test-record",
            category=self.category,
            price=Decimal("24.99"),
            stock=10
        )
        self.user = User.objects.create_user(username="checkoutuser", password="pass1234")
        self.client.force_login(self.user)

        session = self.client.session
        session['cart'] = {
            str(self.product.id): {
                'name': self.product.name,
                'price': str(self.product.price),
                'quantity': 2
            }
        }
        session.save()

    def test_checkout_creates_order_and_orderitems(self):
        response = self.client.post(reverse('checkout:checkout'), {
            'full_name': 'Test User',
            'email': 'test@example.com',
            'number': '1234567890',
            'shipping_address': '123 Test Lane',
            'shipping_city': 'Testville',
            'shipping_postcode': 'TE5 7ST',
            'same_as_shipping': 'on', # 'yes' for separate billing
            'billing_address': '123 Test Lane',
            'billing_city': 'Testville',
            'billing_postcode': 'TE5 7ST'
        })

        self.assertEqual(response.status_code, 302)  # Redirect on success

        # One order should now exist
        order = Order.objects.first()
        self.assertIsNotNone(order)
        self.assertEqual(order.total_amount, Decimal("49.98"))

        # One order item linked
        order_items = OrderItem.objects.filter(order=order)
        self.assertEqual(order_items.count(), 1)
        self.assertEqual(order_items[0].quantity, 2)
        self.assertEqual(order_items[0].product, self.product)

        # Cart should be cleared
        session = self.client.session
        self.assertNotIn('cart', session)
