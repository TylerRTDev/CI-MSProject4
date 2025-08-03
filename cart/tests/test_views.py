from django.test import TestCase
from django.urls import reverse
from products.models import Product, Category
from django.contrib.auth.models import User
from decimal import Decimal

class CartViewTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="CD")
        self.product = Product.objects.create(
            name="Session Test",
            slug="session-test",
            category=self.category,
            price=Decimal("9.99"),
            stock=10
        )
        self.session = self.client.session
        self.session['cart'] = {
            str(self.product.id): {
                'quantity': 1,
                'price': (str(self.product.price)),
                'name': self.product.name,
            }
        }
        self.session.save()

    def test_update_cart_quantity_increases(self):
        response = self.client.post(reverse('cart:update_cart'), {
            'item_id': Decimal(self.product.id),
            'quantity': 3
        })
        self.assertRedirects(response, reverse('cart:view_cart'))
        updated_cart = self.client.session['cart']
        self.assertEqual(updated_cart[str(self.product.id)]['quantity'], 3)

    def test_update_cart_quantity_removes_item(self):
        response = self.client.post(reverse('cart:update_cart'), {
            'item_id': str(self.product.id),
            'quantity': 0
        })
        self.assertRedirects(response, reverse('cart:view_cart'))
        updated_cart = self.client.session['cart']
        self.assertNotIn(str(self.product.id), updated_cart)
